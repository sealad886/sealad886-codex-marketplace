#!/usr/bin/env python3
"""Generate or check Claude Code's catalog against the canonical packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from check_copilot_marketplace import expected_catalog as portable_catalog, read_object
from check_marketplace import MARKETPLACE_NAME
from check_plugin import validate_claude_manifest
from safe_files import read_text


CATALOG_PATH = Path(".claude-plugin/marketplace.json")


def expected_catalog(root: Path) -> tuple[dict, list[str]]:
    # Both catalogs share membership, identity and package locations. Reusing
    # the portable projection also validates excluded Codex-only packages.
    catalog, errors = portable_catalog(root)
    for entry in catalog["plugins"]:
        package = root / entry["source"]
        overlay = read_object(package / ".codex-plugin/plugin.json", root)
        errors.extend(f"{entry['name']}: {error}"
                      for error in validate_claude_manifest(package, overlay))
    return catalog, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--write", action="store_true", help="regenerate only the Claude Code catalog")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    try:
        expected, errors = expected_catalog(root)
        path = root / CATALOG_PATH
        if not errors:
            if args.write:
                if any((root / parent).is_symlink() for parent in CATALOG_PATH.parents):
                    raise ValueError("Claude Code catalog ancestors must not be symlinks")
                path.parent.mkdir(parents=True, exist_ok=True)
                if path.exists() or path.is_symlink():
                    read_text(path, root=root)
                path.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
            elif read_object(path, root) != expected:
                errors.append("Claude Code marketplace is out of date; run "
                              "scripts/check_claude_marketplace.py --write")
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        errors = [str(error)]
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(f"PASS claude_marketplace={MARKETPLACE_NAME} plugins={len(expected['plugins'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
