"""Explicitly back up and convert retired workspace settings to engine-only settings.

This command never reads or deletes translation jobs. It does not contact the
engine. The runtime does not automatically accept the retired settings format.
"""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys


def _settings_module():
    """Share the package-owned settings implementation with MCP and CLI."""
    name = "_local_translation_settings"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("settings.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[name] = module
    return sys.modules[name]


settings = _settings_module()


BACKUP_SUFFIX = ".pre-temporary-jobs.bak"


class MigrationError(RuntimeError):
    MESSAGES = {
        "invalid_legacy": "The selected file is not valid retired Local Translation settings. Nothing was changed.",
        "backup_conflict": "A different backup already exists. Preserve it and choose another settings location before retrying. Nothing was changed.",
        "backup_failed": "Could not create a private settings backup. Nothing was changed. Check local file permissions.",
    }

    def __init__(self, code):
        self.code = code
        super().__init__(self.MESSAGES[code])


def _backup(path, raw):
    backup = path.with_name(path.name + BACKUP_SUFFIX)
    try:
        existing = settings._read_private_bytes(backup)
        if existing is not None:
            if existing != raw:
                raise MigrationError("backup_conflict")
            return backup
        descriptor = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                if os.name == "posix":
                    os.fchmod(stream.fileno(), 0o600)
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
        except OSError:
            backup.unlink()
            raise
        return backup
    except MigrationError:
        raise
    except (OSError, settings.SettingsError):
        raise MigrationError("backup_failed") from None


def migrate(path=None, *, validate):
    """Convert exactly one explicit settings file, retaining a private byte backup."""
    path = settings.settings_path() if path is None else Path(path).expanduser()
    if not path.is_absolute():
        raise MigrationError("invalid_legacy")
    with settings._locked(path, protect_directory=False):
        raw = settings._read_private_bytes(path)
        try:
            value = settings._decode(raw)
            if isinstance(value, dict) and value.get("schema_version") == settings.SCHEMA_VERSION:
                settings._validate_saved(value)
                return {"migrated": False, "settings_path": str(path), "schema_version": settings.SCHEMA_VERSION}
            if (not isinstance(value, dict) or set(value) - {"root", "deployment", "api_key"}
                    or not {"root", "deployment"} <= set(value)
                    or not isinstance(value["root"], str) or not Path(value["root"]).is_absolute()
                    or not isinstance(value["deployment"], dict) or "api_key_env" in value["deployment"]):
                raise ValueError()
            deployment = validate(value["deployment"])
            if not isinstance(deployment, dict):
                raise ValueError()
            candidate = {"schema_version": settings.SCHEMA_VERSION, "deployment": deployment}
            if "api_key" in value:
                candidate["api_key"] = settings._secret(value["api_key"])
        except Exception:
            raise MigrationError("invalid_legacy") from None
        converted = json.dumps(candidate, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
        if len(converted) > settings.MAX_SETTINGS_BYTES:
            raise MigrationError("invalid_legacy")
        backup = _backup(path, raw)
        settings._atomic_write(path, converted)
    return {"migrated": True, "settings_path": str(path), "backup_path": str(backup),
            "schema_version": settings.SCHEMA_VERSION}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, help="Absolute settings file path; defaults to the normal private settings location")
    args = parser.parse_args()
    import server
    try:
        result = migrate(args.settings, validate=server.validate_config)
    except (MigrationError, settings.SettingsError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
