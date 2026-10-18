#!/usr/bin/env python3
"""Validate plugin source/cache structure without third-party packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from safe_files import MAX_TEXT_BYTES, read_bytes, read_text


EXCLUDED_DIRS = {".git", ".venv", "__pycache__", "node_modules"}
TEXT_SUFFIXES = {
    "",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
REQUIRED_SKILL_SECTIONS = (
    "## When to invoke",
    "## Inputs and evidence",
    "## Workflow",
    "## Outputs and handoff",
    "## Completion evidence",
    "## Must not",
)
REQUIRED_ROOT_FILES = (".codexignore", "LICENSE", "README.md", "SECURITY.md")
PUBLIC_FIXTURE_HOME_PATH = re.compile(r"(?:/Users|/home)/[^/\s]+/")
PUBLIC_FIXTURE_TASK_ID = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=str(Path(__file__).parents[1] / "plugins" / "project-delivery"),
        help="plugin source root or installed version-directory root",
    )
    parser.add_argument(
        "--layout",
        choices=("auto", "source", "cache"),
        default="auto",
        help="enforce a source directory or Codex versioned-cache layout",
    )
    return parser.parse_args(argv)


def collect_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if (path.is_symlink() or path.is_file())
        and not EXCLUDED_DIRS.intersection(path.relative_to(root).parts)
    )


def is_external_link(target: str) -> bool:
    parsed = urlparse(target)
    return bool(parsed.scheme or parsed.netloc or target.startswith("#"))


def layout_is_valid(root: Path, name: str, version: str, layout: str) -> bool:
    source_layout = root.name == name
    cache_layout = root.parent.name == name and root.name == version
    if layout == "source":
        return source_layout
    if layout == "cache":
        return cache_layout
    return source_layout or cache_layout


def validate_portable_manifest(root: Path, overlay: dict) -> list[str]:
    """Check portable packages without changing legacy-only package behavior."""
    path = root / "plugin.json"
    if not path.exists() and not path.is_symlink():
        return []
    try:
        portable = json.loads(read_text(path, root=root))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [f"invalid portable manifest: {error}"]
    if not isinstance(portable, dict):
        return ["portable manifest must contain an object"]
    errors: list[str] = []
    if portable.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        errors.append("portable manifest must declare the Agent Plugins 1.0 schema")
    string_fields = {"$schema", "name", "version", "description", "homepage", "repository", "license"}
    unknown = set(portable) - string_fields - {"author", "keywords", "extensions"}
    if unknown:
        errors.append(f"portable manifest has unknown top-level fields: {', '.join(sorted(unknown))}")
    for field in string_fields.intersection(portable):
        if not isinstance(portable[field], str):
            errors.append(f"portable manifest {field} must be a string")
    name = portable.get("name")
    if not isinstance(name, str) or not 1 <= len(name) <= 64:
        errors.append("portable manifest name must have 1-64 characters")
    if "author" in portable:
        author = portable["author"]
        if (not isinstance(author, dict) or set(author) - {"name", "email", "url"}
                or not all(isinstance(value, str) for value in author.values())):
            errors.append("portable manifest author must contain only string name/email/url fields")
    if "keywords" in portable:
        keywords = portable["keywords"]
        if not isinstance(keywords, list) or not all(isinstance(value, str) for value in keywords):
            errors.append("portable manifest keywords must be an array of strings")
    for field in ("name", "version", "description", "author", "homepage",
                  "repository", "license", "keywords"):
        if portable.get(field) != overlay.get(field):
            errors.append(f"portable manifest {field} must match the Codex manifest")
    extensions = portable.get("extensions", {})
    if not isinstance(extensions, dict) or not all(isinstance(value, dict) for value in extensions.values()):
        errors.append("portable manifest extensions must map namespaces to objects")
    openai = extensions.get("com.openai", {}) if isinstance(extensions, dict) else None
    interface = openai.get("interface") if isinstance(openai, dict) else None
    if not isinstance(interface, dict):
        errors.append("portable manifest must provide extensions.com.openai.interface")
        return errors
    if interface != overlay.get("interface"):
        errors.append("portable manifest interface must match the Codex manifest")
    subtitle = interface.get("shortDescription")
    if not isinstance(subtitle, str) or not subtitle.strip() or len(subtitle) > 30:
        errors.append("portable manifest shortDescription must have 1-30 characters")
    for field in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if field not in interface:
            continue
        value = interface[field]
        if not isinstance(value, str) or not value.startswith("./"):
            errors.append(f"portable manifest {field} must be a contained ./ path")
            continue
        relative = Path(value.replace("\\", "/"))
        if ".." in relative.parts or not (root / relative).resolve().is_relative_to(root.resolve()):
            errors.append(f"portable manifest {field} escapes the plugin root")
            continue
        try:
            read_bytes(root / relative, root=root, max_bytes=5 * 1024 * 1024)
        except OSError as error:
            errors.append(f"portable manifest {field} is not usable artwork: {error}")
    return errors


def validate(root: Path, layout: str = "auto") -> tuple[list[str], int, int]:
    errors: list[str] = []
    if not root.is_dir():
        return [f"plugin root is not a directory: {root}"], 0, 0

    manifest_path = root / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        return [f"missing manifest: {manifest_path}"], 0, len(collect_files(root))

    try:
        manifest = json.loads(read_text(manifest_path, root=root))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [f"invalid manifest: {error}"], 0, len(collect_files(root))
    if not isinstance(manifest, dict):
        return ["manifest must contain an object"], 0, len(collect_files(root))
    errors.extend(validate_portable_manifest(root, manifest))

    for relative in REQUIRED_ROOT_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required release file: {relative}")

    name = manifest.get("name")
    version = manifest.get("version")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("manifest name must be lower-case hyphen-case")
        name = ""
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append("manifest version must be valid Semantic Versioning")
        version = ""
    if name and version and not layout_is_valid(root, name, version, layout):
        errors.append(
            "plugin path must be either <parent>/<name> for source or "
            "<cache>/<name>/<version> for an installed cache"
        )

    files = collect_files(root)
    started = time.monotonic()
    for index, path in enumerate(files, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(files) - index)
        print(
            f"CHECK [{index}/{len(files)}] file={path.relative_to(root)} eta={eta:.1f}s",
            flush=True,
        )
        if path.is_symlink():
            errors.append(f"unsupported symlink: {path}")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = read_text(path, root=root, max_bytes=MAX_TEXT_BYTES)
        except (OSError, UnicodeError) as error:
            errors.append(f"unreadable text file: {path}: {error}")
            continue
        placeholder_marker = "[" + "TODO:"
        if placeholder_marker in text:
            errors.append(f"placeholder: {path}")
        relative_parts = path.relative_to(root).parts
        if len(relative_parts) >= 2 and relative_parts[:2] == ("tests", "fixtures"):
            if PUBLIC_FIXTURE_HOME_PATH.search(text):
                errors.append(f"public fixture contains an absolute user-home path: {path}")
            if PUBLIC_FIXTURE_TASK_ID.search(text):
                errors.append(f"public fixture contains a raw task identifier: {path}")
        if path.name == "SKILL.md":
            if not text.startswith("---\n") or not re.search(
                r"^name: [a-z0-9]+(?:-[a-z0-9]+)*$", text, re.MULTILINE
            ):
                errors.append(f"invalid skill frontmatter: {path}")
            if not re.search(r"^description: .+", text, re.MULTILINE):
                errors.append(f"missing skill description: {path}")
            for section in REQUIRED_SKILL_SECTIONS:
                if section not in text:
                    errors.append(f"missing skill contract section {section}: {path}")
        if path.suffix.lower() == ".md":
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                clean_target = target.strip().split(maxsplit=1)[0].strip("<>")
                if is_external_link(clean_target):
                    continue
                relative_target = clean_target.split("#", 1)[0]
                if relative_target and not (path.parent / relative_target).resolve().exists():
                    errors.append(f"broken link: {path} -> {target}")
            for target in re.findall(r"`((?:\.\.?/)[^`\n]+)`", text):
                relative_target = target.split("#", 1)[0]
                if not (path.parent / relative_target).resolve().exists():
                    errors.append(f"missing referenced path: {path} -> {target}")

    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_files:
        errors.append("no skills found")
    return errors, len(skill_files), len(files)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).expanduser().resolve()
    errors, skill_count, file_count = validate(root, args.layout)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(f"PASS files={file_count} skills={skill_count} layout={args.layout}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
