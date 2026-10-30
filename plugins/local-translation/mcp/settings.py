"""Private, persistent Local Translation settings shared by desktop clients.

The file is independent of plugin cache versions. Secrets returned by
``load_settings`` are for the runtime only; use ``public_settings`` at boundaries.
"""

from contextlib import contextmanager
import errno
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile

if os.name == "nt":
    import msvcrt
else:
    import fcntl


MAX_SETTINGS_BYTES = 65536
SCHEMA_VERSION = 2
_UNSET = object()
PUBLIC_DEPLOYMENT_FIELDS = {
    "base_url", "model", "artifact_revision", "runner_version", "locales",
    "max_input_chars", "max_prompt_bytes", "max_output_tokens",
    "context_window_tokens", "timeout_seconds", "run_timeout_seconds",
}


class SettingsError(RuntimeError):
    """Fixed messages suitable for MCP and in-app settings responses."""

    MESSAGES = {
        "invalid_input": "Enter valid engine settings. Nothing was saved.",
        "migration_required": "These settings use the retired workspace format. Choose Back up and upgrade saved settings in the in-app form to preserve the original and convert them to engine-only settings.",
        "invalid_credential": "Enter a nonempty API key without line breaks, or choose Keep or Clear. Nothing was saved.",
        "local_settings_failed": "Could not read or lock private Local Translation settings. Check local file permissions and close other setup pages, then try again.",
        "settings_busy": "Another settings save is active. Nothing was saved. Wait for it to finish, then try again.",
        "stale_configuration": "Settings changed while this page was open. Nothing was saved. Reopen setup to use the latest settings.",
        "verification_failed": "The engine compatibility check failed. Nothing was saved. Check the local endpoint, exact model alias and tokenizer support.",
        "model_unavailable": "The exact model alias is not listed by this engine. Check the served model name. Nothing was saved.",
        "tokenizer_unsupported": "This engine must support POST /tokenize with chat messages and return a positive token count. A chat-only OpenAI endpoint is insufficient. Nothing was saved.",
        "runner_unreachable": "Could not reach this local engine. Start it, check its port and API key, and try again. Nothing was saved.",
        "auth_required": "The engine requires a valid API key. Choose Use a new key and enter the key configured in oMLX or your runner. Nothing was saved.",
        "save_failed": "Could not save private Local Translation settings. Previous settings were preserved. Check local file permissions and try again.",
        "environment_override": "Environment configuration is active. Saved settings were not changed. Remove LOCAL_TRANSLATION_CONFIG from the MCP launch environment before saving in-app settings.",
    }

    def __init__(self, code):
        self.code = code
        super().__init__(self.MESSAGES[code])


def settings_path():
    """Return the version-independent user configuration path; no writes."""
    configured = os.environ.get("XDG_CONFIG_HOME")
    directory = Path(configured).expanduser() if configured else Path.home() / ".config"
    if not directory.is_absolute():
        raise SettingsError("local_settings_failed")
    return directory / "local-translation" / "settings.json"


def _decode(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError()
            result[key] = value
        return result
    def invalid_constant(_):
        raise ValueError()
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=invalid_constant)


def _secret(value):
    if not isinstance(value, str) or not value or len(value) > 4096 or "\r" in value or "\n" in value:
        raise SettingsError("invalid_credential")
    return value


def _read_private_bytes(path):
    """Read a bounded private regular file without following a settings symlink."""
    try:
        if path.is_symlink() or path.parent.is_symlink():
            raise ValueError()
        try:
            with path.open("rb") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or (os.name == "posix" and info.st_mode & 0o077):
                    raise ValueError()
                raw = stream.read(MAX_SETTINGS_BYTES + 1)
        except FileNotFoundError:
            return None
        if len(raw) > MAX_SETTINGS_BYTES:
            raise ValueError()
        return raw
    except (OSError, ValueError, TypeError):
        raise SettingsError("local_settings_failed") from None


def _validate_saved(value):
    if (not isinstance(value, dict) or set(value) - {"schema_version", "deployment", "api_key"}
            or not {"schema_version", "deployment"} <= set(value)
            or type(value["schema_version"]) is not int or value["schema_version"] != SCHEMA_VERSION
            or not isinstance(value["deployment"], dict)):
        raise ValueError()
    if "api_key" in value:
        _secret(value["api_key"])
    return value


def _read_snapshot():
    raw = _read_private_bytes(settings_path())
    if raw is None:
        return None, None
    try:
        value = _decode(raw)
        if isinstance(value, dict) and "root" in value and "schema_version" not in value:
            raise SettingsError("migration_required")
        _validate_saved(value)
        return value, hashlib.sha256(raw).hexdigest()
    except SettingsError as error:
        if error.code == "migration_required":
            raise
        raise SettingsError("local_settings_failed") from None
    except (ValueError, TypeError, UnicodeError):
        raise SettingsError("local_settings_failed") from None


def load_settings():
    """Return private settings or None. Never expose the returned API key."""
    return _read_snapshot()[0]


def settings_revision():
    return _read_snapshot()[1]


def public_settings():
    """Return safe configuration metadata, never a stored credential."""
    value, revision = _read_snapshot()
    result = {"configured": value is not None, "settings_path": str(settings_path()),
              "settings_revision": revision, "credential_configured": False}
    if value is not None:
        result.update(deployment={key: item for key, item in value["deployment"].items()
                                                    if key in PUBLIC_DEPLOYMENT_FIELDS},
                      credential_configured="api_key" in value)
    return result


@contextmanager
def _locked(path, *, protect_directory=True):
    """Hold a nonblocking OS lock, automatically released if the process dies.

    Keep the regular lock file in place: deleting it could let another process
    lock a different inode while an existing writer still holds the old one.
    Normal saves create and protect the dedicated settings directory. Explicit
    migration paths preserve their existing parent directory and permissions.
    """
    descriptor = None
    lock = path.parent / ".settings.lock"
    try:
        if path.parent.is_symlink():
            raise OSError()
        if protect_directory:
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            if os.name == "posix":
                path.parent.chmod(0o700)
        elif not path.parent.is_dir():
            raise OSError()
        if lock.is_symlink():
            raise OSError()
        descriptor = os.open(lock, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or lock.is_symlink():
            raise OSError()
        try:
            if os.name == "nt":
                if info.st_size == 0:
                    os.write(descriptor, b"\0")
                os.lseek(descriptor, 0, os.SEEK_SET)
                msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
            else:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            if error.errno in {errno.EACCES, errno.EAGAIN, errno.EWOULDBLOCK}:
                raise SettingsError("settings_busy") from None
            raise
    except (OSError, SettingsError) as error:
        if descriptor is not None:
            os.close(descriptor)
        if isinstance(error, SettingsError):
            raise
        raise SettingsError("local_settings_failed") from None
    try:
        yield
    finally:
        os.close(descriptor)


def _atomic_write(path, raw):
    """Replace settings only after the private candidate is fully written."""
    temporary = None
    try:
        descriptor, temporary = tempfile.mkstemp(prefix=".settings-", dir=path.parent)
        with os.fdopen(descriptor, "wb") as stream:
            if os.name == "posix":
                os.fchmod(stream.fileno(), 0o600)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    except OSError:
        raise SettingsError("save_failed") from None
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except OSError:
                pass


def save_settings(deployment, *, api_key_action="keep", api_key=None,
                  expected_revision=_UNSET, validate, verify):
    """Validate, verify, then atomically save; failed checks preserve old bytes.

    ``validate(deployment)`` returns normalized deployment configuration.
    ``verify(deployment, api_key)`` checks the configured engine without
    creating a translation job. In-app callers pass their inspected revision,
    including None when no file existed, to reject stale edits.
    """
    try:
        if not isinstance(deployment, dict) or "api_key_env" in deployment:
            raise ValueError()
        deployment = validate(deployment)
        if not isinstance(deployment, dict):
            raise ValueError()
    except Exception:
        raise SettingsError("invalid_input") from None
    if not isinstance(api_key_action, str) or api_key_action not in {"keep", "replace", "clear"}:
        raise SettingsError("invalid_credential")
    if api_key_action == "replace":
        api_key = _secret(api_key)
    elif api_key is not None:
        raise SettingsError("invalid_credential")
    previous, revision = _read_snapshot()
    if expected_revision is not _UNSET:
        if (expected_revision is not None and
                (not isinstance(expected_revision, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_revision))):
            raise SettingsError("invalid_input")
        if revision != expected_revision:
            raise SettingsError("stale_configuration")
    if api_key_action == "keep":
        api_key = previous.get("api_key") if previous else None
    candidate = {"schema_version": SCHEMA_VERSION, "deployment": deployment}
    if api_key is not None:
        candidate["api_key"] = api_key
    raw = json.dumps(candidate, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    if len(raw) > MAX_SETTINGS_BYTES:
        raise SettingsError("invalid_input")
    try:
        verify(deployment, api_key)
    except SettingsError:
        raise
    except Exception:
        raise SettingsError("verification_failed") from None
    path = settings_path()
    with _locked(path):
        if _read_snapshot()[1] != revision:
            raise SettingsError("stale_configuration")
        _atomic_write(path, raw)
    return {"saved": True, "settings_path": str(path),
            "settings_revision": hashlib.sha256(raw).hexdigest(),
            "model": deployment.get("model"), "credential_configured": api_key is not None,
            "compatibility_checked": True}
