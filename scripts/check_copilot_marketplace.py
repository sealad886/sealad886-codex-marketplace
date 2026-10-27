#!/usr/bin/env python3
"""Generate or check Copilot's catalog against the canonical Codex packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from check_distribution_bundle import add_local_mcp_dependencies
from check_marketplace import MARKETPLACE_NAME, safe_source_path
from check_plugin import validate_portable_manifest
from safe_files import read_text


CATALOG_PATH = Path(".github/plugin/marketplace.json")


def read_object(path: Path, root: Path) -> dict:
    value = json.loads(read_text(path, root=root))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(root)} must contain an object")
    return value


def validate_portable_mcp(package: Path, overlay: dict) -> list[str]:
    declaration = overlay.get("mcpServers")
    if declaration is None:
        return []
    try:
        # Reuse the distribution validator's contained local entrypoint contract.
        add_local_mcp_dependencies(package, set(), declaration)
        legacy = read_object(package / declaration, package)
        expected = {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
            "mcpServers": {
                name: {
                    "type": "stdio",
                    "command": server["command"],
                    "args": ["${PLUGIN_ROOT}/" + server["args"][0].removeprefix("./")],
                    "cwd": "${PLUGIN_ROOT}",
                }
                for name, server in legacy["mcpServers"].items()
            },
        }
        actual = read_object(package / "mcp.json", package)
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        return [f"{package.name} portable mcp.json: {error}"]
    if actual != expected:
        return [f"{package.name} portable mcp.json must match the Codex MCP servers "
                "using stdio and plugin-root paths"]
    return []


def expected_catalog(root: Path) -> tuple[dict, list[str]]:
    canonical = read_object(root / ".agents/plugins/marketplace.json", root)
    entries = canonical.get("plugins")
    if canonical.get("name") != MARKETPLACE_NAME or not isinstance(entries, list) or not entries:
        raise ValueError("canonical marketplace must have its expected name and plugin entries")
    plugins: list[dict] = []
    errors: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("source"), dict):
            raise ValueError("canonical marketplace entries must contain source objects")
        name = entry.get("name")
        if not isinstance(name, str) or name in seen:
            raise ValueError("canonical marketplace plugin names must be unique strings")
        seen.add(name)
        package, path_errors = safe_source_path(root, entry["source"].get("path"))
        if path_errors:
            raise ValueError("; ".join(path_errors))
        assert package is not None
        overlay = read_object(package / ".codex-plugin/plugin.json", root)
        if overlay.get("name") != name:
            raise ValueError(f"{name} canonical source must match the package name")
        if not (package / "plugin.json").is_file():
            errors.append(f"{name} missing portable manifest plugin.json")
        else:
            errors.extend(f"{name}: {error}" for error in validate_portable_manifest(package, overlay))
        if not list((package / "skills").glob("*/SKILL.md")):
            errors.append(f"{name} must expose skills in skills/<name>/SKILL.md")
        errors.extend(validate_portable_mcp(package, overlay))
        plugins.append({
            "name": name,
            "description": overlay["description"],
            "version": overlay["version"],
            "source": "./" + package.relative_to(root).as_posix(),
        })
    return {
        "name": MARKETPLACE_NAME,
        "owner": {"name": "Andrew Cox"},
        "metadata": {"description": "Independent software delivery, Git, research, browser, "
                     "mail, visuals, and MLX plugins by sealad886."},
        "plugins": plugins,
    }, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--write", action="store_true", help="regenerate only the Copilot catalog")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    try:
        expected, errors = expected_catalog(root)
        path = root / CATALOG_PATH
        if not errors:
            if args.write:
                if any((root / parent).is_symlink() for parent in CATALOG_PATH.parents):
                    raise ValueError("Copilot catalog ancestors must not be symlinks")
                path.parent.mkdir(parents=True, exist_ok=True)
                # Read through the same no-symlink policy before replacing an existing file.
                if path.exists() or path.is_symlink():
                    read_text(path, root=root)
                path.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
            elif read_object(path, root) != expected:
                errors.append("Copilot marketplace is out of date; run "
                              "scripts/check_copilot_marketplace.py --write")
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        errors = [str(error)]
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(f"PASS copilot_marketplace={MARKETPLACE_NAME} plugins={len(expected['plugins'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
