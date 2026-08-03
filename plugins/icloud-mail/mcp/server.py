#!/usr/bin/env python3
"""Dependency-free local MCP server for iCloud Mail over TLS IMAP and SMTP."""

from __future__ import annotations

import argparse
import base64
import binascii
import copy
import datetime as dt
import email
import email.generator
import email.policy
import email.utils
import html
import imaplib
import json
import os
from pathlib import Path
import re
import smtplib
import ssl
import stat
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager, nullcontext
from contextvars import ContextVar
from email.header import decode_header, make_header
from email.message import EmailMessage, Message
from email.parser import BytesHeaderParser
from typing import Any, Iterator


PROTOCOL_VERSION = "2025-06-18"
SERVER_INFO = {"name": "icloud-mail", "version": "0.1.0"}
IMAP_HOST = "imap.mail.me.com"
IMAP_PORT = 993
SMTP_HOST = "smtp.mail.me.com"
SMTP_PORT = 587
KEYCHAIN_SERVICE = "codex-icloud-mail"
CONFIG_VERSION = 1
MAX_RESULTS = 50
MAX_MOVE_RESULTS = 5
MAX_FLAG_RESULTS = 5
MAX_MAILBOX_RESULTS = 100
MAX_MAILBOX_STATUS = MAX_MAILBOX_RESULTS
MAX_MAILBOX_SCAN_ENTRIES = 1_000
MAX_MAILBOX_SCAN_BYTES = 512 * 1024
MAX_MAILBOX_ENTRY_BYTES = 8 * 1024
MAX_MAILBOX_NAME_CHARS = 500
MAX_MAILBOX_FLAGS = 50
MAX_MAILBOX_FLAG_CHARS = 1_000
MAX_MAILBOX_OUTPUT_BYTES = 128 * 1024
MAX_RECIPIENTS = 20
MAX_SEARCH_SCAN = 80
MAX_BODY_CHARS = 100_000
MAX_ATTACHMENT_BYTES = 5 * 1024 * 1024
MAX_MESSAGE_BYTES = 20 * 1024 * 1024
MAX_SUMMARY_HEADER_BYTES = 64 * 1024
MAX_SUMMARY_METADATA_BYTES = 1024 * 1024
MAX_SUMMARY_ADDRESS_CHARS = 8 * 1024
MAX_SUMMARY_ADDRESSES = 100
MAX_SUMMARY_REFERENCE_CHARS = 8 * 1024
MAX_SUMMARY_REFERENCES = 100
MAX_SUMMARY_SCALAR_CHARS = 4 * 1024
MAX_BODYSTRUCTURE_DEPTH = 50
MAX_MIME_DEPTH = 50
MAX_MIME_PARTS = 500
MAX_INCOMING_ATTACHMENTS = 100
REF_PREFIX = "icloud-mail:"
MCP_OPERATION_BUDGET_SECONDS = 540.0


class MailError(RuntimeError):
    """Safe, user-actionable mail error."""


class SummaryTooLarge(MailError):
    """A search result cannot be represented within the summary limits."""


class _MimePartLimitExceeded(Exception):
    """Internal parser sentinel translated to a safe public mail error."""


class OperationDeadline:
    """One monotonic budget shared by every phase of a public tool call."""

    def __init__(
        self,
        seconds: float = MCP_OPERATION_BUDGET_SECONDS,
        *,
        clock: Any = time.monotonic,
    ) -> None:
        self._clock = clock
        self._expires_at = clock() + seconds

    def timeout(self, cap: float) -> float:
        remaining = self._expires_at - self._clock()
        if remaining <= 0.1:
            raise MailError("iCloud Mail operation timed out before completion")
        return min(cap, remaining)


_ACTIVE_DEADLINE: ContextVar[OperationDeadline | None] = ContextVar(
    "icloud_mail_operation_deadline", default=None
)
_IMAP_LOGIN_CACHE: dict[str, str] = {}


def _current_deadline() -> OperationDeadline:
    return _ACTIVE_DEADLINE.get() or OperationDeadline()


def _set_socket_timeout(
    client: Any,
    cap: float,
    deadline: OperationDeadline | None = None,
) -> float:
    deadline = deadline or _ACTIVE_DEADLINE.get()
    connection_cap = client.__dict__.get("_codex_socket_timeout_cap")
    effective_cap = min(_timeout(), cap)
    if isinstance(connection_cap, (int, float)) and connection_cap > 0:
        effective_cap = min(effective_cap, float(connection_cap))
    timeout = deadline.timeout(effective_cap) if deadline else effective_cap
    socket = getattr(client, "sock", None)
    if socket is not None:
        socket.settimeout(timeout)
    return timeout


def _config_path() -> Path:
    override = os.environ.get("ICLOUD_MAIL_CONFIG_PATH", "").strip()
    if override:
        return Path(override).expanduser()
    if sys.platform == "darwin":
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / "Codex"
            / "iCloud Mail"
            / "config.json"
        )
    xdg_config = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg_config).expanduser() if xdg_config else Path.home() / ".config"
    return base / "codex" / "icloud-mail" / "config.json"


def _email_address(value: Any, name: str, *, required: bool = True) -> str:
    text = _text(value, name, required=required, limit=320)
    if not text:
        return ""
    display, address = email.utils.parseaddr(text)
    if display or not address or address != text or "@" not in address:
        raise ValueError(f"{name} must be one plain email address")
    local, domain = address.rsplit("@", 1)
    if not local or not domain or "." not in domain or any(
        character.isspace() for character in address
    ):
        raise ValueError(f"{name} must be one valid email address")
    return f"{local}@{domain.lower()}"


def _default_config() -> dict[str, Any]:
    return {
        "version": CONFIG_VERSION,
        "account_address": "",
        "imap_username": "",
        "default_from": "",
        "allowed_from": [],
        "display_name": "",
    }


def _validate_config(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise MailError("Saved iCloud Mail configuration must contain an object")
    allowed = {
        "version",
        "account_address",
        "imap_username",
        "default_from",
        "allowed_from",
        "display_name",
    }
    if set(payload) - allowed:
        raise MailError("Saved iCloud Mail configuration contains unsupported fields")
    if payload.get("version") != CONFIG_VERSION:
        raise MailError("Saved iCloud Mail configuration version is unsupported")
    try:
        account = _email_address(payload.get("account_address"), "account_address")
        imap_username = _text(
            payload.get("imap_username"), "imap_username", limit=320
        )
        if "\r" in imap_username or "\n" in imap_username:
            raise ValueError("imap_username is invalid")
        default_from = _email_address(
            payload.get("default_from") or account, "default_from"
        )
        raw_allowed = _list(payload.get("allowed_from"), "allowed_from", limit=50)
        aliases = [
            _email_address(value, "allowed_from", required=True)
            for value in raw_allowed
        ]
        display_name = _validated_display_name(
            _text(payload.get("display_name"), "display_name", limit=200),
            "display_name",
        )
    except ValueError as error:
        raise MailError(f"Saved iCloud Mail configuration is invalid: {error}") from None
    permitted = list(dict.fromkeys([account, *aliases]))
    if default_from not in permitted:
        raise MailError("Saved default_from must be account_address or allowed alias")
    return {
        "version": CONFIG_VERSION,
        "account_address": account,
        "imap_username": imap_username,
        "default_from": default_from,
        "allowed_from": [value for value in permitted if value != account],
        "display_name": display_name,
    }


def _load_config(*, required: bool = False) -> dict[str, Any]:
    path = _config_path()
    if not path.exists():
        legacy = os.environ.get("ICLOUD_MAIL_USERNAME", "").strip()
        if legacy:
            try:
                account = _email_address(legacy, "ICLOUD_MAIL_USERNAME")
                return _validate_config({
                    **_default_config(),
                    "account_address": account,
                    "imap_username": os.environ.get(
                        "ICLOUD_MAIL_IMAP_USERNAME", ""
                    ).strip(),
                    "default_from": account,
                    "display_name": os.environ.get(
                        "ICLOUD_MAIL_DISPLAY_NAME", ""
                    ).strip(),
                })
            except (MailError, ValueError) as error:
                raise MailError(
                    "iCloud Mail environment configuration "
                    "(ICLOUD_MAIL_USERNAME, ICLOUD_MAIL_IMAP_USERNAME, "
                    "ICLOUD_MAIL_DISPLAY_NAME) is invalid: "
                    f"{error}"
                ) from None
        if required:
            raise MailError(
                "iCloud Mail is not configured; run configure_account first"
            )
        return _default_config()
    try:
        metadata = path.lstat()
        if not stat.S_ISREG(metadata.st_mode) or path.is_symlink():
            raise MailError("Saved iCloud Mail configuration must be a regular file")
        if metadata.st_mode & 0o077:
            raise MailError(
                "Saved iCloud Mail configuration permissions must be user-only"
            )
        payload = json.loads(path.read_text(encoding="utf-8"))
    except MailError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise MailError(
            f"Could not read saved iCloud Mail configuration: {type(error).__name__}"
        ) from None
    return _validate_config(payload)


def _write_config(payload: dict[str, Any]) -> Path:
    config = _validate_config(payload)
    path = _config_path()
    parent_existed = path.parent.exists()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not parent_existed:
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass
    descriptor, temporary = tempfile.mkstemp(
        prefix=".config-", suffix=".json", dir=str(path.parent)
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(config, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_path, 0o600)
        os.replace(temporary_path, path)
    except Exception:
        try:
            temporary_path.unlink()
        except OSError:
            pass
        raise
    return path


def _text(value: Any, name: str, *, required: bool = False, limit: int = 10_000) -> str:
    if value is None and not required:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    value = value.strip()
    if required and not value:
        raise ValueError(f"{name} must not be empty")
    protocol_or_header_fields = {
        "mailbox",
        "query",
        "from",
        "to",
        "subject",
        "after",
        "before",
        "imap_username",
        "display_name",
        "_thread_reference_ids",
    }
    if len(value) > limit or (
        name in protocol_or_header_fields and ("\r" in value or "\n" in value)
    ):
        raise ValueError(f"{name} is invalid or too long")
    return value


def _body_text(value: Any, name: str, *, limit: int = MAX_BODY_CHARS) -> str:
    """Validate user-authored content without normalizing its whitespace."""

    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    if len(value) > limit:
        raise ValueError(f"{name} is invalid or too long")
    return value


def _decode_urlsafe_token(value: str, name: str) -> bytes:
    if not value or re.fullmatch(r"[A-Za-z0-9_-]+", value) is None:
        raise ValueError(f"{name} is malformed")
    try:
        decoded = base64.b64decode(
            value + "=" * (-len(value) % 4),
            altchars=b"-_",
            validate=True,
        )
    except (binascii.Error, ValueError, UnicodeError) as error:
        raise ValueError(f"{name} is malformed") from error
    canonical = base64.urlsafe_b64encode(decoded).decode().rstrip("=")
    if canonical != value:
        raise ValueError(f"{name} is malformed")
    return decoded


def _list(value: Any, name: str, *, limit: int = 100) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > limit:
        raise ValueError(f"{name} must be an array with at most {limit} entries")
    return value


def _decode_header(value: str | None) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except (LookupError, UnicodeError, email.errors.HeaderParseError):
        return value


def _addresses(value: str | None) -> list[dict[str, str]]:
    return [
        {"name": _decode_header(name), "address": address}
        for name, address in email.utils.getaddresses([value or ""])
        if address
    ]


def _validated_display_name(value: str, name: str) -> str:
    decoded = _decode_header(value)
    if re.search(r"[\x00-\x08\x0a-\x1f]", decoded):
        raise ValueError(f"{name} contains an invalid display name")
    return decoded


def _timeout() -> float:
    raw = os.environ.get("ICLOUD_MAIL_TIMEOUT", "30")
    try:
        value = float(raw)
    except ValueError as error:
        raise MailError("ICLOUD_MAIL_TIMEOUT must be a number") from error
    if not 5 <= value <= 120:
        raise MailError("ICLOUD_MAIL_TIMEOUT must be between 5 and 120 seconds")
    return value


def _username() -> str:
    return _load_config(required=True)["account_address"]


def _imap_username() -> str:
    return _imap_login_candidates()[0]


def _imap_login_candidates(config: dict[str, Any] | None = None) -> list[str]:
    config = config or _load_config(required=True)
    if config["imap_username"]:
        return [config["imap_username"]]
    account = config["account_address"]
    local_part = account.split("@", 1)[0]
    candidates = list(dict.fromkeys([local_part, account]))
    cached = _IMAP_LOGIN_CACHE.get(account)
    if cached in candidates:
        candidates.remove(cached)
        candidates.insert(0, cached)
    return candidates


def _password(username: str) -> tuple[str, str]:
    environment = os.environ.get("ICLOUD_MAIL_APP_PASSWORD")
    if environment:
        return environment, "environment"
    if sys.platform == "darwin":
        try:
            result = subprocess.run(
                [
                    "/usr/bin/security",
                    "find-generic-password",
                    "-a",
                    username,
                    "-s",
                    KEYCHAIN_SERVICE,
                    "-w",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            result = None
        if (
            result is not None
            and result.returncode == 0
            and result.stdout.rstrip("\n")
        ):
            return result.stdout.rstrip("\n"), "macOS Keychain"
    raise MailError(
        "No app-specific password found; store service codex-icloud-mail in "
        "macOS Keychain or set ICLOUD_MAIL_APP_PASSWORD"
    )


def _shutdown_imap(client: imaplib.IMAP4_SSL) -> None:
    try:
        client.shutdown()
    except Exception:
        pass


def _cleanup_smtp(
    client: smtplib.SMTP, deadline: OperationDeadline
) -> Exception | None:
    try:
        _set_socket_timeout(client, 15.0, deadline)
        client.quit()
    except Exception as error:
        try:
            client.close()
        except Exception:
            pass
        return error
    return None


@contextmanager
def _imap(
    *,
    socket_timeout: float | None = None,
    deadline: OperationDeadline | None = None,
) -> Iterator[imaplib.IMAP4_SSL]:
    deadline = deadline or _ACTIVE_DEADLINE.get()
    config = _load_config(required=True)
    username = config["account_address"]
    password, _ = _password(username)
    logins = _imap_login_candidates(config)
    explicit_override = bool(config["imap_username"])
    client: imaplib.IMAP4_SSL | None = None
    authenticated = False
    try:
        timeout_cap = min(_timeout(), socket_timeout) if socket_timeout is not None else _timeout()
        rejected: imaplib.IMAP4.error | None = None
        for index, login in enumerate(logins):
            authenticated = False
            client = imaplib.IMAP4_SSL(
                IMAP_HOST,
                IMAP_PORT,
                ssl_context=ssl.create_default_context(),
                timeout=deadline.timeout(timeout_cap) if deadline else timeout_cap,
            )
            try:
                if deadline is not None and getattr(client, "sock", None) is not None:
                    client.sock.settimeout(deadline.timeout(timeout_cap))
                client.login(login, password)
                authenticated = True
                client.__dict__["_codex_socket_timeout_cap"] = timeout_cap
                client.__dict__["_codex_imap_username_kind"] = (
                    "override"
                    if explicit_override
                    else "local_part"
                    if login == username.split("@", 1)[0]
                    else "full_address"
                )
                if not explicit_override:
                    _IMAP_LOGIN_CACHE[username] = login
                break
            except imaplib.IMAP4.abort:
                _shutdown_imap(client)
                client = None
                raise
            except MailError:
                _shutdown_imap(client)
                client = None
                raise
            except imaplib.IMAP4.error as error:
                rejected = error
                _shutdown_imap(client)
                client = None
            except (OSError, TimeoutError):
                _shutdown_imap(client)
                client = None
                raise
        else:
            if rejected is None:
                raise MailError("No valid iCloud IMAP login form is configured")
            raise rejected
        yield client
    except imaplib.IMAP4.abort as error:
        if client is not None:
            _shutdown_imap(client)
            client = None
        raise MailError(
            f"Could not connect to iCloud IMAP: {type(error).__name__}"
        ) from None
    except imaplib.IMAP4.error as error:
        raise MailError(f"iCloud IMAP rejected the request: {error}") from None
    except (OSError, TimeoutError) as error:
        if client is not None:
            _shutdown_imap(client)
            client = None
        raise MailError(f"Could not connect to iCloud IMAP: {type(error).__name__}") from None
    finally:
        if client is not None:
            client.__dict__.pop("_codex_selected_mailbox", None)
            client.__dict__.pop("_codex_selected_uidvalidity", None)
            if not authenticated:
                _shutdown_imap(client)
            else:
                try:
                    _set_socket_timeout(client, timeout_cap, deadline)
                    client.logout()
                except (imaplib.IMAP4.error, MailError, OSError, ValueError):
                    _shutdown_imap(client)
                finally:
                    client.__dict__.pop("_codex_socket_timeout_cap", None)


def _select(client: imaplib.IMAP4_SSL, mailbox: str, *, readonly: bool) -> int:
    selected = client.__dict__.get("_codex_selected_mailbox")
    if selected == (mailbox, readonly):
        return client.__dict__["_codex_selected_uidvalidity"]
    _set_socket_timeout(client, 25.0)
    status, data = client.select(_quoted_mailbox(mailbox), readonly=readonly)
    if status != "OK":
        raise MailError(f"Cannot open mailbox {mailbox!r}")
    response = client.response("UIDVALIDITY")[1]
    if not response or response[0] is None:
        raise MailError("Mailbox did not provide UIDVALIDITY")
    try:
        validity = int(response[0])
    except (TypeError, ValueError):
        raise MailError("Mailbox provided invalid UIDVALIDITY") from None
    client.__dict__["_codex_selected_mailbox"] = (mailbox, readonly)
    client.__dict__["_codex_selected_uidvalidity"] = validity
    return validity


def _encode_ref(mailbox: str, uidvalidity: int, uid: int) -> str:
    payload = json.dumps(
        {"m": mailbox, "v": uidvalidity, "u": uid},
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode()
    return REF_PREFIX + base64.urlsafe_b64encode(payload).decode().rstrip("=")


def _decode_ref(value: Any) -> tuple[str, int, int]:
    if not isinstance(value, str) or not value.startswith(REF_PREFIX):
        raise ValueError("message_id must be an iCloud Mail message identifier")
    try:
        encoded = value[len(REF_PREFIX) :]
        payload = json.loads(_decode_urlsafe_token(encoded, "message_id"))
    except (ValueError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("message_id is malformed") from error
    if (
        not isinstance(payload, dict)
        or set(payload) != {"m", "v", "u"}
        or not isinstance(payload["m"], str)
        or isinstance(payload["v"], bool)
        or not isinstance(payload["v"], int)
        or isinstance(payload["u"], bool)
        or not isinstance(payload["u"], int)
        or payload["v"] <= 0
        or payload["u"] <= 0
    ):
        raise ValueError("message_id is malformed")
    mailbox = _text(payload["m"], "mailbox", required=True, limit=500)
    return mailbox, payload["v"], payload["u"]


def _fetch_message(
    client: imaplib.IMAP4_SSL, mailbox: str, expected_validity: int, uid: int
) -> tuple[Message, bytes, str]:
    actual = _select(client, mailbox, readonly=True)
    if actual != expected_validity:
        raise MailError("Message identifier is stale because the mailbox changed")
    _set_socket_timeout(client, 120.0)
    status, size_data = client.uid("fetch", str(uid), "(RFC822.SIZE)")
    if status != "OK" or not any(item is not None for item in (size_data or [])):
        raise MailError("Message no longer exists in this mailbox")
    size_metadata = b""
    for item in size_data:
        if isinstance(item, bytes):
            size_metadata += item + b" "
        elif isinstance(item, tuple) and item and isinstance(item[0], bytes):
            size_metadata += item[0] + b" "
    size_matches = re.findall(
        rb"\bRFC822\.SIZE\s+(\d+)\b", size_metadata, flags=re.I
    )
    if len(size_matches) != 1:
        raise MailError("Could not determine message size before downloading it")
    if int(size_matches[0]) > MAX_MESSAGE_BYTES:
        raise MailError("Message exceeds the 20 MiB processing limit")
    _set_socket_timeout(client, 120.0)
    status, data = client.uid("fetch", str(uid), "(BODY.PEEK[] FLAGS)")
    if status != "OK" or not data or not isinstance(data[0], tuple):
        raise MailError("Message no longer exists in this mailbox")
    raw = data[0][1]
    if not isinstance(raw, bytes):
        raise MailError("Message body response was malformed")
    if len(raw) > MAX_MESSAGE_BYTES:
        raise MailError("Message exceeds the 20 MiB processing limit")
    _validate_summary_header_fields(_bounded_header_block(raw))
    metadata = b""
    for item in data:
        if isinstance(item, tuple):
            metadata += item[0] if isinstance(item[0], bytes) else b""
        elif isinstance(item, bytes):
            metadata += item
    flag_matches = re.findall(
        rb"(?:^|\s)FLAGS\s+\(([^)]*)\)", metadata, flags=re.I
    )
    flags_text = (
        flag_matches[-1].decode("ascii", errors="replace")
        if flag_matches
        else ""
    )
    message = _parse_full_message(raw)
    _validate_mime_depth(message)
    return message, raw, flags_text


def _parse_full_message(raw: bytes) -> Message:
    created = 0

    def bounded_factory(*args: Any, **kwargs: Any) -> EmailMessage:
        nonlocal created
        created += 1
        if created > MAX_MIME_PARTS:
            raise _MimePartLimitExceeded
        return EmailMessage(*args, **kwargs)

    policy = email.policy.default.clone(message_factory=bounded_factory)
    try:
        return email.message_from_bytes(raw, policy=policy)
    except _MimePartLimitExceeded:
        raise MailError(
            f"Message contains more than {MAX_MIME_PARTS} MIME parts"
        ) from None
    except RecursionError:
        raise MailError(
            "Message MIME structure exceeds the supported depth"
        ) from None


def _body(message: Message) -> tuple[str, str]:
    plain = ""
    html = ""
    pending = [message]
    while pending:
        part = pending.pop(0)
        if (
            part.get_content_disposition() == "attachment"
            or part.get_filename() is not None
        ):
            continue
        if part.get_content_type() == "message/rfc822":
            if part is message:
                pending[0:0] = list(part.iter_parts())
            continue
        if part.is_multipart():
            pending[0:0] = list(part.iter_parts())
            continue
        kind = part.get_content_type()
        if kind not in {"text/plain", "text/html"}:
            continue
        try:
            value = part.get_content()
        except (LookupError, UnicodeError):
            payload = part.get_payload(decode=True) or b""
            value = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
        if kind == "text/plain" and not plain:
            plain = str(value)
        elif kind == "text/html" and not html:
            html = str(value)
    return plain[:MAX_BODY_CHARS], html[:MAX_BODY_CHARS]


def _attachment_payload(part: Message) -> bytes:
    payload = part.get_payload(decode=True)
    if isinstance(payload, bytes):
        return payload
    if part.is_multipart() and part.get_content_type() != "message/rfc822":
        return part.as_bytes(policy=email.policy.default)
    if part.get_content_type() == "message/rfc822":
        nested = part.get_payload()
        if isinstance(nested, list):
            return b"".join(
                item.as_bytes(policy=email.policy.default)
                for item in nested
                if isinstance(item, Message)
            )
        if isinstance(nested, Message):
            return nested.as_bytes(policy=email.policy.default)
    return b""


class _ByteCounter:
    def __init__(self) -> None:
        self.count = 0

    def write(self, value: bytes) -> int:
        self.count += len(value)
        return len(value)

    def flush(self) -> None:
        return None


def _serialized_size(message: Message) -> int:
    _validate_mime_depth(message)
    counter = _ByteCounter()
    email.generator.BytesGenerator(
        counter, policy=email.policy.default
    ).flatten(message)
    return counter.count


def _raw_payload_size(payload: str | bytes) -> int:
    if isinstance(payload, bytes):
        return len(payload)
    return sum(
        1
        if ord(character) <= 0xFF or 0xDC80 <= ord(character) <= 0xDCFF
        else 6
        if ord(character) <= 0xFFFF
        else 10
        for character in payload
    )


def _quoted_printable_size(payload: str | bytes) -> int:
    size = 0
    position = 0
    while position < len(payload):
        character = payload[position : position + 1]
        if character in ("=", b"="):
            following = payload[position + 1 : position + 3]
            if following in ("\r\n", b"\r\n"):
                position += 3
                continue
            if payload[position + 1 : position + 2] in ("\n", b"\n"):
                position += 2
                continue
            if len(following) == 2 and all(
                ord("0") <= (item if isinstance(item, int) else ord(item)) <= ord("9")
                or ord("A") <= (item if isinstance(item, int) else ord(item)) <= ord("F")
                or ord("a") <= (item if isinstance(item, int) else ord(item)) <= ord("f")
                for item in following
            ):
                size += 1
                position += 3
                continue
            return _raw_payload_size(payload)
        size += _raw_payload_size(character)
        position += 1
    return size


def _attachment_payload_size(part: Message) -> int:
    if part.is_multipart() and part.get_content_type() != "message/rfc822":
        return _serialized_size(part)
    if part.get_content_type() == "message/rfc822":
        nested = part.get_payload()
        if isinstance(nested, list):
            return sum(
                _serialized_size(item) for item in nested if isinstance(item, Message)
            )
        if isinstance(nested, Message):
            return _serialized_size(nested)
        return 0
    # Message.get_payload() applies policy replacement to raw 8-bit text.
    # The parser-owned payload retains surrogateescaped source octets for counting.
    payload = getattr(part, "_payload", None)
    if not isinstance(payload, (str, bytes)):
        payload = part.get_payload()
    if not isinstance(payload, (str, bytes)):
        return 0
    encoding = (part.get("Content-Transfer-Encoding") or "").lower()
    if encoding == "base64":
        symbols = 0
        padding = 0
        seen_padding = False
        malformed = False
        for character in payload:
            codepoint = character if isinstance(character, int) else ord(character)
            if codepoint in (ord(" "), ord("\t"), ord("\r"), ord("\n")):
                continue
            if (
                ord("A") <= codepoint <= ord("Z")
                or ord("a") <= codepoint <= ord("z")
                or ord("0") <= codepoint <= ord("9")
                or codepoint in (ord("+"), ord("/"))
            ):
                if seen_padding:
                    malformed = True
                symbols += 1
            elif codepoint == ord("="):
                seen_padding = True
                padding += 1
            else:
                malformed = True
        invalid_shape = (
            padding > 2
            or padding > 0
            and (symbols + padding) % 4 != 0
            or padding == 0
            and symbols % 4 == 1
        )
        if invalid_shape or malformed:
            return _raw_payload_size(payload)
        return symbols * 6 // 8
    if encoding == "quoted-printable":
        return _quoted_printable_size(payload)
    return _raw_payload_size(payload)


def _iter_message_parts(message: Message) -> Iterator[tuple[Message, int]]:
    pending = [(message, 0)]
    visited = 0
    while pending:
        part, depth = pending.pop()
        visited += 1
        if visited > MAX_MIME_PARTS:
            raise MailError(f"Message contains more than {MAX_MIME_PARTS} MIME parts")
        if depth > MAX_MIME_DEPTH:
            raise MailError("Message MIME structure exceeds the supported depth")
        yield part, depth
        if part.is_multipart():
            children = list(part.iter_parts())
            pending.extend((child, depth + 1) for child in reversed(children))


def _validate_mime_depth(message: Message) -> None:
    for _part, _depth in _iter_message_parts(message):
        pass


def _attachment_parts(message: Message) -> Iterator[Message]:
    pending = [(message, 0)]
    visited = 0
    while pending:
        part, depth = pending.pop()
        visited += 1
        if visited > MAX_MIME_PARTS:
            raise MailError(f"Message contains more than {MAX_MIME_PARTS} MIME parts")
        if depth > MAX_MIME_DEPTH:
            raise MailError("Message MIME structure exceeds the supported depth")
        filename = _decode_header(part.get_filename())
        if (
            filename
            or part.get_content_disposition() == "attachment"
            or (depth > 0 and part.get_content_type() == "message/rfc822")
        ):
            yield part
        elif part.is_multipart():
            children = list(part.iter_parts())
            pending.extend((child, depth + 1) for child in reversed(children))


def _attachment_entries(message: Message, message_id: str) -> list[dict[str, Any]]:
    entries = []
    walk_indices = {
        id(part): index
        for index, (part, _depth) in enumerate(_iter_message_parts(message))
    }
    for part in _attachment_parts(message):
        if len(entries) >= MAX_INCOMING_ATTACHMENTS:
            raise MailError(
                f"Message contains more than {MAX_INCOMING_ATTACHMENTS} attachments"
            )
        index = walk_indices[id(part)]
        filename = _decode_header(part.get_filename())
        size = _attachment_payload_size(part)
        token = base64.urlsafe_b64encode(str(index).encode()).decode().rstrip("=")
        entries.append(
            {
                "attachment_id": f"{message_id}.{token}",
                "filename": filename or f"attachment-{index}",
                "content_type": part.get_content_type(),
                "size": size,
                "read_supported": size <= MAX_ATTACHMENT_BYTES,
            }
        )
    return entries


def _summary(
    message: Message,
    message_id: str,
    flags: str = "",
    *,
    attachments: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    fields = _bounded_summary_fields(message)
    plain, _ = _body(message)
    attachments = (
        _attachment_entries(message, message_id)
        if attachments is None
        else attachments
    )
    return {
        "id": message_id,
        "internet_message_id": fields["internet_message_id"],
        "subject": fields["subject"],
        "from": fields["from"],
        "to": fields["to"],
        "cc": fields["cc"],
        "bcc": fields["bcc"],
        "date": fields["date"],
        "unread": "\\Seen" not in flags,
        "flagged": "\\Flagged" in flags,
        "has_attachments": bool(attachments),
        "snippet": re.sub(r"\s+", " ", plain).strip()[:300],
    }


def _fetch_summary(
    client: imaplib.IMAP4_SSL,
    mailbox: str,
    expected_validity: int,
    uid: int,
) -> dict[str, Any]:
    actual = _select(client, mailbox, readonly=True)
    if actual != expected_validity:
        raise MailError("Message identifier is stale because the mailbox changed")
    status, data = client.uid(
        "FETCH",
        str(uid),
        (
            "(BODY.PEEK[HEADER.FIELDS "
            "(MESSAGE-ID SUBJECT FROM TO CC BCC DATE REFERENCES IN-REPLY-TO)]"
            f"<0.{MAX_SUMMARY_HEADER_BYTES + 1}> "
            "BODYSTRUCTURE FLAGS)"
        ),
    )
    if status != "OK" or not data:
        raise MailError("Message no longer exists in this mailbox")
    headers = bytearray()
    metadata = bytearray()

    def append_checked(target: bytearray, fragment: Any, limit: int) -> None:
        if not isinstance(fragment, bytes):
            return
        if len(target) + len(fragment) > limit:
            raise SummaryTooLarge("Message summary exceeds the processing limit")
        target.extend(fragment)

    for item in data:
        if isinstance(item, tuple):
            append_checked(metadata, item[0], MAX_SUMMARY_METADATA_BYTES)
            append_checked(headers, item[1], MAX_SUMMARY_HEADER_BYTES)
        elif isinstance(item, bytes):
            append_checked(metadata, item, MAX_SUMMARY_METADATA_BYTES)
    if not headers:
        raise MailError("Message no longer exists in this mailbox")
    header_bytes = bytes(headers)
    metadata_bytes = bytes(metadata)
    _validate_summary_header_fields(header_bytes)
    message = email.message_from_bytes(header_bytes, policy=email.policy.default)
    flag_matches = re.findall(
        rb"(?:^|\s)FLAGS\s+\(([^)]*)\)", metadata_bytes, flags=re.I
    )
    flags = (
        flag_matches[-1].decode("ascii", errors="replace")
        if flag_matches
        else ""
    )
    message_id = _encode_ref(mailbox, expected_validity, uid)
    fields = _bounded_summary_fields(message)
    return {
        "id": message_id,
        "internet_message_id": fields["internet_message_id"],
        "subject": fields["subject"],
        "from": fields["from"],
        "to": fields["to"],
        "cc": fields["cc"],
        "bcc": fields["bcc"],
        "date": fields["date"],
        "in_reply_to": fields["in_reply_to"],
        "unread": "\\Seen" not in flags,
        "flagged": "\\Flagged" in flags,
        "has_attachments": _bodystructure_has_attachment(metadata_bytes),
        "snippet": "",
        "references": fields["references"],
    }


def _bounded_header_block(raw: bytes) -> bytes:
    endings = [
        position + len(separator)
        for separator in (b"\r\n\r\n", b"\n\n")
        if (position := raw.find(separator, 0, MAX_SUMMARY_HEADER_BYTES + 5)) >= 0
    ]
    end = min(endings) if endings else len(raw)
    if end > MAX_SUMMARY_HEADER_BYTES:
        raise SummaryTooLarge("Message summary exceeds the processing limit")
    return raw[:end]


def _bounded_summary_fields(message: Message) -> dict[str, Any]:
    addresses = {
        name: _addresses(message.get(name.replace("_", "-").title()))
        for name in ("from", "to", "cc", "bcc", "reply_to")
    }
    if sum(len(values) for values in addresses.values()) > MAX_SUMMARY_ADDRESSES:
        raise SummaryTooLarge("Message summary exceeds the processing limit")
    scalars = {
        "internet_message_id": str(message.get("Message-ID", "")),
        "subject": _decode_header(message.get("Subject")),
        "date": str(message.get("Date", "")),
        "in_reply_to": str(message.get("In-Reply-To", "")),
    }
    if any(len(value) > MAX_SUMMARY_SCALAR_CHARS for value in scalars.values()):
        raise SummaryTooLarge("Message summary exceeds the processing limit")
    references = str(message.get("References", "")).split()
    if len(references) > MAX_SUMMARY_REFERENCES:
        raise SummaryTooLarge("Message summary exceeds the processing limit")
    return {**scalars, **addresses, "references": references}


def _validate_summary_header_fields(headers: bytes) -> None:
    """Reject compact headers that expand into unbounded summary objects."""
    parsed = BytesHeaderParser(policy=email.policy.compat32).parsebytes(headers)
    address_chars = 0
    address_count = 0
    reference_chars = 0
    reference_count = 0
    scalar_chars: dict[str, int] = {}
    address_names = {"from", "to", "cc", "bcc", "reply-to"}
    reference_names = {"references", "in-reply-to"}
    scalar_names = {"message-id", "subject", "date"}
    for raw_name, raw_value in parsed.raw_items():
        name = raw_name.lower()
        value = str(raw_value)
        if name in address_names:
            address_chars += len(value)
            if value.strip():
                address_count += 1 + value.count(",") + value.count(";")
        elif name in reference_names:
            reference_chars += len(value)
            in_token = False
            for character in value:
                if character.isspace():
                    in_token = False
                elif not in_token:
                    reference_count += 1
                    in_token = True
        elif name in scalar_names:
            scalar_chars[name] = scalar_chars.get(name, 0) + len(value)
    if (
        address_chars > MAX_SUMMARY_ADDRESS_CHARS
        or address_count > MAX_SUMMARY_ADDRESSES
        or reference_chars > MAX_SUMMARY_REFERENCE_CHARS
        or reference_count > MAX_SUMMARY_REFERENCES
        or any(value > MAX_SUMMARY_SCALAR_CHARS for value in scalar_chars.values())
    ):
        raise SummaryTooLarge("Message summary exceeds the processing limit")


def _bodystructure_has_attachment(metadata: bytes) -> bool:
    match = re.search(rb"\bBODYSTRUCTURE\b", metadata, flags=re.I)
    if not match:
        return False

    def parse(position: int, depth: int = 0) -> tuple[Any, int]:
        if depth > MAX_BODYSTRUCTURE_DEPTH:
            raise ValueError
        while position < len(metadata) and metadata[position:position + 1].isspace():
            position += 1
        if position >= len(metadata):
            raise ValueError
        if metadata[position:position + 1] == b"(":
            values = []
            position += 1
            while True:
                while position < len(metadata) and metadata[position:position + 1].isspace():
                    position += 1
                if position >= len(metadata):
                    raise ValueError
                if metadata[position:position + 1] == b")":
                    return values, position + 1
                value, position = parse(position, depth + 1)
                values.append(value)
        if metadata[position:position + 1] == b'"':
            position += 1
            value = bytearray()
            while position < len(metadata):
                character = metadata[position:position + 1]
                position += 1
                if character == b'"':
                    return bytes(value), position
                if character == b"\\" and position < len(metadata):
                    character = metadata[position:position + 1]
                    position += 1
                value.extend(character)
            raise ValueError
        end = position
        while end < len(metadata) and not metadata[end:end + 1].isspace() and metadata[end:end + 1] not in {b"(", b")"}:
            end += 1
        atom = metadata[position:end]
        return (None if atom.upper() == b"NIL" else atom), end

    def contains_attachment(
        node: Any, *, is_root: bool = False, depth: int = 0
    ) -> bool:
        if depth > MAX_BODYSTRUCTURE_DEPTH:
            raise ValueError
        if not isinstance(node, list):
            return False

        def has_filename(parameters: Any) -> bool:
            return isinstance(parameters, list) and any(
                isinstance(parameters[index], bytes)
                and re.fullmatch(
                    rb"(?:NAME|FILENAME)(?:\*|\*\d+\*?)?",
                    parameters[index],
                    flags=re.I,
                )
                is not None
                for index in range(0, len(parameters) - 1, 2)
            )

        def has_disposition(value: Any) -> bool:
            if not isinstance(value, list) or not value:
                return False
            disposition = value[0].upper() if isinstance(value[0], bytes) else b""
            if disposition == b"ATTACHMENT":
                return True
            if disposition == b"INLINE" and len(value) > 1 and has_filename(value[1]):
                return True
            return False

        if node and isinstance(node[0], list):
            child_count = 0
            while child_count < len(node) and isinstance(node[child_count], list):
                if contains_attachment(node[child_count], depth=depth + 1):
                    return True
                child_count += 1
            parameters_index = child_count + 1
            if (
                parameters_index < len(node)
                and has_filename(node[parameters_index])
            ):
                return True
            disposition_index = child_count + 2
            return (
                disposition_index < len(node)
                and has_disposition(node[disposition_index])
            )

        if len(node) < 2 or not all(
            isinstance(node[index], bytes) for index in (0, 1)
        ):
            return False
        maintype = node[0].upper()
        subtype = node[1].upper()
        if len(node) > 2 and has_filename(node[2]):
            return True
        if not is_root and maintype == b"MESSAGE" and subtype == b"RFC822":
            return True
        if maintype == b"TEXT":
            disposition_index = 9
        elif maintype == b"MESSAGE" and subtype == b"RFC822":
            disposition_index = 11
        else:
            disposition_index = 8
        if disposition_index < len(node) and has_disposition(
            node[disposition_index]
        ):
            return True
        return (
            maintype == b"MESSAGE"
            and subtype == b"RFC822"
            and len(node) > 8
            and contains_attachment(node[8], is_root=False, depth=depth + 1)
        )

    try:
        structure, _ = parse(match.end())
        return contains_attachment(structure, is_root=True)
    except (RecursionError, ValueError):
        return False


def get_account_status(arguments: dict[str, Any]) -> dict[str, Any]:
    if arguments:
        raise ValueError("get_account_status takes no arguments")
    config = _load_config()
    username = config["account_address"]
    source = None
    credential_configured = False
    if username:
        try:
            _, source = _password(username)
            credential_configured = True
        except MailError:
            pass
    return {
        "configured": bool(username and credential_configured),
        "account_configured": bool(username),
        "credential_configured": credential_configured,
        "account_address": username or None,
        "imap_username_override": config["imap_username"] or None,
        "default_from": config["default_from"] or None,
        "allowed_from": config["allowed_from"],
        "display_name": config["display_name"] or None,
        "incoming_alias_scope": "all aliases in the iCloud mailbox",
        "credential_source": source,
        "config_path": str(_config_path()),
        "imap": f"{IMAP_HOST}:{IMAP_PORT} TLS",
        "smtp": f"{SMTP_HOST}:{SMTP_PORT} STARTTLS",
        "network_checked": False,
    }


def configure_account(arguments: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "account_address",
        "imap_username",
        "default_from",
        "allowed_from",
        "display_name",
    }
    unknown = set(arguments) - allowed
    if unknown:
        raise ValueError(f"unsupported configure_account fields: {sorted(unknown)}")
    account = _email_address(
        arguments.get("account_address"), "account_address", required=True
    )
    raw_aliases = arguments.get("allowed_from")
    if isinstance(raw_aliases, str):
        raw_aliases = [
            value.strip() for value in raw_aliases.split(",") if value.strip()
        ]
    aliases = [
        _email_address(value, "allowed_from")
        for value in _list(raw_aliases, "allowed_from", limit=50)
    ]
    aliases = list(dict.fromkeys(value for value in aliases if value != account))
    default_from = _email_address(
        arguments.get("default_from") or account, "default_from"
    )
    if default_from not in {account, *aliases}:
        raise ValueError("default_from must be account_address or an allowed alias")
    imap_username = _text(
        arguments.get("imap_username"), "imap_username", limit=320
    )
    if "\r" in imap_username or "\n" in imap_username:
        raise ValueError("imap_username is invalid")
    display_name = _validated_display_name(
        _text(arguments.get("display_name"), "display_name", limit=200),
        "display_name",
    )
    path = _write_config(
        {
            "version": CONFIG_VERSION,
            "account_address": account,
            "imap_username": imap_username,
            "default_from": default_from,
            "allowed_from": aliases,
            "display_name": display_name,
        }
    )
    return {
        "status": "configured",
        "account_address": account,
        "default_from": default_from,
        "allowed_from": aliases,
        "incoming_alias_scope": "all aliases in the iCloud mailbox",
        "config_path": str(path),
        "credential_stored": False,
        "next_step": (
            "Store an Apple app-specific password in macOS Keychain, then call "
            "validate_account."
            if sys.platform == "darwin"
            else "Persist ICLOUD_MAIL_APP_PASSWORD in the environment that launches "
            "Codex, then call validate_account."
        ),
    }


def clear_account_configuration(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"confirm"} or arguments.get("confirm") is not True:
        raise ValueError("clear_account_configuration requires confirm=true")
    path = _config_path()
    removed = False
    if path.exists():
        if path.is_symlink() or not stat.S_ISREG(path.lstat().st_mode):
            raise MailError("Refusing to remove a non-regular configuration path")
        path.unlink()
        removed = True
    return {
        "status": "cleared",
        "configuration_removed": removed,
        "keychain_credential_removed": False,
        "note": "Keychain credential is intentionally preserved.",
    }


def validate_account(arguments: dict[str, Any]) -> dict[str, Any]:
    if arguments:
        raise ValueError("validate_account takes no arguments")
    deadline = _current_deadline()
    with _imap(deadline=deadline) as client:
        _set_socket_timeout(client, _timeout(), deadline)
        status, data = client.status("INBOX", "(MESSAGES)")
        if status != "OK":
            raise MailError("iCloud IMAP login succeeded but INBOX status failed")
        first = data[0] if data else None
        mailbox_status = (
            first.decode("ascii", errors="replace")
            if isinstance(first, bytes)
            else ""
        )
        imap_login_kind = client.__dict__.get(
            "_codex_imap_username_kind", "override"
        )
    username = _username()
    password, _ = _password(username)
    client: smtplib.SMTP | None = None
    try:
        client = smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT,
            timeout=deadline.timeout(_timeout()),
        )
        if getattr(client, "sock", None) is not None:
            _set_socket_timeout(client, _timeout(), deadline)
        client.ehlo()
        if getattr(client, "sock", None) is not None:
            _set_socket_timeout(client, _timeout(), deadline)
        client.starttls(context=ssl.create_default_context())
        if getattr(client, "sock", None) is not None:
            _set_socket_timeout(client, _timeout(), deadline)
        client.ehlo()
        if getattr(client, "sock", None) is not None:
            _set_socket_timeout(client, _timeout(), deadline)
        client.login(username, password)
    except smtplib.SMTPException as error:
        raise MailError(
            f"iCloud SMTP authentication failed: {type(error).__name__}"
        ) from None
    except (OSError, TimeoutError) as error:
        raise MailError(
            f"Could not connect to iCloud SMTP: {type(error).__name__}"
        ) from None
    finally:
        if client is not None:
            _cleanup_smtp(client, deadline)
    match = re.search(r"MESSAGES (\d+)", mailbox_status)
    return {
        "status": "validated",
        "account_address": username,
        "imap_authenticated": True,
        "imap_username_form": imap_login_kind,
        "smtp_authenticated": True,
        "inbox_messages": int(match.group(1)) if match else None,
        "email_sent": False,
    }


def _open_macos(arguments: dict[str, Any], target: str, label: str) -> dict[str, Any]:
    if arguments:
        raise ValueError(f"{label} takes no arguments")
    if sys.platform != "darwin":
        raise MailError(f"{label} is available only on macOS")
    try:
        subprocess.run(
            ["/usr/bin/open", target],
            check=True,
            capture_output=True,
            env={
                key: value
                for key, value in os.environ.items()
                if key != "ICLOUD_MAIL_APP_PASSWORD"
            },
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        raise MailError(f"Could not open {label}") from None
    return {"status": "opened", "target": label}


def open_apple_password_page(arguments: dict[str, Any]) -> dict[str, Any]:
    return _open_macos(
        arguments, "https://account.apple.com/account/manage", "Apple Account"
    )


def open_keychain_access(arguments: dict[str, Any]) -> dict[str, Any]:
    account = _load_config(required=True)["account_address"]
    result = _open_macos(
        arguments,
        "/System/Applications/Utilities/Keychain Access.app",
        "Keychain Access",
    )
    result["instructions"] = {
        "keychain_item_name": KEYCHAIN_SERVICE,
        "account_name": account,
        "password_value": "Apple app-specific password",
    }
    return result


def _mailboxes(
    client: imaplib.IMAP4_SSL, *, limit: int | None = None
) -> tuple[list[dict[str, Any]], bool]:
    _set_socket_timeout(client, 25.0)
    status, data = client.list()
    if status != "OK":
        raise MailError("Could not list iCloud Mail mailboxes")
    result: list[dict[str, Any]] = []
    incomplete = False
    examined_bytes = 0
    pattern = re.compile(
        rb'^\((?P<flags>[^)]*)\) (?:"(?P<delimiter>[^"]*)"|NIL) (?P<name>.+)$'
    )
    for index, raw in enumerate(data or []):
        if index >= MAX_MAILBOX_SCAN_ENTRIES:
            incomplete = True
            break
        if not raw:
            incomplete = True
            continue
        was_tuple = isinstance(raw, tuple)
        if was_tuple:
            parts = [item for item in raw if isinstance(item, bytes)]
            raw_size = sum(len(item) for item in parts) + max(0, len(parts) - 1)
            if not parts:
                incomplete = True
                continue
            if examined_bytes + raw_size > MAX_MAILBOX_SCAN_BYTES:
                incomplete = True
                break
            examined_bytes += raw_size
            if raw_size > MAX_MAILBOX_ENTRY_BYTES:
                incomplete = True
                continue
            raw = b" ".join(parts)
        if not isinstance(raw, bytes):
            incomplete = True
            continue
        if not was_tuple:
            raw_size = len(raw)
            if examined_bytes + raw_size > MAX_MAILBOX_SCAN_BYTES:
                incomplete = True
                break
            examined_bytes += raw_size
            if raw_size > MAX_MAILBOX_ENTRY_BYTES:
                incomplete = True
                continue
        match = pattern.match(raw)
        if not match:
            incomplete = True
            continue
        name_raw = match.group("name").strip()
        name_raw = re.sub(rb"^\{\d+\}\s*", b"", name_raw)
        if name_raw.startswith(b'"') and name_raw.endswith(b'"'):
            name_raw = name_raw[1:-1].replace(b'\\"', b'"').replace(b"\\\\", b"\\")
        name = _decode_imap_utf7(name_raw)
        flags = match.group("flags").decode("ascii", errors="replace").split()
        if (
            len(name) > MAX_MAILBOX_NAME_CHARS
            or len(flags) > MAX_MAILBOX_FLAGS
            or sum(len(value) for value in flags) > MAX_MAILBOX_FLAG_CHARS
        ):
            incomplete = True
            continue
        result.append({"name": name, "flags": flags})
        if limit is not None and len(result) > limit:
            incomplete = True
            break
    return result, incomplete


def list_mailboxes(arguments: dict[str, Any]) -> dict[str, Any]:
    if arguments:
        raise ValueError("list_mailboxes takes no arguments")
    with _imap(socket_timeout=4.0) as client:
        mailboxes, truncated = _mailboxes(client, limit=MAX_MAILBOX_RESULTS)
        mailboxes = mailboxes[:MAX_MAILBOX_RESULTS]
        bounded_mailboxes: list[dict[str, Any]] = []
        for index, item in enumerate(mailboxes):
            if index >= MAX_MAILBOX_STATUS:
                item["messages"] = None
                item["unread"] = None
                continue
            _set_socket_timeout(client, 4.0)
            status, data = client.status(
                _quoted_mailbox(item["name"]), "(MESSAGES UNSEEN)"
            )
            first = data[0] if status == "OK" and data else None
            text = (
                first.decode("ascii", errors="replace")
                if isinstance(first, bytes)
                else ""
            )
            counts = dict(re.findall(r"(MESSAGES|UNSEEN) (\d+)", text))
            item["messages"] = (
                int(counts["MESSAGES"]) if "MESSAGES" in counts else None
            )
            item["unread"] = (
                int(counts["UNSEEN"]) if "UNSEEN" in counts else None
            )
            candidate = {
                "mailboxes": bounded_mailboxes + [item],
                "truncated": False,
            }
            if (
                len(json.dumps(candidate, ensure_ascii=False).encode("utf-8"))
                > MAX_MAILBOX_OUTPUT_BYTES
            ):
                truncated = True
                break
            bounded_mailboxes.append(item)
        return {"mailboxes": bounded_mailboxes, "truncated": truncated}


def _quoted(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _quoted_mailbox(value: str) -> str:
    return _quoted(_encode_imap_utf7(value))


def _encode_imap_utf7(value: str) -> str:
    """Encode a Unicode mailbox name using RFC 3501 modified UTF-7."""
    output: list[str] = []
    non_ascii: list[str] = []

    def flush() -> None:
        if not non_ascii:
            return
        encoded = base64.b64encode("".join(non_ascii).encode("utf-16-be"))
        output.append("&" + encoded.decode("ascii").rstrip("=").replace("/", ",") + "-")
        non_ascii.clear()

    for character in value:
        if "\x20" <= character <= "\x7e":
            flush()
            output.append("&-" if character == "&" else character)
        else:
            non_ascii.append(character)
    flush()
    return "".join(output)


def _decode_imap_utf7(value: bytes) -> str:
    """Decode RFC 3501 modified UTF-7 mailbox names without dependencies."""
    output: list[str] = []
    position = 0
    while position < len(value):
        ampersand = value.find(b"&", position)
        if ampersand < 0:
            output.append(value[position:].decode("ascii", errors="replace"))
            break
        output.append(value[position:ampersand].decode("ascii", errors="replace"))
        hyphen = value.find(b"-", ampersand)
        if hyphen < 0:
            output.append(value[ampersand:].decode("ascii", errors="replace"))
            break
        encoded = value[ampersand + 1 : hyphen]
        if not encoded:
            output.append("&")
        else:
            try:
                padded = encoded.replace(b",", b"/") + b"=" * (-len(encoded) % 4)
                output.append(base64.b64decode(padded).decode("utf-16-be"))
            except (binascii.Error, UnicodeError):
                output.append(value[ampersand : hyphen + 1].decode("ascii", errors="replace"))
        position = hyphen + 1
    return "".join(output)


def search_emails(
    arguments: dict[str, Any],
    *,
    socket_timeout: float | None = 5.0,
    deadline: OperationDeadline | None = None,
    client: imaplib.IMAP4_SSL | None = None,
) -> dict[str, Any]:
    allowed = {
        "mailbox", "query", "from", "to", "subject", "after", "before",
        "unread", "flagged", "has_attachment", "max_results",
        "_thread_reference_ids",
    }
    unknown = set(arguments) - allowed
    if unknown:
        raise ValueError(f"unsupported search fields: {sorted(unknown)}")
    mailbox = _text(arguments.get("mailbox", "INBOX"), "mailbox", required=True, limit=500)
    maximum = arguments.get("max_results", 20)
    if isinstance(maximum, bool) or not isinstance(maximum, int) or not 1 <= maximum <= MAX_RESULTS:
        raise ValueError(f"max_results must be between 1 and {MAX_RESULTS}")
    for field in ("unread", "flagged", "has_attachment"):
        if arguments.get(field) is not None and not isinstance(arguments[field], bool):
            raise ValueError(f"{field} must be a boolean")
    criteria: list[str] = ["ALL"]
    mapping = {"query": "TEXT", "from": "FROM", "to": "TO", "subject": "SUBJECT"}
    for field, atom in mapping.items():
        value = _text(arguments.get(field), field, limit=500)
        if value:
            criteria.extend([atom, _quoted(value)])
    for field, atom in (("after", "SINCE"), ("before", "BEFORE")):
        value = _text(arguments.get(field), field, limit=10)
        if value:
            try:
                parsed = dt.date.fromisoformat(value)
            except ValueError as error:
                raise ValueError(f"{field} must use YYYY-MM-DD") from error
            criteria.extend([atom, parsed.strftime("%d-%b-%Y")])
    if arguments.get("unread") is True:
        criteria.append("UNSEEN")
    elif arguments.get("unread") is False:
        criteria.append("SEEN")
    if arguments.get("flagged") is True:
        criteria.append("FLAGGED")
    elif arguments.get("flagged") is False:
        criteria.append("UNFLAGGED")
    imap_options: dict[str, Any] = {"socket_timeout": socket_timeout}
    if deadline is not None:
        imap_options["deadline"] = deadline
    connection = _imap(**imap_options) if client is None else nullcontext(client)
    with connection as client:
        validity = _select(client, mailbox, readonly=True)
        thread_reference_ids = _list(
            arguments.get("_thread_reference_ids", []),
            "_thread_reference_ids",
            limit=10,
        )
        if thread_reference_ids:
            _set_socket_timeout(client, 10.0, deadline)
            matched_uids: set[int] = set()
            for reference_id in thread_reference_ids:
                _set_socket_timeout(client, 10.0, deadline)
                value = _text(
                    reference_id, "_thread_reference_ids", required=True, limit=500
                )
                status, data = client.uid("search", None, "TEXT", _quoted(value))
                if status != "OK":
                    raise MailError("iCloud Mail thread search failed")
                matched_uids.update(
                    int(item)
                    for item in (data[0].split() if data and data[0] else [])
                )
            uids = sorted(matched_uids)
        else:
            charset = "UTF-8" if any(not item.isascii() for item in criteria) else None
            wire_criteria: list[str | bytes] = (
                [item.encode("utf-8") for item in criteria] if charset else criteria
            )
            status, data = client.uid("search", charset, *wire_criteria)
            if status != "OK":
                raise MailError("iCloud Mail search failed")
            uids = [
                int(item)
                for item in (data[0].split() if data and data[0] else [])
            ]
        uids.reverse()
        results = []
        scanned = 0
        skipped_oversized = 0
        scan_limit = min(
            len(uids), MAX_SEARCH_SCAN, max(maximum * 5, MAX_RESULTS)
        )
        for uid in uids[:scan_limit]:
            if len(results) >= maximum:
                break
            scanned += 1
            try:
                _set_socket_timeout(client, 5.0, deadline)
                item = _fetch_summary(client, mailbox, validity, uid)
            except SummaryTooLarge:
                skipped_oversized += 1
                continue
            except MailError as error:
                if str(error) == "Message no longer exists in this mailbox":
                    continue
                raise
            if arguments.get("has_attachment") is not None and (
                item["has_attachments"] is not arguments["has_attachment"]
            ):
                continue
            results.append(item)
        result = {
            "emails": results,
            "mailbox": mailbox,
            "returned": len(results),
            "matched_before_attachment_filter": len(uids),
            "scanned": scanned,
            "truncated": scanned < len(uids) or skipped_oversized > 0,
        }
        if skipped_oversized:
            result["skipped_oversized_summaries"] = skipped_oversized
        return result


def _read_email_result(
    message: Message,
    raw: bytes,
    flags: str,
    message_id: str,
    mailbox: str,
    *,
    include_raw_mime: bool = False,
) -> dict[str, Any]:
    plain, html = _body(message)
    attachments = _attachment_entries(message, message_id)
    fields = _bounded_summary_fields(message)
    result = _summary(message, message_id, flags, attachments=attachments)
    result.update(
        {
            "mailbox": mailbox,
            "body_text": plain,
            "body_html": html,
            "reply_to": fields["reply_to"],
            "attachments": attachments,
            "references": fields["references"],
            "in_reply_to": fields["in_reply_to"],
        }
    )
    if include_raw_mime:
        if len(raw) > MAX_ATTACHMENT_BYTES:
            raise MailError("Raw MIME exceeds the 5 MiB result limit")
        result["raw_mime_base64"] = base64.b64encode(raw).decode()
    return result


def read_email(
    arguments: dict[str, Any],
    *,
    deadline: OperationDeadline | None = None,
) -> dict[str, Any]:
    if set(arguments) - {"message_id", "include_raw_mime"}:
        raise ValueError("unsupported read_email fields")
    message_id = arguments.get("message_id")
    mailbox, validity, uid = _decode_ref(message_id)
    deadline = deadline or _current_deadline()
    with _imap(deadline=deadline) as client:
        message, raw, flags = _fetch_message(client, mailbox, validity, uid)
    return _read_email_result(
        message,
        raw,
        flags,
        message_id,
        mailbox,
        include_raw_mime=arguments.get("include_raw_mime") is True,
    )


def _read_emails_shared(
    message_ids: list[str],
    deadline: OperationDeadline | None = None,
) -> list[dict[str, Any]]:
    results = []
    imap_options = {"deadline": deadline} if deadline is not None else {}
    with _imap(**imap_options) as client:
        _set_socket_timeout(client, 8.0, deadline)
        for message_id in message_ids:
            _set_socket_timeout(client, 8.0, deadline)
            mailbox, validity, uid = _decode_ref(message_id)
            try:
                message, raw, flags = _fetch_message(
                    client, mailbox, validity, uid
                )
            except MailError as error:
                if str(error) == "Message no longer exists in this mailbox":
                    continue
                raise
            results.append(
                _read_email_result(message, raw, flags, message_id, mailbox)
            )
    return results


def read_attachment(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"message_id", "attachment_id"}:
        raise ValueError("read_attachment requires message_id and attachment_id")
    message_id = arguments["message_id"]
    attachment_id = _text(arguments["attachment_id"], "attachment_id", required=True, limit=4096)
    if not attachment_id.startswith(f"{message_id}."):
        raise ValueError("attachment_id does not belong to message_id")
    try:
        index = int(
            _decode_urlsafe_token(
                attachment_id.rsplit(".", 1)[1], "attachment_id"
            )
        )
    except (ValueError, UnicodeError) as error:
        raise ValueError("attachment_id is malformed") from error
    mailbox, validity, uid = _decode_ref(message_id)
    deadline = _current_deadline()
    with _imap(deadline=deadline) as client:
        message, _, _ = _fetch_message(client, mailbox, validity, uid)
    parts = [part for part, _depth in _iter_message_parts(message)]
    if not 0 <= index < len(parts):
        raise MailError("Attachment no longer exists")
    part = parts[index]
    advertised_parts = {id(item) for item in _attachment_parts(message)}
    if id(part) not in advertised_parts:
        raise MailError("Attachment identifier is not an advertised attachment")
    advertised_size = _attachment_payload_size(part)
    if advertised_size > MAX_ATTACHMENT_BYTES:
        raise MailError("Attachment exceeds the 5 MiB result limit")
    payload = _attachment_payload(part)
    if len(payload) > MAX_ATTACHMENT_BYTES:
        raise MailError("Attachment exceeds the 5 MiB result limit")
    return {
        "attachment_id": attachment_id,
        "filename": _decode_header(part.get_filename()) or f"attachment-{index}",
        "content_type": part.get_content_type(),
        "size": len(payload),
        "content_base64": base64.b64encode(payload).decode(),
    }


def read_email_thread(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) - {"message_id", "max_results"}:
        raise ValueError("unsupported read_email_thread fields")
    deadline = _current_deadline()
    anchor = read_email(
        {"message_id": arguments.get("message_id")}, deadline=deadline
    )
    maximum = arguments.get("max_results", 20)
    if isinstance(maximum, bool) or not isinstance(maximum, int) or not 1 <= maximum <= MAX_RESULTS:
        raise ValueError(f"max_results must be between 1 and {MAX_RESULTS}")

    def internet_id(message: dict[str, Any]) -> str:
        return message.get("internet_message_id", "").strip()

    def references(message: dict[str, Any]) -> set[str]:
        return {
            value
            for value in [
                *message.get("references", []),
                *message.get("in_reply_to", "").split(),
            ]
            if value
        }

    initial_reference_ids = list(
        dict.fromkeys(
            value
            for value in [internet_id(anchor), *references(anchor)]
            if value
        )
    )
    pending = list(initial_reference_ids)
    queued = set(pending)
    searched: set[str] = set()
    candidates_by_id: dict[str, dict[str, Any]] = {anchor["id"]: anchor}
    discovery_truncated = False
    if pending:
        with _imap(deadline=deadline) as discovery_client:
            while pending and len(searched) < 10:
                batch = pending[: min(5, 10 - len(searched))]
                del pending[: len(batch)]
                searched.update(batch)
                result = search_emails(
                    {
                        "mailbox": anchor["mailbox"],
                        "_thread_reference_ids": batch,
                        "max_results": MAX_RESULTS,
                    },
                    deadline=deadline,
                    client=discovery_client,
                )
                discovery_truncated = discovery_truncated or result["truncated"]
                for item in result["emails"]:
                    candidates_by_id[item["id"]] = item
                    for value in [internet_id(item), *references(item)]:
                        if value and value not in queued and value not in searched:
                            if len(queued | searched) >= 10:
                                discovery_truncated = True
                            else:
                                queued.add(value)
                                pending.append(value)
    if pending:
        discovery_truncated = True
    candidates = list(candidates_by_id.values())

    connected_ids = {anchor["id"]}
    connected_reference_nodes = (
        {internet_id(anchor)} | references(anchor)
    ) - {""}
    changed = True
    while changed:
        changed = False
        for message in candidates:
            if message["id"] in connected_ids:
                continue
            message_id = internet_id(message)
            message_references = references(message)
            message_reference_nodes = (
                {message_id} | message_references
            ) - {""}
            linked = bool(message_reference_nodes & connected_reference_nodes)
            if linked:
                connected_ids.add(message["id"])
                connected_reference_nodes.update(message_reference_nodes)
                changed = True
    connected = [item for item in candidates if item["id"] in connected_ids]

    def chronological_key(message: dict[str, Any]) -> tuple[dt.datetime, int, str]:
        try:
            parsed = email.utils.parsedate_to_datetime(message.get("date", ""))
            if parsed is None:
                raise ValueError
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=dt.timezone.utc)
            parsed = parsed.astimezone(dt.timezone.utc)
        except (TypeError, ValueError, OverflowError):
            parsed = dt.datetime.min.replace(tzinfo=dt.timezone.utc)
        try:
            uid = _decode_ref(message["id"])[2]
        except (KeyError, ValueError):
            uid = 0
        return parsed, uid, message.get("id", "")

    connected.sort(key=chronological_key)
    selected = connected[:maximum]
    if anchor["id"] not in {item["id"] for item in selected}:
        selected = sorted(
            connected[: maximum - 1] + [anchor], key=chronological_key
        )
    other_ids = [item["id"] for item in selected if item["id"] != anchor["id"]]
    loaded = {
        item["id"]: item
        for item in _read_emails_shared(other_ids, deadline)
    }
    messages = [
        anchor if item["id"] == anchor["id"] else loaded[item["id"]]
        for item in selected
        if item["id"] == anchor["id"] or item["id"] in loaded
    ]
    return {
        "messages": messages,
        "threading": "RFC Message-ID, References, and In-Reply-To relationships",
        "truncated": (
            discovery_truncated
            or len(connected_ids) > maximum
            or len(loaded) < len(other_ids)
        ),
    }


def _special_mailbox(client: imaplib.IMAP4_SSL, special: str, fallbacks: list[str]) -> str:
    mailboxes, _ = _mailboxes(client)
    flag = f"\\{special.lower()}"
    for item in mailboxes:
        if any(value.lower() == flag for value in item["flags"]):
            return item["name"]
    names = {item["name"].lower(): item["name"] for item in mailboxes}
    for fallback in fallbacks:
        if fallback.lower() in names:
            return names[fallback.lower()]
    raise MailError(f"Could not find the iCloud {special} mailbox")


def _move(client: imaplib.IMAP4_SSL, message_id: str, destination: str) -> dict[str, Any]:
    mailbox, validity, uid = _decode_ref(message_id)
    actual = _select(client, mailbox, readonly=False)
    if actual != validity:
        raise MailError("Message identifier is stale because the mailbox changed")
    exists_status, exists_data = client.uid("FETCH", str(uid), "(UID)")
    if (
        exists_status != "OK"
        or not exists_data
        or not any(item for item in exists_data if item is not None)
    ):
        raise MailError("Message no longer exists in the source mailbox")
    capabilities = {
        value.decode("ascii", errors="ignore") if isinstance(value, bytes) else value
        for value in client.capabilities
    }
    if "MOVE" in capabilities:
        try:
            status, _ = client.uid(
                "MOVE", str(uid), _quoted_mailbox(destination)
            )
        except (OSError, TimeoutError, imaplib.IMAP4.error) as error:
            return {
                "message_id": message_id,
                "destination": destination,
                "status": "move_unconfirmed",
                "error": f"MOVE response was lost: {type(error).__name__}",
                "retry_move": False,
                "next_step": "Inspect both source and destination mailboxes before acting again.",
            }
        outcome = "moved"
    else:
        try:
            status, _ = client.uid(
                "COPY", str(uid), _quoted_mailbox(destination)
            )
        except (OSError, TimeoutError, imaplib.IMAP4.error) as error:
            return {
                "message_id": message_id,
                "destination": destination,
                "status": "copy_unconfirmed",
                "error": f"COPY response was lost: {type(error).__name__}",
                "retry_move": False,
                "next_step": "Inspect both source and destination mailboxes before acting again.",
            }
        if status == "OK":
            try:
                status, _ = client.uid(
                    "STORE", str(uid), "+FLAGS.SILENT", "(\\Deleted)"
                )
            except (OSError, TimeoutError, imaplib.IMAP4.error) as error:
                return {
                    "message_id": message_id,
                    "destination": destination,
                    "status": "copied_source_cleanup_unconfirmed",
                    "error": f"Source cleanup failed: {type(error).__name__}",
                    "retry_move": False,
                    "next_step": "Remove the source message manually; the destination copy exists.",
                }
            if status != "OK":
                return {
                    "message_id": message_id,
                    "destination": destination,
                    "status": "copied_source_cleanup_failed",
                    "retry_move": False,
                    "next_step": "Remove the source message manually; the destination copy exists.",
                }
        outcome = "copied_and_marked_deleted"
    if status != "OK":
        raise MailError(f"Could not move message to {destination!r}")
    return {"message_id": message_id, "destination": destination, "status": outcome}


def _move_batch(
    client: imaplib.IMAP4_SSL, message_ids: list[Any], destination: str
) -> dict[str, Any]:
    _set_socket_timeout(client, 25.0)
    results = []
    for message_id in message_ids:
        try:
            _set_socket_timeout(client, 25.0)
            results.append(_move(client, message_id, destination))
        except (
            MailError,
            ValueError,
            OSError,
            TimeoutError,
            imaplib.IMAP4.error,
        ) as error:
            results.append(
                {
                    "message_id": message_id,
                    "destination": destination,
                    "status": "failed",
                    "error": str(error),
                }
            )
    return {"results": results}


def move_emails(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"message_ids", "destination"}:
        raise ValueError("move_emails requires message_ids and destination")
    ids = _list(arguments["message_ids"], "message_ids", limit=MAX_MOVE_RESULTS)
    if not ids:
        raise ValueError("message_ids must not be empty")
    destination = _text(arguments["destination"], "mailbox", required=True, limit=500)
    with _imap(socket_timeout=10.0) as client:
        return _move_batch(client, ids, destination)


def archive_emails(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"message_ids"}:
        raise ValueError("archive_emails requires message_ids")
    ids = _list(arguments["message_ids"], "message_ids", limit=MAX_MOVE_RESULTS)
    with _imap(socket_timeout=10.0) as client:
        destination = _special_mailbox(client, "Archive", ["Archive"])
        return _move_batch(client, ids, destination)


def trash_emails(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"message_ids"}:
        raise ValueError("trash_emails requires message_ids")
    ids = _list(arguments["message_ids"], "message_ids", limit=MAX_MOVE_RESULTS)
    with _imap(socket_timeout=10.0) as client:
        destination = _special_mailbox(client, "Trash", ["Deleted Messages", "Trash"])
        return _move_batch(client, ids, destination)


def set_email_flags(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) - {"message_ids", "read", "flagged"}:
        raise ValueError("unsupported set_email_flags fields")
    ids = _list(
        arguments.get("message_ids"),
        "message_ids",
        limit=MAX_FLAG_RESULTS,
    )
    if not ids or arguments.get("read") is None and arguments.get("flagged") is None:
        raise ValueError("provide message_ids and at least one flag change")
    for key in ("read", "flagged"):
        if arguments.get(key) is not None and not isinstance(arguments[key], bool):
            raise ValueError(f"{key} must be a boolean")
    results = []
    with _imap(socket_timeout=10.0) as client:
        _set_socket_timeout(client, 25.0)
        for message_id in ids:
            changes = {}
            active_change = None
            try:
                _set_socket_timeout(client, 25.0)
                mailbox, validity, uid = _decode_ref(message_id)
                if _select(client, mailbox, readonly=False) != validity:
                    raise MailError(
                        "Message identifier is stale because the mailbox changed"
                    )
                exists_status, exists_data = client.uid("FETCH", str(uid), "(UID)")
                if (
                    exists_status != "OK"
                    or not exists_data
                    or not any(item for item in exists_data if item is not None)
                ):
                    raise MailError("Message no longer exists in the source mailbox")
                for key, flag in (("read", "\\Seen"), ("flagged", "\\Flagged")):
                    if arguments.get(key) is not None:
                        operation = (
                            "+FLAGS.SILENT"
                            if arguments[key] is True
                            else "-FLAGS.SILENT"
                        )
                        active_change = key
                        status, _ = client.uid("STORE", str(uid), operation, f"({flag})")
                        changes[key] = {
                            "status": "updated" if status == "OK" else "failed"
                        }
                        active_change = None
                failures = [
                    key for key, value in changes.items() if value["status"] == "failed"
                ]
                successes = [
                    key for key, value in changes.items() if value["status"] == "updated"
                ]
                results.append(
                    {
                        "message_id": message_id,
                        "status": (
                            "updated"
                            if not failures
                            else "partial"
                            if successes
                            else "failed"
                        ),
                        "changes": changes,
                    }
                )
            except (
                MailError,
                ValueError,
                OSError,
                TimeoutError,
                imaplib.IMAP4.error,
            ) as error:
                if active_change is not None:
                    changes[active_change] = {"status": "unconfirmed"}
                successes = [
                    key for key, value in changes.items() if value["status"] == "updated"
                ]
                results.append(
                    {
                        "message_id": message_id,
                        "status": (
                            "partial"
                            if successes
                            else "unconfirmed"
                            if active_change is not None
                            else "failed"
                        ),
                        "changes": changes,
                        "error": str(error),
                    }
                )
    return {"results": results}


def _recipients(value: Any, name: str, *, required: bool = False) -> list[str]:
    raw = _list(value, name, limit=MAX_RECIPIENTS)
    result = []
    for item in raw:
        address = _text(item, name, required=True, limit=320)
        if "\r" in address or "\n" in address:
            raise ValueError(f"{name} contains an invalid address")
        parsed_addresses = email.utils.getaddresses([address])
        if len(parsed_addresses) != 1:
            raise ValueError(f"{name} must contain one address per entry")
        display, parsed = parsed_addresses[0]
        if not parsed or "@" not in parsed:
            raise ValueError(f"{name} contains an invalid address")
        canonical = _email_address(parsed, name)
        decoded_display = _validated_display_name(display, name)
        result.append(
            email.utils.formataddr((decoded_display, canonical))
            if display
            else canonical
        )
    if required and not result:
        raise ValueError(f"{name} must not be empty")
    return result


def _read_outgoing_attachment(path: Path, remaining: int) -> bytes:
    if not path.is_absolute():
        raise ValueError("each attachment file must be an absolute regular-file path")
    if remaining <= 0:
        raise ValueError("attachments must be at most 5 MiB each and 10 MiB total")
    if not hasattr(os, "O_NOFOLLOW"):
        raise ValueError("secure attachment reads are not supported on this platform")
    flags = os.O_RDONLY | os.O_NOFOLLOW
    flags |= getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NONBLOCK", 0)
    descriptor: int | None = None
    try:
        descriptor = os.open(path, flags)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError(
                "each attachment file must be an absolute regular-file path"
            )
        limit = min(MAX_ATTACHMENT_BYTES, remaining)
        if metadata.st_size > limit:
            raise ValueError(
                "attachments must be at most 5 MiB each and 10 MiB total"
            )
        with os.fdopen(descriptor, "rb", closefd=True) as source:
            descriptor = None
            payload = source.read(limit + 1)
    except ValueError:
        raise
    except OSError as error:
        raise ValueError(
            "each attachment file must be an absolute regular-file path"
        ) from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if len(payload) > min(MAX_ATTACHMENT_BYTES, remaining):
        raise ValueError("attachments must be at most 5 MiB each and 10 MiB total")
    return payload


def _outgoing(arguments: dict[str, Any], reply: Message | None = None) -> EmailMessage:
    allowed = {
        "to", "cc", "bcc", "subject", "body", "html_body", "reply_message_id",
        "attachment_files", "from",
    }
    unknown = set(arguments) - allowed
    if unknown:
        raise ValueError(f"unsupported outgoing fields: {sorted(unknown)}")
    message = EmailMessage()
    config = _load_config(required=True)
    username = config["account_address"]
    permitted_from = {username, *config["allowed_from"]}
    sender = _email_address(
        arguments.get("from") or config["default_from"], "from"
    )
    if sender not in permitted_from:
        raise ValueError("from must be the account address or a configured allowed alias")
    display = config["display_name"]
    message["From"] = email.utils.formataddr((display, sender)) if display else sender
    to = _recipients(arguments.get("to"), "to")
    cc = _recipients(arguments.get("cc"), "cc")
    bcc = _recipients(arguments.get("bcc"), "bcc")
    if len(to) + len(cc) + len(bcc) > MAX_RECIPIENTS:
        raise ValueError(f"message may contain at most {MAX_RECIPIENTS} recipients")
    if reply is None and not (to or cc or bcc):
        raise ValueError("at least one to, cc, or bcc recipient is required")
    if to:
        message["To"] = ", ".join(to)
    if cc:
        message["Cc"] = ", ".join(cc)
    if bcc:
        message["Bcc"] = ", ".join(bcc)
    subject = _text(arguments.get("subject"), "subject", required=reply is None, limit=998)
    if reply is not None:
        if not (to or cc or bcc):
            reply_target = reply.get("Reply-To") or reply.get("From")
            message["To"] = reply_target
        if not subject:
            original = _decode_header(reply.get("Subject"))
            subject = original if re.match(r"^re:", original, re.I) else f"Re: {original}"
        internet_id = reply.get("Message-ID")
        if internet_id:
            message["In-Reply-To"] = internet_id
            references = reply.get("References", "")
            message["References"] = (references + " " + internet_id).strip()
    message["Subject"] = subject
    message["Date"] = email.utils.format_datetime(dt.datetime.now(dt.timezone.utc))
    message["Message-ID"] = email.utils.make_msgid(domain=username.split("@", 1)[1])
    body = _body_text(arguments.get("body"), "body")
    html = _body_text(arguments.get("html_body"), "html_body")
    if not body.strip() and not html.strip():
        raise ValueError("body or html_body is required")
    message.set_content(body or "This message contains an HTML part.")
    if html:
        message.add_alternative(html, subtype="html")
    total_attachment_bytes = 0
    for raw_path in _list(arguments.get("attachment_files"), "attachment_files", limit=20):
        path_text = _text(raw_path, "attachment_files", required=True, limit=4096)
        path = Path(path_text)
        payload = _read_outgoing_attachment(
            path, 10 * 1024 * 1024 - total_attachment_bytes
        )
        total_attachment_bytes += len(payload)
        import mimetypes

        content_type, _ = mimetypes.guess_type(path.name)
        maintype, subtype = (
            content_type.split("/", 1)
            if content_type and "/" in content_type
            else ("application", "octet-stream")
        )
        message.add_attachment(
            payload, maintype=maintype, subtype=subtype, filename=path.name
        )
    return message


def _smtp_send(message: Message) -> dict[str, Any]:
    deadline = _current_deadline()
    username = _username()
    password, _ = _password(username)
    raw_sender = email.utils.parseaddr(message.get("From", ""))[1]
    try:
        sender = _email_address(raw_sender, "Draft From")
    except ValueError:
        raise MailError(
            "Draft From address is not allowed by current configuration"
        ) from None
    config = _load_config(required=True)
    if sender not in {username, *config["allowed_from"]}:
        raise MailError("Draft From address is not allowed by current configuration")
    recipients = [
        address
        for header in ("To", "Cc", "Bcc")
        for _, address in email.utils.getaddresses([message.get(header, "")])
        if address
    ]
    if not recipients:
        raise ValueError("message has no recipients")
    if len(recipients) > MAX_RECIPIENTS:
        raise ValueError(f"message may contain at most {MAX_RECIPIENTS} recipients")
    wire = email.message_from_bytes(
        message.as_bytes(policy=email.policy.SMTP), policy=email.policy.SMTP
    )
    if "Bcc" in wire:
        del wire["Bcc"]
    client: smtplib.SMTP | None = None
    refused: dict[str, tuple[int, bytes]] | None = None
    acceptance_unconfirmed: str | None = None
    payload_sent = False
    final_data_reply: tuple[int, bytes] | None = None
    cleanup_warning = None
    try:
        client = smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT,
            timeout=deadline.timeout(min(_timeout(), 15.0)),
        )
        _set_socket_timeout(client, 15.0, deadline)
        client.ehlo()
        _set_socket_timeout(client, 15.0, deadline)
        client.starttls(context=ssl.create_default_context())
        _set_socket_timeout(client, 15.0, deadline)
        client.ehlo()
        _set_socket_timeout(client, 15.0, deadline)
        client.login(username, password)
        original_data = client.data
        original_getreply = client.getreply
        original_send = client.send
        data_command_active = False
        data_command_accepted = False

        def tracked_getreply() -> tuple[int, bytes]:
            nonlocal data_command_accepted
            reply = original_getreply()
            if data_command_active and reply[0] == 354:
                data_command_accepted = True
            return reply

        def tracked_send(payload: bytes) -> None:
            nonlocal payload_sent
            if data_command_active and data_command_accepted:
                payload_sent = True
            original_send(payload)

        def tracked_data(payload: Any) -> tuple[int, bytes]:
            nonlocal data_command_active, final_data_reply
            data_command_active = True
            try:
                final_data_reply = original_data(payload)
                return final_data_reply
            finally:
                data_command_active = False

        client.getreply = tracked_getreply
        client.send = tracked_send
        client.data = tracked_data
        try:
            _set_socket_timeout(client, 15.0, deadline)
            refused = client.send_message(
                wire, from_addr=sender, to_addrs=recipients
            )
        except (smtplib.SMTPServerDisconnected, OSError, TimeoutError) as error:
            if final_data_reply is not None and final_data_reply[0] != 250:
                raise smtplib.SMTPDataError(*final_data_reply) from error
            if not payload_sent:
                raise
            acceptance_unconfirmed = type(error).__name__
        finally:
            client.data = original_data
            client.getreply = original_getreply
            client.send = original_send
    except smtplib.SMTPException as error:
        raise MailError(f"iCloud SMTP rejected the request: {type(error).__name__}") from None
    except (OSError, TimeoutError) as error:
        raise MailError(f"Could not connect to iCloud SMTP: {type(error).__name__}") from None
    finally:
        if client is not None:
            cleanup_error = _cleanup_smtp(client, deadline)
            if cleanup_error is not None and refused is not None:
                cleanup_warning = (
                    "SMTP accepted the message, but connection cleanup failed: "
                    f"{type(cleanup_error).__name__}"
                )
    result = {
        "status": (
            "acceptance_unconfirmed"
            if acceptance_unconfirmed
            else "partial"
            if refused
            else "accepted"
        ),
        "internet_message_id": message.get("Message-ID", ""),
        "from": sender,
        "recipients": recipients,
        "refused": sorted(refused or {}),
    }
    if acceptance_unconfirmed:
        result.update(
            {
                "error": (
                    "Connection was lost while awaiting the SMTP DATA result: "
                    f"{acceptance_unconfirmed}"
                ),
                "retry_send": False,
                "next_step": "Check Sent Mail before deciding whether to send again.",
            }
        )
    elif refused:
        result.update(
            {
                "retry_send": False,
                "retry_recipients": sorted(refused),
                "next_step": (
                    "Send a new message only to refused recipients; retrying the "
                    "original message may duplicate delivery."
                ),
            }
        )
    if cleanup_warning:
        result["cleanup_warning"] = cleanup_warning
        result["retry_send"] = False
    return result


def _prepare_outgoing(arguments: dict[str, Any]) -> EmailMessage:
    reply = None
    reply_id = arguments.get("reply_message_id")
    if reply_id:
        mailbox, validity, uid = _decode_ref(reply_id)
        with _imap(socket_timeout=10.0) as client:
            reply, _, _ = _fetch_message(client, mailbox, validity, uid)
    return _outgoing(arguments, reply)


def send_email(arguments: dict[str, Any]) -> dict[str, Any]:
    return _smtp_send(_prepare_outgoing(arguments))


def create_draft(
    arguments: dict[str, Any],
    *,
    socket_timeout: float | None = 10.0,
    preserved_attachments: list[Message] | None = None,
) -> dict[str, Any]:
    message = _prepare_outgoing(arguments)
    if preserved_attachments:
        if len(preserved_attachments) > 20:
            raise MailError("Draft contains more than 20 attachments")
        total_attachment_bytes = 0
        for part in preserved_attachments:
            size = _attachment_payload_size(part)
            if size > MAX_ATTACHMENT_BYTES:
                raise MailError(
                    "Draft attachments must be at most 5 MiB each and 10 MiB total"
                )
            total_attachment_bytes += size
            if total_attachment_bytes > 10 * 1024 * 1024:
                raise MailError(
                    "Draft attachments must be at most 5 MiB each and 10 MiB total"
                )
        if message.get_content_type() != "multipart/mixed":
            message.make_mixed()
        for part in preserved_attachments:
            message.attach(copy.deepcopy(part))
    raw = message.as_bytes(policy=email.policy.SMTP)
    if len(raw) > MAX_MESSAGE_BYTES:
        raise MailError("Draft exceeds the 20 MiB message processing limit")
    with _imap(socket_timeout=socket_timeout) as client:
        drafts = _special_mailbox(client, "Drafts", ["Drafts"])
        try:
            _set_socket_timeout(client, 25.0)
            status, data = client.append(
                _quoted_mailbox(drafts), "(\\Draft \\Seen)", None, raw
            )
        except (
            OSError,
            TimeoutError,
            imaplib.IMAP4.error,
        ) as error:
            return {
                "draft_id": None,
                "internet_message_id": message["Message-ID"],
                "status": "creation_unconfirmed",
                "error": (
                    "Connection was lost while awaiting the IMAP APPEND result: "
                    f"{type(error).__name__}"
                ),
                "retry_create": False,
                "next_step": "Find the draft by its Internet Message-ID before creating another.",
            }
        if status != "OK":
            raise MailError("Could not create iCloud Mail draft")
        append_uid = client.response("APPENDUID")[1]
        if (
            isinstance(append_uid, (list, tuple))
            and append_uid
            and isinstance(append_uid[0], bytes)
        ):
            match = re.search(rb"(\d+)\s+(\d+)", append_uid[0])
            if match:
                validity, uid = map(int, match.groups())
                return {
                    "draft_id": _encode_ref(drafts, validity, uid),
                    "internet_message_id": message["Message-ID"],
                    "status": "created",
                }
        try:
            validity = _select(client, drafts, readonly=True)
            search_status, search_data = client.uid(
                "search", None, "HEADER", "Message-ID", _quoted(message["Message-ID"])
            )
            if search_status != "OK" or not search_data or not search_data[0]:
                raise MailError("Draft identifier recovery failed")
            uid = int(search_data[0].split()[-1])
        except (
            MailError,
            ValueError,
            TypeError,
            OSError,
            TimeoutError,
            imaplib.IMAP4.error,
        ):
            return {
                "draft_id": None,
                "internet_message_id": message["Message-ID"],
                "status": "created_unresolved",
                "retry_create": False,
                "next_step": "Find the existing draft by its Internet Message-ID.",
            }
    return {
        "draft_id": _encode_ref(drafts, validity, uid),
        "internet_message_id": message["Message-ID"],
        "status": "created",
    }


def _validate_draft_ref(client: imaplib.IMAP4_SSL, draft_id: str) -> Message:
    mailbox, validity, uid = _decode_ref(draft_id)
    drafts = _special_mailbox(client, "Drafts", ["Drafts"])
    if mailbox != drafts:
        raise ValueError("draft_id must identify a message in the Drafts mailbox")
    message, _, flags = _fetch_message(client, mailbox, validity, uid)
    if "\\Draft" not in flags:
        raise ValueError("draft_id must identify a message with the Draft flag")
    return message


def update_draft(arguments: dict[str, Any]) -> dict[str, Any]:
    draft_id = arguments.get("draft_id")
    if not draft_id:
        raise ValueError("update_draft requires draft_id")
    if "attachment_files" in arguments and arguments["attachment_files"] is None:
        raise ValueError("attachment_files must be an array")
    with _imap(socket_timeout=10.0) as client:
        existing = _validate_draft_ref(client, draft_id)
    replacement = dict(arguments)
    del replacement["draft_id"]
    preserved_attachments = None
    if "attachment_files" not in arguments and isinstance(existing, Message):
        preserved_attachments = list(_attachment_parts(existing))
    create_options: dict[str, Any] = {"socket_timeout": 10.0}
    if preserved_attachments:
        create_options["preserved_attachments"] = preserved_attachments
    created = create_draft(replacement, **create_options)
    created["replaced_draft_id"] = draft_id
    if not created.get("draft_id"):
        created["old_draft_cleanup"] = {
            "status": "preserved",
            "reason": "replacement draft ID is unresolved",
        }
        return created
    created["status"] = "updated"
    try:
        with _imap(socket_timeout=10.0) as client:
            trash = _special_mailbox(client, "Trash", ["Deleted Messages", "Trash"])
            cleanup = _move(client, draft_id, trash)
        if cleanup["status"] in {"moved", "copied_and_marked_deleted"}:
            created["old_draft_cleanup"] = {
                "status": "moved_to_trash",
                "method": cleanup["status"],
            }
        else:
            created["old_draft_cleanup"] = {
                **cleanup,
                "retry_update": False,
            }
    except (MailError, ValueError) as error:
        created["old_draft_cleanup"] = {
            "status": "failed",
            "error": str(error),
            "retry_update": False,
            "next_step": "Remove or move the old draft manually; the replacement exists.",
        }
    return created


def list_drafts(arguments: dict[str, Any]) -> dict[str, Any]:
    maximum = arguments.get("max_results", 20)
    if set(arguments) - {"max_results"}:
        raise ValueError("unsupported list_drafts fields")
    with _imap(socket_timeout=10.0) as client:
        drafts = _special_mailbox(client, "Drafts", ["Drafts"])
    return search_emails(
        {"mailbox": drafts, "max_results": maximum}, socket_timeout=10.0
    )


def send_draft(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"draft_id"}:
        raise ValueError("send_draft requires draft_id")
    draft_id = arguments["draft_id"]
    with _imap(socket_timeout=10.0) as client:
        message = _validate_draft_ref(client, draft_id)
    current_date = email.utils.format_datetime(dt.datetime.now(dt.timezone.utc))
    if "Date" in message:
        message.replace_header("Date", current_date)
    else:
        message["Date"] = current_date
    result = _smtp_send(message)
    result["draft_id"] = draft_id
    if result["status"] != "accepted":
        result["draft_cleanup"] = {
            "status": "preserved",
            "reason": f"SMTP result is {result['status']}",
            "retry_send": False,
        }
        return result
    try:
        with _imap(socket_timeout=10.0) as client:
            trash = _special_mailbox(client, "Trash", ["Deleted Messages", "Trash"])
            cleanup = _move(client, draft_id, trash)
        if cleanup["status"] in {"moved", "copied_and_marked_deleted"}:
            result["draft_cleanup"] = {
                "status": "moved_to_trash",
                "method": cleanup["status"],
            }
        else:
            result["draft_cleanup"] = {
                **cleanup,
                "retry_send": False,
            }
    except (MailError, ValueError) as error:
        result["draft_cleanup"] = {
            "status": "failed",
            "error": str(error),
            "retry_send": False,
            "next_step": "Remove or move the draft manually; the email was already accepted.",
        }
    return result


def _format_addresses(addresses: list[dict[str, str]]) -> str:
    return ", ".join(
        email.utils.formataddr((item.get("name", ""), item["address"]))
        if item.get("name")
        else item["address"]
        for item in addresses
        if item.get("address")
    )


def _html_to_text(value: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", value)
    text = re.sub(r"(?i)<br\s*/?>|</p\s*>|</div\s*>", "\n", text)
    return html.unescape(re.sub(r"(?s)<[^>]+>", "", text)).strip()


def forward_emails(arguments: dict[str, Any]) -> dict[str, Any]:
    allowed = {"message_ids", "to", "cc", "bcc", "note", "from"}
    if set(arguments) - allowed:
        raise ValueError("unsupported forward_emails fields")
    ids = _list(arguments.get("message_ids"), "message_ids", limit=1)
    if not ids:
        raise ValueError("message_ids must not be empty")
    results = []
    for message_id in ids:
        try:
            mailbox, validity, uid = _decode_ref(message_id)
            with _imap(socket_timeout=10.0) as client:
                source, raw, flags = _fetch_message(client, mailbox, validity, uid)
            original = _read_email_result(
                source, raw, flags, message_id, mailbox
            )
            subject = original["subject"]
            subject = (
                subject if re.match(r"^fwd?:", subject, re.I) else f"Fwd: {subject}"
            )
            note = _body_text(arguments.get("note"), "note", limit=20_000)
            forwarded_header = "\n".join(
                [
                    "---------- Forwarded message ----------",
                    f"From: {_format_addresses(original['from'])}",
                    f"Date: {original['date']}",
                    f"Subject: {original['subject']}",
                    "",
                ]
            )
            wrapper = f"{note}\n\n{forwarded_header}" if note else forwarded_header
            source_body = original["body_text"] or _html_to_text(
                original.get("body_html", "")
            )
            quoted = (wrapper + source_body[: max(0, MAX_BODY_CHARS - len(wrapper))])[
                :MAX_BODY_CHARS
            ]
            outgoing = {
                "to": arguments.get("to"),
                "cc": arguments.get("cc"),
                "bcc": arguments.get("bcc"),
                "from": arguments.get("from"),
                "subject": subject,
                "body": quoted,
            }
            forwarded = _prepare_outgoing(outgoing)
            attachment_parts: list[Message] = []
            attachment_count = 0
            attachment_bytes = 0
            for part in _attachment_parts(source):
                size = _attachment_payload_size(part)
                attachment_count += 1
                attachment_bytes += size
                if (
                    size > MAX_ATTACHMENT_BYTES
                    or attachment_count > 20
                    or attachment_bytes > 10 * 1024 * 1024
                ):
                    raise MailError(
                        "Cannot forward attachments: limit is 20 files, 5 MiB each, "
                        "and 10 MiB total"
                    )
                attachment_parts.append(part)
            decoded_attachment_bytes = 0
            for part in attachment_parts:
                filename = _decode_header(part.get_filename())
                payload = _attachment_payload(part)
                decoded_attachment_bytes += len(payload)
                if (
                    len(payload) > MAX_ATTACHMENT_BYTES
                    or decoded_attachment_bytes > 10 * 1024 * 1024
                ):
                    raise MailError(
                        "Cannot forward attachments: limit is 20 files, 5 MiB each, "
                        "and 10 MiB total"
                    )
                content_type = part.get_content_type().split("/", 1)
                if part.is_multipart() or content_type[0] == "message":
                    content_type = ["application", "octet-stream"]
                forwarded.add_attachment(
                    payload,
                    maintype=content_type[0],
                    subtype=content_type[1],
                    filename=filename or "attachment",
                )
            sent = _smtp_send(forwarded)
            sent["source_message_id"] = message_id
            results.append(sent)
        except (MailError, ValueError) as error:
            results.append(
                {
                    "source_message_id": message_id,
                    "status": "failed",
                    "error": str(error),
                }
            )
    return {"results": results}


TOOLS = [
    {"name": "get_account_status", "description": "Check local iCloud Mail configuration without connecting to Apple.", "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "configure_account", "description": "Persist non-secret iCloud Mail account, sender alias, and display settings. Incoming mail already includes every alias in the mailbox.", "inputSchema": {"type": "object", "properties": {"account_address": {"type": "string", "description": "Primary full iCloud Mail address used for SMTP authentication, not an alias or necessarily the Apple Account sign-in address."}, "imap_username": {"type": "string", "description": "Optional incoming-login override; normally leave blank."}, "default_from": {"type": "string", "description": "Default sender address; must be account_address or an allowed alias."}, "allowed_from": {"oneOf": [{"type": "array", "items": {"type": "string"}, "maxItems": 50}, {"type": "string"}], "description": "Optional iCloud Mail aliases allowed only for sending, as an array or comma-delimited string."}, "display_name": {"type": "string"}}, "required": ["account_address"], "additionalProperties": False}},
    {"name": "clear_account_configuration", "description": "Remove saved non-secret account settings while deliberately preserving the Keychain credential.", "inputSchema": {"type": "object", "properties": {"confirm": {"type": "boolean"}}, "required": ["confirm"], "additionalProperties": False}},
    {"name": "validate_account", "description": "Authenticate to iCloud IMAP and SMTP without sending email.", "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "open_apple_password_page", "description": "On macOS, open Apple Account so the user can create an app-specific password. This does not read credentials.", "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "open_keychain_access", "description": "On macOS, open Keychain Access and return fields for manually saving the app-specific password.", "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "list_mailboxes", "description": "List up to 100 iCloud Mail folders with total and unread counts; truncated is true when more folders exist.", "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "search_emails", "description": "Search one mailbox using bounded structured IMAP fields.", "inputSchema": {"type": "object", "properties": {"mailbox": {"type": "string", "default": "INBOX"}, "query": {"type": "string"}, "from": {"type": "string"}, "to": {"type": "string"}, "subject": {"type": "string"}, "after": {"type": "string", "description": "YYYY-MM-DD"}, "before": {"type": "string", "description": "YYYY-MM-DD"}, "unread": {"type": "boolean"}, "flagged": {"type": "boolean"}, "has_attachment": {"type": "boolean"}, "max_results": {"type": "integer", "minimum": 1, "maximum": MAX_RESULTS, "default": 20}}, "additionalProperties": False}},
    {"name": "read_email", "description": "Read one message and list its attachments.", "inputSchema": {"type": "object", "properties": {"message_id": {"type": "string"}, "include_raw_mime": {"type": "boolean", "default": False}}, "required": ["message_id"], "additionalProperties": False}},
    {"name": "read_email_thread", "description": "Read a best-effort conversation reconstructed within the message mailbox.", "inputSchema": {"type": "object", "properties": {"message_id": {"type": "string"}, "max_results": {"type": "integer", "minimum": 1, "maximum": MAX_RESULTS, "default": 20}}, "required": ["message_id"], "additionalProperties": False}},
    {"name": "read_attachment", "description": "Read one advertised attachment up to 5 MiB as base64.", "inputSchema": {"type": "object", "properties": {"message_id": {"type": "string"}, "attachment_id": {"type": "string"}}, "required": ["message_id", "attachment_id"], "additionalProperties": False}},
    {"name": "list_drafts", "description": "List iCloud Mail drafts.", "inputSchema": {"type": "object", "properties": {"max_results": {"type": "integer", "minimum": 1, "maximum": MAX_RESULTS, "default": 20}}, "additionalProperties": False}},
    {"name": "set_email_flags", "description": "Explicitly mark up to five messages read/unread or flagged/unflagged.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_FLAG_RESULTS}, "read": {"type": "boolean"}, "flagged": {"type": "boolean"}}, "required": ["message_ids"], "additionalProperties": False}},
    {"name": "move_emails", "description": "Explicitly move up to five messages to a named iCloud Mail folder.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_MOVE_RESULTS}, "destination": {"type": "string"}}, "required": ["message_ids", "destination"], "additionalProperties": False}},
    {"name": "archive_emails", "description": "Explicitly move up to five messages to the iCloud Archive folder.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_MOVE_RESULTS}}, "required": ["message_ids"], "additionalProperties": False}},
    {"name": "trash_emails", "description": "Explicitly move up to five messages to iCloud Trash without permanent deletion.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_MOVE_RESULTS}}, "required": ["message_ids"], "additionalProperties": False}},
    {"name": "create_draft", "description": "Create an iCloud Mail draft without sending it.", "inputSchema": {"type": "object", "properties": {"from": {"type": "string", "description": "Configured account address or allowed sender alias."}, "to": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "cc": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "bcc": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "subject": {"type": "string"}, "body": {"type": "string"}, "html_body": {"type": "string"}, "reply_message_id": {"type": "string"}, "attachment_files": {"type": "array", "items": {"type": "string"}, "maxItems": 20}}, "additionalProperties": False}},
    {"name": "update_draft", "description": "Replace an existing draft with revised content without sending it. Existing attachments are preserved when attachment_files is omitted.", "inputSchema": {"type": "object", "properties": {"draft_id": {"type": "string"}, "from": {"type": "string", "description": "Configured account address or allowed sender alias."}, "to": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "cc": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "bcc": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "subject": {"type": "string"}, "body": {"type": "string"}, "html_body": {"type": "string"}, "reply_message_id": {"type": "string"}, "attachment_files": {"type": "array", "items": {"type": "string"}, "maxItems": 20, "description": "Omit to preserve existing attachments, use an empty array to remove them, or provide paths to replace them."}}, "required": ["draft_id"], "additionalProperties": False}},
    {"name": "send_email", "description": "Send a new message or reply through iCloud SMTP; use only on explicit send intent.", "inputSchema": {"type": "object", "properties": {"from": {"type": "string", "description": "Configured account address or allowed sender alias."}, "to": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "cc": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "bcc": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "subject": {"type": "string"}, "body": {"type": "string"}, "html_body": {"type": "string"}, "reply_message_id": {"type": "string"}, "attachment_files": {"type": "array", "items": {"type": "string"}, "maxItems": 20}}, "additionalProperties": False}},
    {"name": "send_draft", "description": "Send an existing reviewed draft and move it to Trash; explicit send intent required.", "inputSchema": {"type": "object", "properties": {"draft_id": {"type": "string"}}, "required": ["draft_id"], "additionalProperties": False}},
    {"name": "forward_emails", "description": "Forward one existing message with an optional note; explicit send intent required. One source per call preserves an unambiguous acceptance receipt within the tool timeout.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 1}, "from": {"type": "string", "description": "Configured account address or allowed sender alias."}, "to": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "cc": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "bcc": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_RECIPIENTS}, "note": {"type": "string"}}, "required": ["message_ids"], "additionalProperties": False}},
]

HANDLERS = {
    "get_account_status": get_account_status,
    "configure_account": configure_account,
    "clear_account_configuration": clear_account_configuration,
    "validate_account": validate_account,
    "open_apple_password_page": open_apple_password_page,
    "open_keychain_access": open_keychain_access,
    "list_mailboxes": list_mailboxes,
    "search_emails": search_emails,
    "read_email": read_email,
    "read_email_thread": read_email_thread,
    "read_attachment": read_attachment,
    "list_drafts": list_drafts,
    "set_email_flags": set_email_flags,
    "move_emails": move_emails,
    "archive_emails": archive_emails,
    "trash_emails": trash_emails,
    "create_draft": create_draft,
    "update_draft": update_draft,
    "send_email": send_email,
    "send_draft": send_draft,
    "forward_emails": forward_emails,
}


def _response(request_id: Any, result: Any = None, error: dict[str, Any] | None = None) -> dict[str, Any]:
    response = {"jsonrpc": "2.0", "id": request_id}
    response["error" if error is not None else "result"] = error if error is not None else result
    return response


def handle(request: dict[str, Any]) -> dict[str, Any] | None:
    if "id" not in request:
        return None
    request_id = request.get("id")
    method = request.get("method")
    if method == "ping":
        return _response(request_id, {})
    if method == "initialize":
        return _response(
            request_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": SERVER_INFO,
            },
        )
    if method == "tools/list":
        return _response(request_id, {"tools": TOOLS})
    if method == "tools/call":
        params = request.get("params", {})
        name = params.get("name") if isinstance(params, dict) else None
        arguments = params.get("arguments", {}) if isinstance(params, dict) else {}
        if name not in HANDLERS:
            return _response(request_id, error={"code": -32602, "message": "Unknown tool"})
        if not isinstance(arguments, dict):
            return _response(request_id, error={"code": -32602, "message": "Tool arguments must be an object"})
        deadline_token = _ACTIVE_DEADLINE.set(OperationDeadline())
        try:
            result = HANDLERS[name](arguments)
            return _response(
                request_id,
                {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]},
            )
        except (ValueError, MailError) as error:
            return _response(
                request_id,
                {
                    "content": [{"type": "text", "text": str(error)}],
                    "isError": True,
                },
            )
        except Exception as error:  # redact unexpected internals
            return _response(
                request_id,
                {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Unexpected iCloud Mail error: {type(error).__name__}",
                        }
                    ],
                    "isError": True,
                },
            )
        finally:
            _ACTIVE_DEADLINE.reset(deadline_token)
    return _response(request_id, error={"code": -32601, "message": "Method not found"})


def self_test() -> None:
    ref = _encode_ref("INBOX", 123, 456)
    assert _decode_ref(ref) == ("INBOX", 123, 456)
    assert len(TOOLS) == len(HANDLERS)
    assert {tool["name"] for tool in TOOLS} == set(HANDLERS)
    message = EmailMessage()
    message["From"] = "Sender <sender@example.com>"
    message["To"] = "Reader <reader@example.com>"
    message["Subject"] = "Encoded ✓"
    message["Message-ID"] = "<test@example.com>"
    message.set_content("Hello world")
    message.add_attachment(b"data", maintype="application", subtype="octet-stream", filename="test.bin")
    parsed = email.message_from_bytes(message.as_bytes(), policy=email.policy.default)
    attachments = _attachment_entries(parsed, ref)
    assert _summary(parsed, ref)["snippet"] == "Hello world"
    assert attachments[0]["filename"] == "test.bin"
    assert handle({"jsonrpc": "2.0", "id": 1, "method": "initialize"})["result"]["serverInfo"] == SERVER_INFO
    assert len(handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})["result"]["tools"]) == len(TOOLS)
    try:
        _decode_ref("bad")
    except ValueError:
        pass
    else:
        raise AssertionError("malformed reference accepted")
    print("PASS icloud-mail MCP self-test")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    options = parser.parse_args()
    if options.self_test:
        self_test()
        return
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                raise ValueError("request must be an object")
            response = handle(request)
        except (ValueError, json.JSONDecodeError):
            response = _response(None, error={"code": -32700, "message": "Parse error"})
        if response is not None:
            print(json.dumps(response, separators=(",", ":"), ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
