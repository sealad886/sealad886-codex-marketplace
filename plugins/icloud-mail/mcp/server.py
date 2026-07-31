#!/usr/bin/env python3
"""Dependency-free local MCP server for iCloud Mail over TLS IMAP and SMTP."""

from __future__ import annotations

import argparse
import base64
import binascii
import datetime as dt
import email
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
from contextlib import contextmanager
from email.header import decode_header, make_header
from email.message import EmailMessage, Message
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
MAX_SEARCH_SCAN = 200
MAX_BODY_CHARS = 100_000
MAX_ATTACHMENT_BYTES = 5 * 1024 * 1024
REF_PREFIX = "icloud-mail:"


class MailError(RuntimeError):
    """Safe, user-actionable mail error."""


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
    base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
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
        display_name = _text(
            payload.get("display_name"), "display_name", limit=200
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
            account = _email_address(legacy, "ICLOUD_MAIL_USERNAME")
            return {
                **_default_config(),
                "account_address": account,
                "imap_username": os.environ.get(
                    "ICLOUD_MAIL_IMAP_USERNAME", ""
                ).strip(),
                "default_from": account,
                "display_name": os.environ.get(
                    "ICLOUD_MAIL_DISPLAY_NAME", ""
                ).strip(),
            }
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
    }
    if len(value) > limit or (
        name in protocol_or_header_fields and ("\r" in value or "\n" in value)
    ):
        raise ValueError(f"{name} is invalid or too long")
    return value


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
    except (LookupError, UnicodeError):
        return value


def _addresses(value: str | None) -> list[dict[str, str]]:
    return [
        {"name": _decode_header(name), "address": address}
        for name, address in email.utils.getaddresses([value or ""])
        if address
    ]


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
    config = _load_config(required=True)
    return config["imap_username"] or config["account_address"]


def _password(username: str) -> tuple[str, str]:
    environment = os.environ.get("ICLOUD_MAIL_APP_PASSWORD")
    if environment:
        return environment, "environment"
    if sys.platform == "darwin":
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
        if result.returncode == 0 and result.stdout.rstrip("\n"):
            return result.stdout.rstrip("\n"), "macOS Keychain"
    raise MailError(
        "No app-specific password found; store service codex-icloud-mail in "
        "macOS Keychain or set ICLOUD_MAIL_APP_PASSWORD"
    )


@contextmanager
def _imap() -> Iterator[imaplib.IMAP4_SSL]:
    username = _username()
    password, _ = _password(username)
    login = _imap_username()
    client: imaplib.IMAP4_SSL | None = None
    try:
        client = imaplib.IMAP4_SSL(
            IMAP_HOST,
            IMAP_PORT,
            ssl_context=ssl.create_default_context(),
            timeout=_timeout(),
        )
        client.login(login, password)
        yield client
    except imaplib.IMAP4.error as error:
        raise MailError(f"iCloud IMAP rejected the request: {error}") from None
    except (OSError, TimeoutError) as error:
        raise MailError(f"Could not connect to iCloud IMAP: {type(error).__name__}") from None
    finally:
        if client is not None:
            try:
                client.logout()
            except (imaplib.IMAP4.error, OSError):
                pass


def _select(client: imaplib.IMAP4_SSL, mailbox: str, *, readonly: bool) -> int:
    status, data = client.select(_quoted_mailbox(mailbox), readonly=readonly)
    if status != "OK":
        raise MailError(f"Cannot open mailbox {mailbox!r}")
    response = client.response("UIDVALIDITY")[1]
    if not response:
        raise MailError("Mailbox did not provide UIDVALIDITY")
    return int(response[0])


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
        payload = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
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
    status, data = client.uid("fetch", str(uid), "(BODY.PEEK[] FLAGS)")
    if status != "OK" or not data or not isinstance(data[0], tuple):
        raise MailError("Message no longer exists in this mailbox")
    raw = data[0][1]
    flags_text = data[0][0].decode("ascii", errors="replace")
    return email.message_from_bytes(raw, policy=email.policy.default), raw, flags_text


def _body(message: Message) -> tuple[str, str]:
    plain = ""
    html = ""
    parts = message.walk() if message.is_multipart() else [message]
    for part in parts:
        if part.get_content_disposition() == "attachment":
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


def _attachment_entries(message: Message, message_id: str) -> list[dict[str, Any]]:
    entries = []
    for index, part in enumerate(message.walk()):
        filename = _decode_header(part.get_filename())
        disposition = part.get_content_disposition()
        if not filename and disposition != "attachment":
            continue
        payload = part.get_payload(decode=True) or b""
        token = base64.urlsafe_b64encode(str(index).encode()).decode().rstrip("=")
        entries.append(
            {
                "attachment_id": f"{message_id}.{token}",
                "filename": filename or f"attachment-{index}",
                "content_type": part.get_content_type(),
                "size": len(payload),
                "read_supported": len(payload) <= MAX_ATTACHMENT_BYTES,
            }
        )
    return entries


def _summary(message: Message, message_id: str, flags: str = "") -> dict[str, Any]:
    plain, _ = _body(message)
    return {
        "id": message_id,
        "internet_message_id": message.get("Message-ID", ""),
        "subject": _decode_header(message.get("Subject")),
        "from": _addresses(message.get("From")),
        "to": _addresses(message.get("To")),
        "cc": _addresses(message.get("Cc")),
        "date": message.get("Date", ""),
        "unread": "\\Seen" not in flags,
        "flagged": "\\Flagged" in flags,
        "has_attachments": bool(_attachment_entries(message, message_id)),
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
            "(MESSAGE-ID SUBJECT FROM TO CC DATE REFERENCES IN-REPLY-TO)] "
            "BODYSTRUCTURE FLAGS)"
        ),
    )
    if status != "OK" or not data:
        raise MailError("Message no longer exists in this mailbox")
    headers = b""
    metadata = b""
    for item in data:
        if isinstance(item, tuple):
            metadata += item[0] if isinstance(item[0], bytes) else b""
            headers += item[1] if isinstance(item[1], bytes) else b""
        elif isinstance(item, bytes):
            metadata += item
    if not headers:
        raise MailError("Message no longer exists in this mailbox")
    message = email.message_from_bytes(headers, policy=email.policy.default)
    flags = metadata.decode("ascii", errors="replace")
    lower_metadata = metadata.lower()
    message_id = _encode_ref(mailbox, expected_validity, uid)
    return {
        "id": message_id,
        "internet_message_id": message.get("Message-ID", ""),
        "subject": _decode_header(message.get("Subject")),
        "from": _addresses(message.get("From")),
        "to": _addresses(message.get("To")),
        "cc": _addresses(message.get("Cc")),
        "date": message.get("Date", ""),
        "unread": "\\Seen" not in flags,
        "flagged": "\\Flagged" in flags,
        "has_attachments": (
            b"attachment" in lower_metadata or b"filename" in lower_metadata
        ),
        "snippet": "",
        "references": message.get("References", "").split(),
        "in_reply_to": message.get("In-Reply-To", ""),
    }


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
    display_name = _text(
        arguments.get("display_name"), "display_name", limit=200
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
    with _imap() as client:
        status, data = client.status("INBOX", "(MESSAGES)")
        if status != "OK":
            raise MailError("iCloud IMAP login succeeded but INBOX status failed")
        mailbox_status = data[0].decode("ascii", errors="replace") if data else ""
    username = _username()
    password, _ = _password(username)
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=_timeout()) as client:
            client.ehlo()
            client.starttls(context=ssl.create_default_context())
            client.ehlo()
            client.login(username, password)
    except smtplib.SMTPException as error:
        raise MailError(
            f"iCloud SMTP authentication failed: {type(error).__name__}"
        ) from None
    except (OSError, TimeoutError) as error:
        raise MailError(
            f"Could not connect to iCloud SMTP: {type(error).__name__}"
        ) from None
    match = re.search(r"MESSAGES (\d+)", mailbox_status)
    return {
        "status": "validated",
        "account_address": username,
        "imap_authenticated": True,
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
    result = _open_macos(
        arguments,
        "/System/Applications/Utilities/Keychain Access.app",
        "Keychain Access",
    )
    account = _load_config(required=True)["account_address"]
    result["instructions"] = {
        "keychain_item_name": KEYCHAIN_SERVICE,
        "account_name": account,
        "password_value": "Apple app-specific password",
    }
    return result


def _mailboxes(client: imaplib.IMAP4_SSL) -> list[dict[str, Any]]:
    status, data = client.list()
    if status != "OK":
        raise MailError("Could not list iCloud Mail mailboxes")
    result = []
    pattern = re.compile(rb'^\((?P<flags>[^)]*)\) "(?P<delimiter>[^"]*)" (?P<name>.+)$')
    for raw in data or []:
        if not raw:
            continue
        match = pattern.match(raw)
        if not match:
            continue
        name_raw = match.group("name").strip()
        if name_raw.startswith(b'"') and name_raw.endswith(b'"'):
            name_raw = name_raw[1:-1].replace(b'\\"', b'"').replace(b"\\\\", b"\\")
        name = _decode_imap_utf7(name_raw)
        flags = match.group("flags").decode("ascii", errors="replace").split()
        result.append({"name": name, "flags": flags})
    return result


def list_mailboxes(arguments: dict[str, Any]) -> dict[str, Any]:
    if arguments:
        raise ValueError("list_mailboxes takes no arguments")
    with _imap() as client:
        mailboxes = _mailboxes(client)
        for item in mailboxes:
            status, data = client.status(
                _quoted_mailbox(item["name"]), "(MESSAGES UNSEEN)"
            )
            text = data[0].decode("ascii", errors="replace") if status == "OK" and data else ""
            counts = dict(re.findall(r"(MESSAGES|UNSEEN) (\d+)", text))
            item["messages"] = int(counts.get("MESSAGES", 0))
            item["unread"] = int(counts.get("UNSEEN", 0))
        return {"mailboxes": mailboxes}


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


def search_emails(arguments: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "mailbox", "query", "from", "to", "subject", "after", "before",
        "unread", "flagged", "has_attachment", "max_results",
    }
    unknown = set(arguments) - allowed
    if unknown:
        raise ValueError(f"unsupported search fields: {sorted(unknown)}")
    mailbox = _text(arguments.get("mailbox", "INBOX"), "mailbox", required=True, limit=500)
    maximum = arguments.get("max_results", 20)
    if isinstance(maximum, bool) or not isinstance(maximum, int) or not 1 <= maximum <= MAX_RESULTS:
        raise ValueError(f"max_results must be between 1 and {MAX_RESULTS}")
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
    with _imap() as client:
        validity = _select(client, mailbox, readonly=True)
        charset = "UTF-8" if any(not item.isascii() for item in criteria) else None
        wire_criteria: list[str | bytes] = (
            [item.encode("utf-8") for item in criteria] if charset else criteria
        )
        status, data = client.uid("search", charset, *wire_criteria)
        if status != "OK":
            raise MailError("iCloud Mail search failed")
        uids = [int(item) for item in (data[0].split() if data and data[0] else [])]
        uids.reverse()
        results = []
        scanned = 0
        scan_limit = (
            min(len(uids), MAX_SEARCH_SCAN, max(maximum * 5, MAX_RESULTS))
            if arguments.get("has_attachment") is not None
            else len(uids)
        )
        for uid in uids[:scan_limit]:
            if len(results) >= maximum:
                break
            scanned += 1
            item = _fetch_summary(client, mailbox, validity, uid)
            if arguments.get("has_attachment") is not None and (
                item["has_attachments"] is not arguments["has_attachment"]
            ):
                continue
            results.append(item)
        return {
            "emails": results,
            "mailbox": mailbox,
            "returned": len(results),
            "matched_before_attachment_filter": len(uids),
            "scanned": scanned,
            "truncated": scanned < len(uids),
        }


def read_email(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) - {"message_id", "include_raw_mime"}:
        raise ValueError("unsupported read_email fields")
    message_id = arguments.get("message_id")
    mailbox, validity, uid = _decode_ref(message_id)
    with _imap() as client:
        message, raw, flags = _fetch_message(client, mailbox, validity, uid)
    plain, html = _body(message)
    result = _summary(message, message_id, flags)
    result.update(
        {
            "mailbox": mailbox,
            "body_text": plain,
            "body_html": html,
            "reply_to": _addresses(message.get("Reply-To")),
            "attachments": _attachment_entries(message, message_id),
            "references": message.get("References", "").split(),
            "in_reply_to": message.get("In-Reply-To", ""),
        }
    )
    if arguments.get("include_raw_mime") is True:
        if len(raw) > MAX_ATTACHMENT_BYTES:
            raise MailError("Raw MIME exceeds the 5 MiB result limit")
        result["raw_mime_base64"] = base64.b64encode(raw).decode()
    return result


def read_attachment(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"message_id", "attachment_id"}:
        raise ValueError("read_attachment requires message_id and attachment_id")
    message_id = arguments["message_id"]
    attachment_id = _text(arguments["attachment_id"], "attachment_id", required=True, limit=4096)
    if not attachment_id.startswith(f"{message_id}."):
        raise ValueError("attachment_id does not belong to message_id")
    try:
        index = int(
            base64.urlsafe_b64decode(
                attachment_id.rsplit(".", 1)[1] + "=" * (-len(attachment_id.rsplit(".", 1)[1]) % 4)
            )
        )
    except (ValueError, UnicodeError) as error:
        raise ValueError("attachment_id is malformed") from error
    mailbox, validity, uid = _decode_ref(message_id)
    with _imap() as client:
        message, _, _ = _fetch_message(client, mailbox, validity, uid)
    parts = list(message.walk())
    if not 0 <= index < len(parts):
        raise MailError("Attachment no longer exists")
    part = parts[index]
    payload = part.get_payload(decode=True) or b""
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
    anchor = read_email({"message_id": arguments.get("message_id")})
    maximum = arguments.get("max_results", 20)
    if isinstance(maximum, bool) or not isinstance(maximum, int) or not 1 <= maximum <= MAX_RESULTS:
        raise ValueError(f"max_results must be between 1 and {MAX_RESULTS}")
    subject = re.sub(r"^(?:(?:re|fw|fwd):\s*)+", "", anchor["subject"], flags=re.I)
    if not subject:
        return {
            "messages": [anchor],
            "threading": "RFC Message-ID, References, and In-Reply-To relationships",
            "truncated": False,
        }
    result = search_emails(
        {"mailbox": anchor["mailbox"], "subject": subject, "max_results": MAX_RESULTS}
    )
    candidates = list(reversed(result["emails"]))
    if all(item["id"] != anchor["id"] for item in candidates):
        candidates.append(anchor)

    def internet_id(message: dict[str, Any]) -> str:
        return message.get("internet_message_id", "").strip()

    def references(message: dict[str, Any]) -> set[str]:
        return {
            value
            for value in [
                *message.get("references", []),
                message.get("in_reply_to", "").strip(),
            ]
            if value
        }

    connected_ids = {anchor["id"]}
    connected_internet_ids = {internet_id(anchor)} - {""}
    changed = True
    while changed:
        changed = False
        for message in candidates:
            if message["id"] in connected_ids:
                continue
            message_id = internet_id(message)
            message_references = references(message)
            connected_messages = [
                item for item in candidates if item["id"] in connected_ids
            ]
            linked = bool(message_references & connected_internet_ids) or any(
                message_id and message_id in references(item)
                for item in connected_messages
            )
            if linked:
                connected_ids.add(message["id"])
                if message_id:
                    connected_internet_ids.add(message_id)
                changed = True
    connected = [item for item in candidates if item["id"] in connected_ids]
    selected = connected[:maximum]
    if anchor["id"] not in {item["id"] for item in selected}:
        selected = connected[: maximum - 1] + [anchor]
    messages = [
        anchor if item["id"] == anchor["id"] else read_email({"message_id": item["id"]})
        for item in selected
    ]
    return {
        "messages": messages,
        "threading": "RFC Message-ID, References, and In-Reply-To relationships",
        "truncated": result["truncated"] or len(connected_ids) > maximum,
    }


def _special_mailbox(client: imaplib.IMAP4_SSL, special: str, fallbacks: list[str]) -> str:
    mailboxes = _mailboxes(client)
    flag = f"\\{special.lower()}"
    for item in mailboxes:
        if any(value.lower() == flag for value in item["flags"]):
            return item["name"]
    names = {item["name"].lower(): item["name"] for item in mailboxes}
    for fallback in fallbacks:
        if fallback.lower() in names:
            return names[fallback.lower()]
    raise MailError(f"Could not find the iCloud {special} mailbox")


def _move(client: imaplib.IMAP4_SSL, message_id: str, destination: str) -> dict[str, str]:
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
        status, _ = client.uid("MOVE", str(uid), _quoted_mailbox(destination))
    else:
        status, _ = client.uid("COPY", str(uid), _quoted_mailbox(destination))
        if status == "OK":
            status, _ = client.uid("STORE", str(uid), "+FLAGS.SILENT", "(\\Deleted)")
    if status != "OK":
        raise MailError(f"Could not move message to {destination!r}")
    return {"message_id": message_id, "destination": destination, "status": "moved"}


def _move_batch(
    client: imaplib.IMAP4_SSL, message_ids: list[Any], destination: str
) -> dict[str, Any]:
    results = []
    for message_id in message_ids:
        try:
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
    ids = _list(arguments["message_ids"], "message_ids", limit=50)
    if not ids:
        raise ValueError("message_ids must not be empty")
    destination = _text(arguments["destination"], "mailbox", required=True, limit=500)
    with _imap() as client:
        return _move_batch(client, ids, destination)


def archive_emails(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"message_ids"}:
        raise ValueError("archive_emails requires message_ids")
    ids = _list(arguments["message_ids"], "message_ids", limit=50)
    with _imap() as client:
        destination = _special_mailbox(client, "Archive", ["Archive"])
        return _move_batch(client, ids, destination)


def trash_emails(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"message_ids"}:
        raise ValueError("trash_emails requires message_ids")
    ids = _list(arguments["message_ids"], "message_ids", limit=50)
    with _imap() as client:
        destination = _special_mailbox(client, "Trash", ["Deleted Messages", "Trash"])
        return _move_batch(client, ids, destination)


def set_email_flags(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) - {"message_ids", "read", "flagged"}:
        raise ValueError("unsupported set_email_flags fields")
    ids = _list(arguments.get("message_ids"), "message_ids", limit=50)
    if not ids or arguments.get("read") is None and arguments.get("flagged") is None:
        raise ValueError("provide message_ids and at least one flag change")
    results = []
    with _imap() as client:
        for message_id in ids:
            try:
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
                changes = {}
                for key, flag in (("read", "\\Seen"), ("flagged", "\\Flagged")):
                    if arguments.get(key) is not None:
                        operation = (
                            "+FLAGS.SILENT"
                            if arguments[key] is True
                            else "-FLAGS.SILENT"
                        )
                        status, _ = client.uid(
                            "STORE", str(uid), operation, f"({flag})"
                        )
                        changes[key] = {
                            "status": "updated" if status == "OK" else "failed"
                        }
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
                results.append(
                    {
                        "message_id": message_id,
                        "status": "failed",
                        "error": str(error),
                    }
                )
    return {"results": results}


def _recipients(value: Any, name: str, *, required: bool = False) -> list[str]:
    raw = _list(value, name, limit=100)
    result = []
    for item in raw:
        address = _text(item, name, required=True, limit=320)
        parsed = email.utils.parseaddr(address)[1]
        if not parsed or "@" not in parsed:
            raise ValueError(f"{name} contains an invalid address")
        result.append(address)
    if required and not result:
        raise ValueError(f"{name} must not be empty")
    return result


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
    to = _recipients(arguments.get("to"), "to", required=reply is None)
    cc = _recipients(arguments.get("cc"), "cc")
    bcc = _recipients(arguments.get("bcc"), "bcc")
    if to:
        message["To"] = ", ".join(to)
    if cc:
        message["Cc"] = ", ".join(cc)
    if bcc:
        message["Bcc"] = ", ".join(bcc)
    subject = _text(arguments.get("subject"), "subject", required=reply is None, limit=998)
    if reply is not None:
        if not to:
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
    body = _text(arguments.get("body"), "body", limit=MAX_BODY_CHARS)
    html = _text(arguments.get("html_body"), "html_body", limit=MAX_BODY_CHARS)
    if not body and not html:
        raise ValueError("body or html_body is required")
    message.set_content(body or "This message contains an HTML part.")
    if html:
        message.add_alternative(html, subtype="html")
    total_attachment_bytes = 0
    for raw_path in _list(arguments.get("attachment_files"), "attachment_files", limit=20):
        path_text = _text(raw_path, "attachment_files", required=True, limit=4096)
        path = Path(path_text)
        if not path.is_absolute() or not path.is_file() or path.is_symlink():
            raise ValueError("each attachment file must be an absolute regular-file path")
        size = path.stat().st_size
        total_attachment_bytes += size
        if size > MAX_ATTACHMENT_BYTES or total_attachment_bytes > 10 * 1024 * 1024:
            raise ValueError("attachments must be at most 5 MiB each and 10 MiB total")
        payload = path.read_bytes()
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
    username = _username()
    password, _ = _password(username)
    sender = email.utils.parseaddr(message.get("From", ""))[1]
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
    wire = email.message_from_bytes(
        message.as_bytes(policy=email.policy.SMTP), policy=email.policy.SMTP
    )
    if "Bcc" in wire:
        del wire["Bcc"]
    client: smtplib.SMTP | None = None
    refused: dict[str, tuple[int, bytes]] | None = None
    cleanup_warning = None
    try:
        client = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=_timeout())
        client.ehlo()
        client.starttls(context=ssl.create_default_context())
        client.ehlo()
        client.login(username, password)
        refused = client.send_message(wire, from_addr=sender, to_addrs=recipients)
    except smtplib.SMTPException as error:
        raise MailError(f"iCloud SMTP rejected the request: {type(error).__name__}") from None
    except (OSError, TimeoutError) as error:
        raise MailError(f"Could not connect to iCloud SMTP: {type(error).__name__}") from None
    finally:
        if client is not None:
            try:
                client.quit()
            except (smtplib.SMTPException, OSError, TimeoutError) as error:
                if refused is not None:
                    cleanup_warning = (
                        "SMTP accepted the message, but connection cleanup failed: "
                        f"{type(error).__name__}"
                    )
    result = {
        "status": "accepted",
        "internet_message_id": message.get("Message-ID", ""),
        "from": sender,
        "recipients": recipients,
        "refused": sorted(refused or {}),
    }
    if cleanup_warning:
        result["cleanup_warning"] = cleanup_warning
        result["retry_send"] = False
    return result


def _prepare_outgoing(arguments: dict[str, Any]) -> EmailMessage:
    reply = None
    reply_id = arguments.get("reply_message_id")
    if reply_id:
        mailbox, validity, uid = _decode_ref(reply_id)
        with _imap() as client:
            reply, _, _ = _fetch_message(client, mailbox, validity, uid)
    return _outgoing(arguments, reply)


def send_email(arguments: dict[str, Any]) -> dict[str, Any]:
    return _smtp_send(_prepare_outgoing(arguments))


def create_draft(arguments: dict[str, Any]) -> dict[str, Any]:
    message = _prepare_outgoing(arguments)
    raw = message.as_bytes(policy=email.policy.SMTP)
    with _imap() as client:
        drafts = _special_mailbox(client, "Drafts", ["Drafts"])
        status, data = client.append(
            _quoted_mailbox(drafts), "(\\Draft \\Seen)", None, raw
        )
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


def _validate_draft_ref(client: imaplib.IMAP4_SSL, draft_id: str) -> None:
    mailbox, validity, uid = _decode_ref(draft_id)
    drafts = _special_mailbox(client, "Drafts", ["Drafts"])
    if mailbox != drafts:
        raise ValueError("draft_id must identify a message in the Drafts mailbox")
    _, _, flags = _fetch_message(client, mailbox, validity, uid)
    if "\\Draft" not in flags:
        raise ValueError("draft_id must identify a message with the Draft flag")


def update_draft(arguments: dict[str, Any]) -> dict[str, Any]:
    draft_id = arguments.get("draft_id")
    if not draft_id:
        raise ValueError("update_draft requires draft_id")
    with _imap() as client:
        _validate_draft_ref(client, draft_id)
    replacement = dict(arguments)
    del replacement["draft_id"]
    created = create_draft(replacement)
    created["replaced_draft_id"] = draft_id
    if not created.get("draft_id"):
        created["old_draft_cleanup"] = {
            "status": "preserved",
            "reason": "replacement draft ID is unresolved",
        }
        return created
    created["status"] = "updated"
    try:
        with _imap() as client:
            trash = _special_mailbox(client, "Trash", ["Deleted Messages", "Trash"])
            _move(client, draft_id, trash)
        created["old_draft_cleanup"] = {"status": "moved_to_trash"}
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
    with _imap() as client:
        drafts = _special_mailbox(client, "Drafts", ["Drafts"])
    return search_emails({"mailbox": drafts, "max_results": maximum})


def send_draft(arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"draft_id"}:
        raise ValueError("send_draft requires draft_id")
    draft_id = arguments["draft_id"]
    mailbox, validity, uid = _decode_ref(draft_id)
    with _imap() as client:
        _validate_draft_ref(client, draft_id)
        message, _, _ = _fetch_message(client, mailbox, validity, uid)
    result = _smtp_send(message)
    result["draft_id"] = draft_id
    try:
        with _imap() as client:
            trash = _special_mailbox(client, "Trash", ["Deleted Messages", "Trash"])
            _move(client, draft_id, trash)
        result["draft_cleanup"] = {"status": "moved_to_trash"}
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
    ids = _list(arguments.get("message_ids"), "message_ids", limit=20)
    if not ids:
        raise ValueError("message_ids must not be empty")
    results = []
    for message_id in ids:
        try:
            original = read_email({"message_id": message_id})
            subject = original["subject"]
            subject = (
                subject if re.match(r"^fwd?:", subject, re.I) else f"Fwd: {subject}"
            )
            note = _text(arguments.get("note"), "note", limit=20_000)
            quoted = "\n".join(
                [
                    note,
                    "",
                    "---------- Forwarded message ----------",
                    f"From: {_format_addresses(original['from'])}",
                    f"Date: {original['date']}",
                    f"Subject: {original['subject']}",
                    "",
                    original["body_text"]
                    or _html_to_text(original.get("body_html", "")),
                ]
            ).strip()
            outgoing = {
                "to": arguments.get("to"),
                "cc": arguments.get("cc"),
                "bcc": arguments.get("bcc"),
                "from": arguments.get("from"),
                "subject": subject,
                "body": quoted,
            }
            forwarded = _prepare_outgoing(outgoing)
            mailbox, validity, uid = _decode_ref(message_id)
            with _imap() as client:
                source, _, _ = _fetch_message(client, mailbox, validity, uid)
            attachment_count = 0
            attachment_bytes = 0
            for part in source.walk():
                filename = _decode_header(part.get_filename())
                if not filename and part.get_content_disposition() != "attachment":
                    continue
                payload = part.get_payload(decode=True) or b""
                attachment_count += 1
                attachment_bytes += len(payload)
                if (
                    len(payload) > MAX_ATTACHMENT_BYTES
                    or attachment_count > 20
                    or attachment_bytes > 10 * 1024 * 1024
                ):
                    raise MailError(
                        "Cannot forward attachments: limit is 20 files, 5 MiB each, "
                        "and 10 MiB total"
                    )
                content_type = part.get_content_type().split("/", 1)
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
    {"name": "list_mailboxes", "description": "List iCloud Mail folders with total and unread counts.", "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "search_emails", "description": "Search one mailbox using bounded structured IMAP fields.", "inputSchema": {"type": "object", "properties": {"mailbox": {"type": "string", "default": "INBOX"}, "query": {"type": "string"}, "from": {"type": "string"}, "to": {"type": "string"}, "subject": {"type": "string"}, "after": {"type": "string", "description": "YYYY-MM-DD"}, "before": {"type": "string", "description": "YYYY-MM-DD"}, "unread": {"type": "boolean"}, "flagged": {"type": "boolean"}, "has_attachment": {"type": "boolean"}, "max_results": {"type": "integer", "minimum": 1, "maximum": MAX_RESULTS, "default": 20}}, "additionalProperties": False}},
    {"name": "read_email", "description": "Read one message and list its attachments.", "inputSchema": {"type": "object", "properties": {"message_id": {"type": "string"}, "include_raw_mime": {"type": "boolean", "default": False}}, "required": ["message_id"], "additionalProperties": False}},
    {"name": "read_email_thread", "description": "Read a best-effort conversation reconstructed within the message mailbox.", "inputSchema": {"type": "object", "properties": {"message_id": {"type": "string"}, "max_results": {"type": "integer", "minimum": 1, "maximum": MAX_RESULTS, "default": 20}}, "required": ["message_id"], "additionalProperties": False}},
    {"name": "read_attachment", "description": "Read one advertised attachment up to 5 MiB as base64.", "inputSchema": {"type": "object", "properties": {"message_id": {"type": "string"}, "attachment_id": {"type": "string"}}, "required": ["message_id", "attachment_id"], "additionalProperties": False}},
    {"name": "list_drafts", "description": "List iCloud Mail drafts.", "inputSchema": {"type": "object", "properties": {"max_results": {"type": "integer", "minimum": 1, "maximum": MAX_RESULTS, "default": 20}}, "additionalProperties": False}},
    {"name": "set_email_flags", "description": "Explicitly mark messages read/unread or flagged/unflagged.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 50}, "read": {"type": "boolean"}, "flagged": {"type": "boolean"}}, "required": ["message_ids"], "additionalProperties": False}},
    {"name": "move_emails", "description": "Explicitly move messages to a named iCloud Mail folder.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 50}, "destination": {"type": "string"}}, "required": ["message_ids", "destination"], "additionalProperties": False}},
    {"name": "archive_emails", "description": "Explicitly move messages to the iCloud Archive folder.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 50}}, "required": ["message_ids"], "additionalProperties": False}},
    {"name": "trash_emails", "description": "Explicitly move messages to iCloud Trash without permanent deletion.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 50}}, "required": ["message_ids"], "additionalProperties": False}},
    {"name": "create_draft", "description": "Create an iCloud Mail draft without sending it.", "inputSchema": {"type": "object", "properties": {"from": {"type": "string", "description": "Configured account address or allowed sender alias."}, "to": {"type": "array", "items": {"type": "string"}}, "cc": {"type": "array", "items": {"type": "string"}}, "bcc": {"type": "array", "items": {"type": "string"}}, "subject": {"type": "string"}, "body": {"type": "string"}, "html_body": {"type": "string"}, "reply_message_id": {"type": "string"}, "attachment_files": {"type": "array", "items": {"type": "string"}, "maxItems": 20}}, "additionalProperties": False}},
    {"name": "update_draft", "description": "Replace an existing draft with revised content without sending it.", "inputSchema": {"type": "object", "properties": {"draft_id": {"type": "string"}, "from": {"type": "string", "description": "Configured account address or allowed sender alias."}, "to": {"type": "array", "items": {"type": "string"}}, "cc": {"type": "array", "items": {"type": "string"}}, "bcc": {"type": "array", "items": {"type": "string"}}, "subject": {"type": "string"}, "body": {"type": "string"}, "html_body": {"type": "string"}, "reply_message_id": {"type": "string"}, "attachment_files": {"type": "array", "items": {"type": "string"}, "maxItems": 20}}, "required": ["draft_id"], "additionalProperties": False}},
    {"name": "send_email", "description": "Send a new message or reply through iCloud SMTP; use only on explicit send intent.", "inputSchema": {"type": "object", "properties": {"from": {"type": "string", "description": "Configured account address or allowed sender alias."}, "to": {"type": "array", "items": {"type": "string"}}, "cc": {"type": "array", "items": {"type": "string"}}, "bcc": {"type": "array", "items": {"type": "string"}}, "subject": {"type": "string"}, "body": {"type": "string"}, "html_body": {"type": "string"}, "reply_message_id": {"type": "string"}, "attachment_files": {"type": "array", "items": {"type": "string"}, "maxItems": 20}}, "additionalProperties": False}},
    {"name": "send_draft", "description": "Send an existing reviewed draft and move it to Trash; explicit send intent required.", "inputSchema": {"type": "object", "properties": {"draft_id": {"type": "string"}}, "required": ["draft_id"], "additionalProperties": False}},
    {"name": "forward_emails", "description": "Forward existing messages with an optional note; explicit send intent required.", "inputSchema": {"type": "object", "properties": {"message_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 20}, "from": {"type": "string", "description": "Configured account address or allowed sender alias."}, "to": {"type": "array", "items": {"type": "string"}}, "cc": {"type": "array", "items": {"type": "string"}}, "bcc": {"type": "array", "items": {"type": "string"}}, "note": {"type": "string"}}, "required": ["message_ids", "to"], "additionalProperties": False}},
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
    request_id = request.get("id")
    method = request.get("method")
    if method == "notifications/initialized":
        return None
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
