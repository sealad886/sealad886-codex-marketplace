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


MARKETPLACE_NAME = "sealad886-codex-marketplace"
MARKETPLACE_DISPLAY_NAME = "sealad886 Codex Marketplace"
REPOSITORY_SOURCE_URL = (
    "https://github.com/sealad886/sealad886-codex-marketplace.git"
)
PROJECT_DELIVERY_PLUGIN_NAME = "project-delivery"
PINNED_SOURCE_TYPE = "git-subdir"
LOCAL_SOURCE_TYPE = "local"
ALLOWED_SOURCE_TYPES = {PINNED_SOURCE_TYPE, LOCAL_SOURCE_TYPE}
EXPECTED_LICENSE_SHA256 = "486b9c74f1d5bf1a5be12a8fe070db7cfad5a4901f083d4810a677b32f2d4993"
EXPECTED_COPYRIGHT = "Copyright (c) 2026 Andrew Cox"
PLUGIN_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = (
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
IMMUTABLE_TAG = re.compile(
    rf"^(?:[a-z0-9][a-z0-9._-]*-)?v?(?P<version>{SEMVER_PATTERN})$"
)
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
SEMVER = re.compile(rf"^{SEMVER_PATTERN}$")


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


def version_from_tag(value: object) -> str | None:
    if not isinstance(value, str) or COMMIT_SHA.fullmatch(value):
        return None
    match = IMMUTABLE_TAG.fullmatch(value)
    return match.group("version") if match is not None else None


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
    source_ref: object,
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
    else:
        tagged_version = version_from_tag(source_ref)
        if tagged_version is not None and version != tagged_version:
            errors.append(
                f"{label} source.ref version {tagged_version!r} must match "
                f"pinned manifest version {version!r}"
            )
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


def validate_local_interface(
    plugin_root: Path,
    manifest: dict[str, object],
    label: str,
) -> list[str]:
    """Validate metadata Codex exposes before a repository-local plugin is installed."""

    errors: list[str] = []
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        return [f"{label} local manifest interface must be an object"]

    for field in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
    ):
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"{label} local manifest interface.{field} must be non-empty"
            )

    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities or not all(
        isinstance(value, str) and value.strip() for value in capabilities
    ):
        errors.append(
            f"{label} local manifest interface.capabilities must be a non-empty "
            "array of strings"
        )

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        errors.append(
            f"{label} local manifest interface.defaultPrompt must contain 1 to 3 prompts"
        )
    elif not all(
        isinstance(prompt, str) and prompt.strip() and len(prompt) <= 128
        for prompt in prompts
    ):
        errors.append(
            f"{label} local manifest interface.defaultPrompt entries must be "
            "non-empty strings of at most 128 characters"
        )

    for field in ("composerIcon", "logo"):
        asset, asset_errors = safe_source_path(plugin_root, interface.get(field))
        if asset_errors:
            errors.extend(
                error.replace("marketplace source.path", f"{label} interface.{field}")
                for error in asset_errors
            )
        elif asset is None or not asset.is_file():
            errors.append(f"{label} local manifest interface.{field} must name a file")

    return errors


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
    source_type = source.get("source")
    if (
        not isinstance(source_type, str)
        or source_type not in ALLOWED_SOURCE_TYPES
    ):
        errors.append(
            f"{label} source.source must be one of {sorted(ALLOWED_SOURCE_TYPES)!r}"
        )
    if (
        name == PROJECT_DELIVERY_PLUGIN_NAME
        and source_type != PINNED_SOURCE_TYPE
    ):
        errors.append(
            f"{label} {PROJECT_DELIVERY_PLUGIN_NAME} source.source must be "
            f"{PINNED_SOURCE_TYPE!r}"
        )

    source_ref: object = None
    source_commit: str | None = None
    if source_type == PINNED_SOURCE_TYPE:
        if source.get("url") != REPOSITORY_SOURCE_URL:
            errors.append(
                f"{label} source.url must be {REPOSITORY_SOURCE_URL!r}"
            )
        source_ref = source.get("ref")
        if not is_immutable_ref(source_ref):
            errors.append(
                f"{label} source.ref must be an immutable version tag or "
                "40-character commit"
            )
        source_commit, ref_errors = resolve_source_commit(root, source_ref, label)
        errors.extend(ref_errors)
    elif source_type == LOCAL_SOURCE_TYPE:
        for field in ("url", "ref"):
            if field in source:
                errors.append(
                    f"{label} local source must not declare source.{field}"
                )

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
    manifest_version = manifest.get("version")
    if not isinstance(manifest_version, str) or not SEMVER.fullmatch(
        manifest_version
    ):
        errors.append(
            f"{label} target manifest version must be valid Semantic Versioning"
        )
    manifest_interface = manifest.get("interface")
    manifest_category = (
        manifest_interface.get("category")
        if isinstance(manifest_interface, dict)
        else None
    )
    if entry.get("category") != manifest_category:
        errors.append(f"{label} category must match manifest interface.category")
    if source_type == LOCAL_SOURCE_TYPE:
        errors.extend(validate_local_interface(plugin_root, manifest, label))

    pinned_license_bytes: bytes | None = None
    if source_commit is not None:
        pinned_license_bytes, pinned_errors = inspect_pinned_source(
            root,
            source_commit,
            source_ref,
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
    project_delivery_entry = next(
        entry
        for entry in marketplace["plugins"]
        if entry["name"] == PROJECT_DELIVERY_PLUGIN_NAME
    )
    project_delivery_ref = project_delivery_entry["source"]["ref"]
    source_types = sorted(
        {entry["source"]["source"] for entry in marketplace["plugins"]}
    )
    print(
        f"PASS marketplace={MARKETPLACE_NAME} plugins={len(marketplace['plugins'])} "
        f"project-delivery-ref={project_delivery_ref} "
        f"sources={','.join(source_types)} "
        "policy=AVAILABLE/ON_INSTALL license_parity=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
