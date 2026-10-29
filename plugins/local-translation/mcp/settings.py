"""Private, persistent Local Translation settings shared by desktop clients.

The file is independent of plugin cache versions. Secrets returned by
``load_settings`` are for the runtime only; use ``public_settings`` at boundaries.
"""

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile


MAX_SETTINGS_BYTES = 65536
_UNSET = object()
PUBLIC_DEPLOYMENT_FIELDS = {
    "base_url", "model", "artifact_revision", "runner_version", "locales",
    "max_input_chars", "max_prompt_bytes", "max_output_tokens",
    "context_window_tokens", "timeout_seconds", "run_timeout_seconds",
}


class SettingsError(RuntimeError):
    """Fixed messages suitable for MCP and browser responses."""

    MESSAGES = {
        "invalid_input": "Enter an existing absolute workspace folder and valid engine settings. Nothing was saved.",
        "invalid_credential": "Enter a nonempty API key without line breaks, or choose Keep or Clear. Nothing was saved.",
        "local_settings_failed": "Could not read or lock private Local Translation settings. Check local file permissions and close other setup pages, then try again.",
        "stale_configuration": "Settings changed while this page was open. Nothing was saved. Reopen setup to use the latest settings.",
        "verification_failed": "The engine compatibility check failed. Nothing was saved. Check the local endpoint, exact model alias and tokenizer support.",
        "model_unavailable": "The exact model alias is not listed by this engine. Check the served model name. Nothing was saved.",
        "tokenizer_unsupported": "This engine must support POST /tokenize with chat messages and return a positive token count. A chat-only OpenAI endpoint is insufficient. Nothing was saved.",
        "runner_unreachable": "Could not reach this local engine. Start it, check its port and API key, and try again. Nothing was saved.",
        "auth_required": "The engine requires a valid API key. Choose Use a new key and enter the key configured in oMLX or your runner. Nothing was saved.",
        "save_failed": "Could not save private Local Translation settings. Previous settings were preserved. Check local file permissions and try again.",
        "page_expired": "This setup page expired. Nothing was saved. Open a new page from the plugin.",
        "browser_unavailable": "Could not open the private setup page in your system browser. Check that a browser is available, then call translation_open_settings again.",
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


def _read_snapshot():
    path = settings_path()
    try:
        if path.is_symlink() or path.parent.is_symlink():
            raise ValueError()
        try:
            with path.open("rb") as stream:
                if os.name == "posix" and os.fstat(stream.fileno()).st_mode & 0o077:
                    raise ValueError()
                raw = stream.read(MAX_SETTINGS_BYTES + 1)
        except FileNotFoundError:
            return None, None
        if len(raw) > MAX_SETTINGS_BYTES:
            raise ValueError()
        value = _decode(raw)
        if (not isinstance(value, dict) or set(value) - {"root", "deployment", "api_key"}
                or not {"root", "deployment"} <= set(value)
                or not isinstance(value["root"], str) or not Path(value["root"]).is_absolute()
                or not isinstance(value["deployment"], dict)):
            raise ValueError()
        if "api_key" in value:
            _secret(value["api_key"])
        return value, hashlib.sha256(raw).hexdigest()
    except (OSError, ValueError, TypeError, UnicodeError, SettingsError):
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
        result.update(root=value["root"], deployment={key: item for key, item in value["deployment"].items()
                                                    if key in PUBLIC_DEPLOYMENT_FIELDS},
                      credential_configured="api_key" in value)
    return result


@contextmanager
def _locked(path):
    descriptor = None
    lock = path.parent / ".settings.lock"
    try:
        if path.parent.is_symlink():
            raise OSError()
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if os.name == "posix":
            path.parent.chmod(0o700)
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except OSError:
        raise SettingsError("local_settings_failed") from None
    try:
        yield
    finally:
        os.close(descriptor)
        try:
            lock.unlink(missing_ok=True)
        except OSError:
            pass


def save_settings(root, deployment, *, api_key_action="keep", api_key=None,
                  expected_revision=_UNSET, validate, verify):
    """Validate, verify, then atomically save; failed checks preserve old bytes.

    ``validate(deployment)`` returns normalized deployment configuration.
    ``verify(root, deployment, api_key)`` checks the configured engine without
    creating a translation job. Browser callers pass their inspected revision,
    including None when no file existed, to reject stale edits.
    """
    try:
        if not isinstance(root, str) or not root.strip() or len(root) > 4096:
            raise ValueError()
        directory = Path(root).expanduser()
        if not directory.is_absolute() or not directory.is_dir():
            raise ValueError()
        root = str(directory.resolve(strict=True))
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
    candidate = {"root": root, "deployment": deployment}
    if api_key is not None:
        candidate["api_key"] = api_key
    raw = json.dumps(candidate, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    if len(raw) > MAX_SETTINGS_BYTES:
        raise SettingsError("invalid_input")
    try:
        verify(root, deployment, api_key)
    except SettingsError:
        raise
    except Exception:
        raise SettingsError("verification_failed") from None
    path = settings_path()
    with _locked(path):
        if _read_snapshot()[1] != revision:
            raise SettingsError("stale_configuration")
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
    return {"saved": True, "settings_path": str(path),
            "settings_revision": hashlib.sha256(raw).hexdigest(), "root": root,
            "model": deployment.get("model"), "credential_configured": api_key is not None,
            "compatibility_checked": True}
