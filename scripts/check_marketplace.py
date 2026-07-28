#!/usr/bin/env python3
"""Validate repository marketplace identity, entries, containment, and licenses."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path


MARKETPLACE_NAME = "andrew-cox-codex-marketplace"
MARKETPLACE_DISPLAY_NAME = "Andrew Cox's Codex Plugin Marketplace"
REPOSITORY_SOURCE_URL = (
    "https://github.com/sealad886/andrew-cox-codex-marketplace.git"
)
PROJECT_DELIVERY_PLUGIN_NAME = "project-delivery"
PROJECT_DELIVERY_SOURCE_REF = "v1.4.0"
EXPECTED_SOURCE_TYPE = "git-subdir"
EXPECTED_LICENSE_SHA256 = "486b9c74f1d5bf1a5be12a8fe070db7cfad5a4901f083d4810a677b32f2d4993"
EXPECTED_COPYRIGHT = "Copyright (c) 2026 Andrew Cox"
PLUGIN_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
IMMUTABLE_TAG = re.compile(
    r"^(?:[a-z0-9][a-z0-9._-]*-)?v?\d+\.\d+\.\d+"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=str(Path(__file__).parents[1]),
        help="repository root containing .agents/plugins/marketplace.json",
    )
    return parser.parse_args(argv)


def safe_source_path(root: Path, value: object) -> tuple[Path | None, list[str]]:
    if not isinstance(value, str) or not value:
        return None, ["marketplace source.path must be a non-empty string"]
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    relative = Path(normalized)
    if relative.is_absolute() or ".." in relative.parts:
        return None, [f"marketplace source.path escapes the repository: {value}"]
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root):
        return None, [f"marketplace source.path resolves outside the repository: {value}"]
    return resolved, []


def is_immutable_ref(value: object) -> bool:
    return isinstance(value, str) and bool(
        IMMUTABLE_TAG.fullmatch(value) or COMMIT_SHA.fullmatch(value)
    )


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
    )


def resolve_source_commit(
    root: Path, source_ref: object, label: str
) -> tuple[str | None, list[str]]:
    if not is_immutable_ref(source_ref):
        return None, []
    assert isinstance(source_ref, str)
    revision = (
        f"{source_ref}^{{commit}}"
        if COMMIT_SHA.fullmatch(source_ref)
        else f"refs/tags/{source_ref}^{{commit}}"
    )
    result = run_git(root, "rev-parse", "--verify", revision)
    commit = result.stdout.decode("ascii", errors="replace").strip()
    if result.returncode != 0 or not COMMIT_SHA.fullmatch(commit):
        return None, [
            f"{label} source.ref does not resolve to an exact local tag or commit: "
            f"{source_ref!r}"
        ]
    return commit, []


def inspect_pinned_source(
    root: Path,
    commit: str,
    source_path: object,
    name: str,
    category: object,
    label: str,
) -> tuple[bytes | None, list[str]]:
    if not isinstance(source_path, str):
        return None, []
    prefix = source_path.replace("\\", "/")
    while prefix.startswith("./"):
        prefix = prefix[2:]
    prefix = prefix.rstrip("/")
    tree_result = run_git(
        root, "ls-tree", "-r", "--name-only", commit, "--", prefix
    )
    if tree_result.returncode != 0:
        return None, [f"cannot inspect {label} pinned source tree at {commit[:12]}"]
    tree_paths = {
        line
        for line in tree_result.stdout.decode("utf-8", errors="replace").splitlines()
        if line
    }
    manifest_path = f"{prefix}/.codex-plugin/plugin.json"
    license_path = f"{prefix}/LICENSE"
    readme_path = f"{prefix}/README.md"
    required = {manifest_path, license_path, readme_path}
    missing = sorted(required - tree_paths)
    if missing:
        return None, [
            f"{label} pinned source {commit[:12]} is missing required path: {path}"
            for path in missing
        ]

    manifest_result = run_git(root, "show", f"{commit}:{manifest_path}")
    if manifest_result.returncode != 0:
        return None, [
            f"cannot read {label} pinned manifest at {commit[:12]}:{manifest_path}"
        ]
    try:
        pinned_manifest = json.loads(manifest_result.stdout.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        return None, [f"cannot parse {label} pinned manifest: {error}"]

    errors: list[str] = []
    if pinned_manifest.get("name") != name:
        errors.append(f"{label} pinned manifest name must match marketplace entry")
    version = pinned_manifest.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append(f"{label} pinned manifest version must be valid Semantic Versioning")
    if not isinstance(pinned_manifest.get("description"), str) or not pinned_manifest.get(
        "description", ""
    ).strip():
        errors.append(f"{label} pinned manifest description must be non-empty")
    if not isinstance(pinned_manifest.get("license"), str) or not pinned_manifest.get(
        "license", ""
    ).strip():
        errors.append(f"{label} pinned manifest license must be non-empty")
    pinned_interface = pinned_manifest.get("interface")
    pinned_category = (
        pinned_interface.get("category")
        if isinstance(pinned_interface, dict)
        else None
    )
    if pinned_category != category:
        errors.append(
            f"{label} category must match pinned manifest interface.category"
        )
    skills_path = pinned_manifest.get("skills")
    if not isinstance(skills_path, str) or not skills_path:
        errors.append(f"{label} pinned manifest must declare a skills path")
    elif not any(
        path.startswith(f"{prefix}/skills/") and path.endswith("/SKILL.md")
        for path in tree_paths
    ):
        errors.append(f"{label} pinned source must contain at least one skill")

    license_result = run_git(root, "show", f"{commit}:{license_path}")
    if license_result.returncode != 0 or not license_result.stdout:
        errors.append(f"{label} pinned package license must be non-empty")
        return None, errors
    return license_result.stdout, errors


def validate_entry(
    root: Path,
    entry: object,
    index: int,
    seen_names: set[str],
    seen_paths: set[Path],
) -> list[str]:
    errors: list[str] = []
    label = f"marketplace plugin entry {index}"
    if not isinstance(entry, dict):
        return [f"{label} must be an object"]

    name = entry.get("name")
    if not isinstance(name, str) or not PLUGIN_NAME.fullmatch(name):
        errors.append(f"{label} name must be lower-case hyphen-case")
        return errors
    if name in seen_names:
        errors.append(f"marketplace plugin names must be unique: {name!r}")
    seen_names.add(name)

    source = entry.get("source")
    if not isinstance(source, dict):
        return errors + [f"{label} source must be an object"]
    if source.get("source") != EXPECTED_SOURCE_TYPE:
        errors.append(
            f"{label} source.source must be {EXPECTED_SOURCE_TYPE!r}"
        )
    if source.get("url") != REPOSITORY_SOURCE_URL:
        errors.append(
            f"{label} source.url must be {REPOSITORY_SOURCE_URL!r}"
        )
    source_ref = source.get("ref")
    if not is_immutable_ref(source_ref):
        errors.append(
            f"{label} source.ref must be an immutable version tag or 40-character commit"
        )
    source_commit, ref_errors = resolve_source_commit(root, source_ref, label)
    errors.extend(ref_errors)

    plugin_root, path_errors = safe_source_path(root, source.get("path"))
    errors.extend(path_errors)
    if plugin_root is None:
        return errors
    expected_root = (root / "plugins" / name).resolve()
    if plugin_root != expected_root:
        errors.append(
            f"{label} source.path must resolve to {expected_root}, found {plugin_root}"
        )
    if plugin_root in seen_paths:
        errors.append(f"marketplace plugin source paths must be unique: {plugin_root}")
    seen_paths.add(plugin_root)

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append(f"{label} policy must be an object")
    else:
        if policy.get("installation") != "AVAILABLE":
            errors.append(f"{label} policy.installation must be 'AVAILABLE'")
        if policy.get("authentication") != "ON_INSTALL":
            errors.append(f"{label} policy.authentication must be 'ON_INSTALL'")

    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"cannot read {label} target manifest: {error}")
        manifest = {}
    if manifest.get("name") != name:
        errors.append(f"{label} name must match target manifest name")
    manifest_interface = manifest.get("interface")
    manifest_category = (
        manifest_interface.get("category")
        if isinstance(manifest_interface, dict)
        else None
    )
    if entry.get("category") != manifest_category:
        errors.append(f"{label} category must match manifest interface.category")

    pinned_license_bytes: bytes | None = None
    if source_commit is not None:
        pinned_license_bytes, pinned_errors = inspect_pinned_source(
            root,
            source_commit,
            source.get("path"),
            name,
            entry.get("category"),
            label,
        )
        errors.extend(pinned_errors)

    package_license = plugin_root / "LICENSE"
    try:
        current_license_bytes = package_license.read_bytes()
    except OSError as error:
        errors.append(f"cannot read {label} package license: {error}")
    else:
        if not current_license_bytes:
            errors.append(f"{label} working-tree package license must be non-empty")

    if name == PROJECT_DELIVERY_PLUGIN_NAME:
        if source_ref != PROJECT_DELIVERY_SOURCE_REF:
            errors.append(
                "Project Delivery marketplace source.ref must be immutable release "
                f"{PROJECT_DELIVERY_SOURCE_REF!r}"
            )
        root_license = root / "LICENSE"
        try:
            root_bytes = root_license.read_bytes()
            package_bytes = package_license.read_bytes()
        except OSError as error:
            errors.append(f"cannot read required Project Delivery MIT license copy: {error}")
        else:
            if root_bytes != package_bytes or (
                pinned_license_bytes is not None
                and root_bytes != pinned_license_bytes
            ):
                errors.append(
                    "root, working-tree, and pinned Project Delivery MIT license files "
                    "must be byte-identical"
                )
            actual_hash = hashlib.sha256(root_bytes).hexdigest()
            if actual_hash != EXPECTED_LICENSE_SHA256:
                errors.append(
                    "MIT license text differs from the approved Andrew Cox license: "
                    f"sha256={actual_hash}"
                )
            license_lines = root_bytes.decode(
                "utf-8", errors="replace"
            ).splitlines()
            if EXPECTED_COPYRIGHT not in license_lines:
                errors.append(
                    f"MIT license must contain exactly: {EXPECTED_COPYRIGHT}"
                )
    return errors


def validate_repository_marketplace(root: Path) -> list[str]:
    errors: list[str] = []
    marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [f"cannot read repository marketplace: {error}"]

    if marketplace.get("name") != MARKETPLACE_NAME:
        errors.append(f"marketplace name must be {MARKETPLACE_NAME!r}")
    interface = marketplace.get("interface")
    if (
        not isinstance(interface, dict)
        or interface.get("displayName") != MARKETPLACE_DISPLAY_NAME
    ):
        errors.append(
            "marketplace interface.displayName must be "
            f"{MARKETPLACE_DISPLAY_NAME!r}"
        )

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        return errors + ["marketplace plugins must be an array"]
    if not plugins:
        return errors + ["marketplace must contain at least one plugin entry"]

    started = time.monotonic()
    seen_names: set[str] = set()
    seen_paths: set[Path] = set()
    for index, entry in enumerate(plugins, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(plugins) - index)
        plugin_name = entry.get("name") if isinstance(entry, dict) else "<invalid>"
        print(
            f"MARKETPLACE [{index}/{len(plugins)}] plugin={plugin_name} eta={eta:.1f}s",
            flush=True,
        )
        errors.extend(validate_entry(root, entry, index, seen_names, seen_paths))

    matching = [
        entry
        for entry in plugins
        if isinstance(entry, dict)
        and entry.get("name") == PROJECT_DELIVERY_PLUGIN_NAME
    ]
    if len(matching) != 1:
        errors.append(
            "marketplace must contain exactly one "
            f"{PROJECT_DELIVERY_PLUGIN_NAME!r} entry"
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).expanduser().resolve()
    errors = validate_repository_marketplace(root)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    marketplace = json.loads(
        (root / ".agents" / "plugins" / "marketplace.json").read_text(
            encoding="utf-8"
        )
    )
    print(
        f"PASS marketplace={MARKETPLACE_NAME} plugins={len(marketplace['plugins'])} "
        f"project-delivery-ref={PROJECT_DELIVERY_SOURCE_REF} "
        "source=git-subdir policy=AVAILABLE/ON_INSTALL license_parity=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
