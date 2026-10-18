#!/usr/bin/env python3
"""Validate blind route receipts against semantic route contracts."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
import tarfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from check_distribution_bundle import payload_sha256
from check_distribution_bundle import select_paths
from check_distribution_bundle import validate_source_boundary
from route_canary_protocol import CAPTURE_EVIDENCE_CLASS
from route_canary_protocol import CAPTURE_FIELDS
from route_canary_protocol import COORDINATOR_ATTESTATION
from route_canary_protocol import MAX_CAPTURE_AGE_SECONDS
from route_canary_protocol import PROTOCOL as COORDINATOR_PROTOCOL
from route_canary_protocol import PUBLIC_NONCE
from route_canary_protocol import PUBLIC_RECEIPT
from route_canary_protocol import RAW_HASH_METHOD
from route_canary_protocol import TASK_PROMPT_PROTOCOL
from route_canary_protocol import render_task_prompt
from safe_files import MAX_CONTROL_BYTES, MAX_PAYLOAD_BYTES, MAX_TEXT_BYTES
from safe_files import read_bytes as safe_read_bytes
from safe_files import read_text as safe_read_text


ALLOWED_CONDITIONAL_STATES = {
    "activated",
    "blocked",
    "deferred",
    "not-applicable",
    "planned-future",
}
ALLOWED_TRIGGER_RESULTS = {"future-pending", "met", "not-met", "unknown"}
ALLOWED_OUTCOME_STATES = {
    "meaningful-outcome-observed",
    "no-meaningful-outcome-observed",
    "unknown",
}
ALLOWED_GAP_KINDS = {
    "authority-limit",
    "missing-context",
    "missing-evidence",
    "unavailable-capability",
    "unresolved-question",
}
ALLOWED_GAP_ROUTE_EFFECTS = {"blocks-route", "nonblocking"}
PLANNED_FUTURE_CAPABILITIES = {"retrospective-improvement"}
FRESH_EVIDENCE_CLASS = "fresh-task semantic route observation"
HISTORICAL_EVIDENCE_CLASS = (
    "historical contract-blind route with post-hoc semantic annotation"
)
HISTORICAL_CONTRACT_FIXTURE = Path(
    "tests/fixtures/route-contracts-v2.legacy.json"
)
FRESH_SEMANTIC_FREEZE_FIELDS = {
    "actual_route",
    "authority",
    "conditional_dispositions",
    "evidence",
    "extra_capability_justifications",
    "gaps",
    "risk",
    "scale",
    "taxonomy_evidence",
    "taxonomy_rationale",
}
FRESH_V3_SEMANTIC_FREEZE_FIELDS = FRESH_SEMANTIC_FREEZE_FIELDS | {
    "outcome_observation",
    "scenario_observation",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_REVISION = re.compile(r"^[0-9a-f]{7,64}$")
PUBLIC_RECEIPT_ID = re.compile(r"^[a-z0-9][a-z0-9._-]{7,127}$")
INTERNAL_UUID = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
)
REQUIRED_RECEIPT_FIELDS = {
    "id",
    "actual_route",
    "scale",
    "risk",
    "authority",
    "taxonomy_rationale",
    "taxonomy_evidence",
    "conditional_dispositions",
    "extra_capability_justifications",
    "delivery_result",
    "evidence",
    "gaps",
}
FRESH_REQUIRED_RECEIPT_FIELDS = REQUIRED_RECEIPT_FIELDS | {"prompt"}
FRESH_PLUGIN_IDENTITY_FIELDS = {
    "cache_relative_path",
    "installed_version",
    "manifest_sha256",
    "name",
    "payload_hash_method",
    "payload_sha256",
    "source_revision",
}
FRESH_TASK_IDENTITY_FIELDS = {
    "public_receipt_id",
    "selected_at",
    "source_observation_sha256",
}
FRESH_REPOSITORY_IDENTITY_FIELDS = {
    "instructions_evidence",
    "name",
    "revision",
    "working_tree_state",
}
FRESH_LOADED_SPECIALIST_FIELDS = {
    "evidence",
    "relative_path",
    "skill",
    "skill_sha256",
    "state",
}
FRESH_CONDITIONAL_DISPOSITION_FIELDS = {"evidence", "rationale", "state"}
FRESH_EXTRA_JUSTIFICATION_FIELDS = {"evidence", "rationale"}
FRESH_V3_ANNOTATION_PROVENANCE_FIELDS = {
    "contract_access",
    "post_freeze_enrichment_fields",
    "semantic_fields_origin",
    "semantic_fields_revised_after_comparison",
}
FRESH_V3_LOADED_SPECIALIST_FIELDS = {
    "instruction_closure",
    "relative_path",
    "skill",
    "skill_sha256",
    "state",
}
FRESH_V3_INSTRUCTION_CLOSURE_FIELDS = {
    "files",
    "state",
    "unresolved_references",
}
FRESH_V3_INSTRUCTION_FILE_FIELDS = {
    "relative_path",
    "role",
    "sha256",
    "state",
}
FRESH_V3_SCENARIO_FIELDS = FRESH_REQUIRED_RECEIPT_FIELDS | {
    "outcome_observation",
    "scenario_observation",
}
FRESH_V3_SCENARIO_OBSERVATION_FIELDS = {
    "effects_performed",
    "legacy_administrative_visibility",
    "legacy_branded_state_created",
    "legacy_invocations",
    "legacy_runtime_events",
    "observation_scope",
}
FRESH_V3_OUTCOME_OBSERVATION_FIELDS = {"evidence", "state"}
FRESH_V3_CONDITIONAL_DISPOSITION_FIELDS = {
    "evidence",
    "rationale",
    "state",
    "trigger_evaluation",
}
FRESH_V3_TRIGGER_EVALUATION_FIELDS = {"result", "source", "trigger_statement"}
FRESH_V3_GAP_FIELDS = {
    "id",
    "kind",
    "next_action",
    "related_field",
    "route_effect",
    "summary",
}
FRESH_OBSERVATION_HASH_FIELDS = (
    "observation_scope",
    "effects_performed",
    "legacy_runtime_events",
    "legacy_administrative_visibility",
    "loaded_specialists",
    "scenarios",
)
FRESH_TOP_LEVEL_FIELDS = {
    "annotation_provenance",
    "contract_schema_version",
    "effects_performed",
    "evidence_class",
    "legacy_administrative_visibility",
    "legacy_runtime_events",
    "loaded_specialists",
    "observation_scope",
    "plugin_identity",
    "repository_identity",
    "scenarios",
    "schema_version",
    "semantic_fields_were_frozen_before_contract_comparison",
    "semantic_freeze_evidence",
    "semantic_freeze_scope",
    "task_identity",
}
FRESH_V3_TOP_LEVEL_FIELDS = FRESH_TOP_LEVEL_FIELDS | {
    "legacy_branded_state_created",
    "legacy_invocations",
}
GAP_ID = re.compile(r"^GAP-[A-Z0-9][A-Z0-9-]{2,63}$")
BACKTICKED_SHARED_REFERENCE = re.compile(
    r"`(\.\./\.shared/[a-z0-9._-]+\.(?:json|md))`"
)
INSTALLED_PAYLOAD_HASH_METHOD = (
    "project-delivery length-prefixed path-and-content sha256 v1"
)
SOURCE_PLUGIN_PREFIX = Path("plugins/project-delivery")
PLUGIN_MANIFEST = Path(".codex-plugin/plugin.json")
CACHEBUSTER_VERSION = re.compile(r"^.+\+codex\.[0-9]{14}$")
COORDINATOR_PROMPT_FIELDS = {"byte_count", "hash_method", "sha256"}
COORDINATOR_TASK_PROMPT_FIELDS = COORDINATOR_PROMPT_FIELDS | {"prompt_protocol"}
COORDINATOR_SOURCE_GIT_FIELDS = {
    "clean",
    "head",
    "status_byte_count",
    "status_format",
    "status_sha256",
}
COORDINATOR_PLUGIN_IDENTITY_FIELDS = {
    "directory_count",
    "file_count",
    "manifest_sha256",
    "name",
    "payload_hash_method",
    "payload_sha256",
    "version",
}
COORDINATOR_INSTALLED_IDENTITY_FIELDS = COORDINATOR_PLUGIN_IDENTITY_FIELDS | {
    "cache_relative_path",
    "marketplace",
}
COORDINATOR_PLUGIN_IDENTITIES_FIELDS = {
    "installed_cache",
    "prepared_personal_source",
    "source_package",
}
COORDINATOR_PARITY_FIELDS = {
    "prepared_to_installed",
    "source_to_installed",
    "source_to_prepared",
}
COORDINATOR_MARKETPLACE_FIELDS = {
    "entry_hash_method",
    "entry_sha256",
    "file_sha256",
    "marketplace_name",
    "plugin_name",
    "source_path",
    "source_type",
    "target_payload_sha256",
}
COORDINATOR_BOUNDARY_FIELDS = {
    "instruction_files",
    "mode",
    "repository_name",
    "revision",
    "working_tree_state",
}
COORDINATOR_INSTRUCTION_FIELDS = {
    "byte_count",
    "hash_method",
    "label",
    "sha256",
}
COORDINATOR_RAW_FIELDS = {"byte_count", "hash_method", "sha256"}
GRADE_EVIDENCE_CLASS = "independent sealed route grade"
GRADE_FIELDS = {
    "candidate_proof",
    "checker_sha256",
    "coordinator_attestation_sha256",
    "error_count",
    "error_set_sha256",
    "errors",
    "evidence_class",
    "graded_at_utc",
    "installed_payload_sha256",
    "limitations",
    "prompt_manifest_sha256",
    "raw_observation_sha256",
    "route_contract_sha256",
    "scenario_count",
    "schema_version",
    "source_revision",
    "task_prompt_sha256",
    "verdict",
}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "receipts",
        help="JSON receipt set produced by a fresh task before contract comparison",
    )
    parser.add_argument(
        "--root",
        default=str(Path(__file__).parents[1]),
        help="plugin source or installed root containing tests/route-contracts.json",
    )
    parser.add_argument(
        "--allow-subset",
        action="store_true",
        help="allow receipts for only a subset of canonical scenarios",
    )
    parser.add_argument(
        "--allow-historical-annotations",
        action="store_true",
        help=(
            "allow preserved blind route selections whose semantic taxonomy and branch "
            "annotations were added after contract comparison; never use this for candidate proof"
        ),
    )
    parser.add_argument(
        "--allow-unsealed-fresh",
        action="store_true",
        help=(
            "allow deprecated schema-v2 synthetic fresh records for regression tests; "
            "never use this option as candidate or decommission evidence"
        ),
    )
    parser.add_argument(
        "--allow-unattested-v3",
        action="store_true",
        help=(
            "allow schema-v3 structural regression tests without coordinator binding; "
            "never use this option as candidate or decommission evidence"
        ),
    )
    parser.add_argument(
        "--installed-plugin-root",
        help=(
            "exact installed plugin cache root used by a fresh observation; "
            "required for fresh-task evidence"
        ),
    )
    parser.add_argument(
        "--expected-source-revision",
        help=(
            "release commit expected to have produced the installed plugin; "
            "required for fresh-task evidence"
        ),
    )
    parser.add_argument(
        "--coordinator-attestation",
        help="publishable coordinator capture bound to the exact raw receipt bytes",
    )
    parser.add_argument(
        "--expected-attestation-sha256",
        help="externally retained SHA-256 of exact coordinator-attestation bytes",
    )
    parser.add_argument(
        "--prompt-manifest",
        help="prompt-only manifest whose bytes were sealed before task launch",
    )
    parser.add_argument(
        "--task-prompt",
        help="canonical blind task prompt whose exact bytes were used at launch",
    )
    parser.add_argument(
        "--grade-output",
        help="new output path for the independent schema-v3 grade record",
    )
    return parser.parse_args(argv)


def read_regular_bytes(
    path: Path, label: str, *, root: Path | None = None,
    max_bytes: int = MAX_CONTROL_BYTES,
) -> tuple[bytes | None, list[str]]:
    """Read one immutable regular-file snapshot without following a final symlink."""
    try:
        return safe_read_bytes(path, root=root, max_bytes=max_bytes), []
    except OSError as error:
        if "non-symlink" in str(error):
            return None, [f"{label} must be a regular non-symlink file: {error}"]
        return None, [f"invalid {label}: {error}"]


class DuplicateJSONKey(ValueError):
    """Raised when sealed JSON contains an ambiguous repeated object key."""


def reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateJSONKey(f"duplicate object key: {key}")
        value[key] = item
    return value


def json_from_bytes(raw: bytes) -> object:
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=reject_duplicate_json_keys,
    )


def parse_json_bytes(
    raw: bytes,
    label: str,
) -> tuple[dict[str, object] | None, list[str]]:
    try:
        value = json_from_bytes(raw)
    except (UnicodeError, json.JSONDecodeError, DuplicateJSONKey) as error:
        return None, [f"invalid {label}: {error}"]
    if not isinstance(value, dict):
        return None, [f"{label} root must be an object"]
    return value, []


def read_json(
    path: Path, label: str, *, root: Path | None = None,
) -> tuple[dict[str, object] | None, list[str]]:
    raw, errors = read_regular_bytes(path, label, root=root)
    if raw is None:
        return None, errors
    return parse_json_bytes(raw, label)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_command(root: Path, *arguments: str) -> tuple[bytes | None, str | None]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError:
        return None, "Git could not be executed"
    if result.returncode != 0:
        return None, "Git command failed"
    return result.stdout, None


def payload_sha256_snapshot(files: dict[Path, bytes]) -> str:
    """Hash one already-read package snapshot using the canonical payload method."""
    digest = hashlib.sha256()
    for relative, contents in sorted(files.items()):
        encoded_path = relative.as_posix().encode("utf-8")
        digest.update(len(encoded_path).to_bytes(8, "big"))
        digest.update(encoded_path)
        digest.update(len(contents).to_bytes(8, "big"))
        digest.update(contents)
    return digest.hexdigest()


def snapshot_directory_count(files: dict[Path, bytes]) -> int:
    directories: set[Path] = set()
    for relative in files:
        parent = relative.parent
        while parent != Path("."):
            directories.add(parent)
            parent = parent.parent
    return len(directories)


def identity_from_package_snapshot(
    files: dict[Path, bytes],
    label: str,
) -> tuple[dict[str, object] | None, list[str]]:
    manifest_raw = files.get(PLUGIN_MANIFEST)
    if manifest_raw is None:
        return None, [f"{label} lacks {PLUGIN_MANIFEST.as_posix()}"]
    manifest, manifest_errors = parse_json_bytes(manifest_raw, f"{label} manifest")
    if manifest is None:
        return None, manifest_errors
    errors = list(manifest_errors)
    if manifest.get("name") != "project-delivery":
        errors.append(f"{label} manifest name must be project-delivery")
    version = manifest.get("version")
    if not isinstance(version, str) or not version.strip():
        errors.append(f"{label} manifest version must be non-empty")
    if errors:
        return None, errors
    return {
        "name": manifest["name"],
        "version": version,
        "manifest_sha256": sha256_bytes(manifest_raw),
        "file_count": len(files),
        "directory_count": snapshot_directory_count(files),
        "payload_sha256": payload_sha256_snapshot(files),
        "payload_hash_method": INSTALLED_PAYLOAD_HASH_METHOD,
    }, []


def snapshot_committed_plugin(
    root: Path,
    expected_commit: str,
) -> tuple[dict[Path, bytes] | None, list[str]]:
    """Read the exact committed plugin tree without checking out or extracting it."""
    archive_raw, archive_error = git_command(
        root,
        "archive",
        "--format=tar",
        expected_commit,
        SOURCE_PLUGIN_PREFIX.as_posix(),
    )
    if archive_error is not None or archive_raw is None:
        return None, ["expected source commit plugin package cannot be archived"]
    files: dict[Path, bytes] = {}
    errors: list[str] = []
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_raw), mode="r:") as archive:
            for member in archive.getmembers():
                candidate = Path(member.name)
                if candidate.is_absolute() or ".." in candidate.parts:
                    errors.append("expected source plugin archive contains an unsafe path")
                    continue
                if candidate == SOURCE_PLUGIN_PREFIX or member.isdir():
                    continue
                try:
                    relative = candidate.relative_to(SOURCE_PLUGIN_PREFIX)
                except ValueError:
                    errors.append("expected source plugin archive escapes its package prefix")
                    continue
                if relative == Path(".") or not member.isfile():
                    errors.append(
                        "expected source plugin contains a non-regular entry: "
                        + relative.as_posix()
                    )
                    continue
                if member.mode & 0o111:
                    errors.append(
                        "expected source plugin contains an executable file: "
                        + relative.as_posix()
                    )
                    continue
                extracted = archive.extractfile(member)
                if extracted is None:
                    errors.append(
                        "expected source plugin file cannot be read: "
                        + relative.as_posix()
                    )
                    continue
                if relative in files:
                    errors.append(
                        "expected source plugin contains a duplicate path: "
                        + relative.as_posix()
                    )
                    continue
                files[relative] = extracted.read()
    except (OSError, tarfile.TarError) as error:
        return None, [f"expected source plugin archive cannot be inspected: {error}"]
    if not files:
        errors.append("expected source commit does not contain the plugin package")
    return (files if not errors else None), errors


def snapshot_installed_plugin(
    installed_plugin_root: Path | None,
) -> tuple[dict[Path, bytes] | None, list[str]]:
    """Read one bounded snapshot of every installed package entry."""
    if installed_plugin_root is None:
        return None, ["sealed provenance requires --installed-plugin-root"]
    if installed_plugin_root.is_symlink() or not installed_plugin_root.is_dir():
        return None, ["sealed provenance requires a regular installed plugin directory"]
    files: dict[Path, bytes] = {}
    errors: list[str] = []
    try:
        entries = sorted(installed_plugin_root.rglob("*"))
    except OSError as error:
        return None, [f"installed plugin package cannot be inventoried: {error}"]
    for entry in entries:
        relative = entry.relative_to(installed_plugin_root)
        if entry.is_symlink():
            errors.append(
                "installed plugin package contains a symlink: " + relative.as_posix()
            )
            continue
        if entry.is_dir():
            continue
        try:
            metadata = entry.stat(follow_symlinks=False)
        except OSError as error:
            errors.append(
                f"installed plugin entry cannot be inspected: {relative.as_posix()}: {error}"
            )
            continue
        if not stat.S_ISREG(metadata.st_mode):
            errors.append(
                "installed plugin package contains a non-regular entry: "
                + relative.as_posix()
            )
            continue
        if metadata.st_mode & 0o111:
            errors.append(
                "installed plugin package contains an executable file: "
                + relative.as_posix()
            )
            continue
        raw, read_errors = read_regular_bytes(
            entry, f"installed plugin file {relative.as_posix()}",
            root=installed_plugin_root, max_bytes=MAX_PAYLOAD_BYTES,
        )
        errors.extend(read_errors)
        if raw is not None:
            files[relative] = raw
    return (files if not errors else None), errors


def compare_identity(
    claimed: object,
    actual: dict[str, object],
    label: str,
) -> list[str]:
    if not isinstance(claimed, dict):
        return [f"{label} identity must be an object"]
    errors: list[str] = []
    for field, value in actual.items():
        if claimed.get(field) != value:
            errors.append(f"{label} {field} does not match inspected bytes")
    return errors


def validate_source_installed_provenance(
    root: Path,
    expected_source_revision: str | None,
    installed_files: dict[Path, bytes] | None,
    identities: dict[str, object],
    parity: object,
) -> list[str]:
    """Prove the installed package is the expected commit plus one cachebuster edit."""
    if not isinstance(expected_source_revision, str) or not SOURCE_REVISION.fullmatch(
        expected_source_revision
    ):
        return ["sealed provenance requires a full expected source revision"]
    committed_files, committed_errors = snapshot_committed_plugin(
        root, expected_source_revision
    )
    errors = list(committed_errors)
    if committed_files is None or installed_files is None:
        if installed_files is None:
            errors.append("sealed provenance lacks the initial installed package snapshot")
        return errors
    source_identity, source_errors = identity_from_package_snapshot(
        committed_files, "expected source package"
    )
    installed_identity, identity_errors = identity_from_package_snapshot(
        installed_files, "installed plugin package"
    )
    errors.extend(source_errors)
    errors.extend(identity_errors)
    if source_identity is None or installed_identity is None:
        return errors
    errors.extend(
        compare_identity(
            identities.get("source_package"), source_identity, "source_package"
        )
    )
    errors.extend(
        compare_identity(
            identities.get("installed_cache"),
            installed_identity,
            "installed_cache",
        )
    )

    source_paths = set(committed_files)
    installed_paths = set(installed_files)
    if source_paths != installed_paths:
        errors.append(
            "installed plugin paths do not exactly match the expected source commit"
        )
        return errors
    changed = [
        relative
        for relative in sorted(source_paths)
        if committed_files[relative] != installed_files[relative]
    ]
    mode = "exact-byte-parity"
    if changed:
        if changed != [PLUGIN_MANIFEST]:
            errors.append(
                "installed plugin differs from the expected source commit outside the manifest"
            )
            return errors
        source_manifest, source_manifest_errors = parse_json_bytes(
            committed_files[PLUGIN_MANIFEST], "expected source manifest"
        )
        installed_manifest, installed_manifest_errors = parse_json_bytes(
            installed_files[PLUGIN_MANIFEST], "installed plugin manifest"
        )
        errors.extend(source_manifest_errors)
        errors.extend(installed_manifest_errors)
        if source_manifest is None or installed_manifest is None:
            return errors
        source_version = source_manifest.get("version")
        installed_version = installed_manifest.get("version")
        transformed = dict(source_manifest)
        transformed["version"] = installed_version
        if not isinstance(source_version, str) or not isinstance(installed_version, str):
            errors.append("source and installed manifest versions must be strings")
        elif (
            not CACHEBUSTER_VERSION.fullmatch(installed_version)
            or installed_version != f"{source_version}+codex.{installed_version.rsplit('.', 1)[-1]}"
        ):
            errors.append(
                "installed manifest version is not the canonical Plugin Creator cachebuster"
            )
        expected_manifest_raw = (
            json.dumps(transformed, indent=2, ensure_ascii=False) + "\n"
        ).encode("utf-8")
        if installed_files[PLUGIN_MANIFEST] != expected_manifest_raw:
            errors.append(
                "installed manifest contains changes beyond the canonical cachebuster"
            )
        mode = "manifest-version-cachebuster-only"

    if not isinstance(parity, dict) or not isinstance(
        parity.get("source_to_installed"), dict
    ):
        errors.append("coordinator source_to_installed parity is unavailable")
    else:
        source_to_installed = parity["source_to_installed"]
        if source_to_installed.get("mode") != mode:
            errors.append(
                "coordinator source_to_installed mode differs from inspected provenance"
            )
        if source_to_installed.get("file_count") != len(committed_files):
            errors.append(
                "coordinator source_to_installed file count differs from inspected provenance"
            )
    return errors


def validate_grader_source(
    root: Path,
    expected_source_revision: str | None,
    contract_raw: bytes,
    checker_raw: bytes,
) -> list[str]:
    """Bind grading policy to one clean, exact source commit."""
    errors: list[str] = []
    if not isinstance(expected_source_revision, str) or not SOURCE_REVISION.fullmatch(
        expected_source_revision
    ):
        return ["sealed grading requires a valid expected source revision"]

    top_level_raw, top_level_error = git_command(root, "rev-parse", "--show-toplevel")
    if top_level_error is not None or top_level_raw is None:
        return ["sealed grading root must be an inspectable Git working tree"]
    try:
        top_level = Path(top_level_raw.decode("utf-8").strip()).resolve()
    except UnicodeError:
        return ["sealed grading Git top-level is not valid UTF-8"]
    if top_level != root:
        errors.append("sealed grading root must be the exact Git top-level")

    current_head_raw, current_head_error = git_command(root, "rev-parse", "HEAD")
    expected_commit_raw, expected_commit_error = git_command(
        root,
        "rev-parse",
        "--verify",
        f"{expected_source_revision}^{{commit}}",
    )
    current_head = (
        current_head_raw.decode("ascii").strip()
        if current_head_error is None and current_head_raw is not None
        else None
    )
    expected_commit = (
        expected_commit_raw.decode("ascii").strip()
        if expected_commit_error is None and expected_commit_raw is not None
        else None
    )
    if current_head is None or expected_commit is None:
        errors.append("sealed grading source revision cannot be resolved")
    else:
        if expected_source_revision != expected_commit:
            errors.append("sealed grading requires the full resolved source revision")
        if current_head != expected_commit:
            errors.append("sealed grading Git HEAD differs from the expected source revision")

    status_raw, status_error = git_command(
        root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--ignore-submodules=none",
    )
    if status_error is not None or status_raw is None:
        errors.append("sealed grading source status cannot be inspected")
    elif status_raw:
        errors.append("sealed grading source must be clean")

    expected_checker = (root / "scripts" / "check_route_receipts.py").resolve()
    if Path(__file__).resolve() != expected_checker:
        errors.append("sealed grading must execute the checker from the grading root")

    if expected_commit is not None:
        for relative, snapshot, label in (
            ("tests/route-contracts.json", contract_raw, "route contracts"),
            ("scripts/check_route_receipts.py", checker_raw, "receipt checker"),
        ):
            committed_raw, committed_error = git_command(
                root,
                "cat-file",
                "blob",
                f"{expected_commit}:{relative}",
            )
            if committed_error is not None or committed_raw is None:
                errors.append(f"sealed grading committed {label} cannot be inspected")
            elif committed_raw != snapshot:
                errors.append(
                    f"sealed grading {label} bytes differ from the expected source revision"
                )
    return errors


def parse_utc_second(value: object, label: str) -> tuple[datetime | None, list[str]]:
    if not isinstance(value, str):
        return None, [f"{label} must be a UTC ISO-8601 timestamp"]
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None, [f"{label} must be a UTC ISO-8601 timestamp"]
    return parsed, []


def validate_sha256(value: object, label: str) -> list[str]:
    if not isinstance(value, str) or not SHA256.fullmatch(value):
        return [f"{label} must be a SHA-256 digest"]
    return []


def validate_public_capture_values(value: object, label: str = "coordinator capture") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"path", "root", "resolved_target", "internal_task_id"}:
                errors.append(f"{label} exposes prohibited private field {key}")
            errors.extend(validate_public_capture_values(item, f"{label}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(validate_public_capture_values(item, f"{label}[{index}]"))
    elif isinstance(value, str):
        if value.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", value):
            errors.append(f"{label} exposes an absolute filesystem path")
        if INTERNAL_UUID.search(value):
            errors.append(f"{label} exposes an internal task identifier")
    return errors


def validate_coordinator_plugin_identity(
    value: object,
    expected_fields: set[str],
    label: str,
) -> list[str]:
    if not isinstance(value, dict):
        return [f"{label} must be an object"]
    errors = exact_field_errors(value, expected_fields, label)
    if value.get("name") != "project-delivery":
        errors.append(f"{label} name must be project-delivery")
    if not isinstance(value.get("version"), str) or not value["version"].strip():
        errors.append(f"{label} version must be non-empty")
    if value.get("payload_hash_method") != INSTALLED_PAYLOAD_HASH_METHOD:
        errors.append(f"{label} payload hash method is invalid")
    for field in ("manifest_sha256", "payload_sha256"):
        errors.extend(validate_sha256(value.get(field), f"{label} {field}"))
    for field in ("file_count", "directory_count"):
        if not isinstance(value.get(field), int) or value[field] < 1:
            errors.append(f"{label} {field} must be a positive integer")
    return errors


def validate_coordinator_parity(
    value: object,
    identities: dict[str, object],
) -> list[str]:
    if not isinstance(value, dict):
        return ["coordinator parity must be an object"]
    errors = exact_field_errors(value, COORDINATOR_PARITY_FIELDS, "coordinator parity")
    source = identities.get("source_package")
    prepared = identities.get("prepared_personal_source")
    installed = identities.get("installed_cache")
    if not all(isinstance(item, dict) for item in (source, prepared, installed)):
        return errors + ["coordinator parity cannot bind invalid plugin identities"]
    assert isinstance(source, dict)
    assert isinstance(prepared, dict)
    assert isinstance(installed, dict)

    source_prepared = value.get("source_to_prepared")
    if not isinstance(source_prepared, dict):
        errors.append("coordinator source_to_prepared parity must be an object")
    else:
        mode = source_prepared.get("mode")
        expected = {
            "file_count",
            "mode",
            "prepared_payload_sha256",
            "source_payload_sha256",
        }
        if mode == "manifest-version-cachebuster-only":
            expected |= {"prepared_version", "source_version"}
        elif mode != "exact-byte-parity":
            errors.append("coordinator source_to_prepared parity mode is invalid")
        errors.extend(
            exact_field_errors(
                source_prepared, expected, "coordinator source_to_prepared parity"
            )
        )
        if source_prepared.get("source_payload_sha256") != source.get("payload_sha256"):
            errors.append("coordinator source_to_prepared source payload is unbound")
        if source_prepared.get("prepared_payload_sha256") != prepared.get("payload_sha256"):
            errors.append("coordinator source_to_prepared prepared payload is unbound")
        if mode == "manifest-version-cachebuster-only" and (
            source_prepared.get("source_version") != source.get("version")
            or source_prepared.get("prepared_version") != prepared.get("version")
        ):
            errors.append("coordinator source_to_prepared versions are unbound")

    prepared_installed = value.get("prepared_to_installed")
    if not isinstance(prepared_installed, dict):
        errors.append("coordinator prepared_to_installed parity must be an object")
    else:
        errors.extend(
            exact_field_errors(
                prepared_installed,
                {"file_count", "mode", "payload_sha256"},
                "coordinator prepared_to_installed parity",
            )
        )
        if prepared_installed.get("mode") != "exact-byte-parity":
            errors.append("coordinator prepared_to_installed parity must be exact")
        if prepared_installed.get("payload_sha256") not in {
            prepared.get("payload_sha256"),
            installed.get("payload_sha256"),
        } or prepared.get("payload_sha256") != installed.get("payload_sha256"):
            errors.append("coordinator prepared/installed payload parity is unbound")

    source_installed = value.get("source_to_installed")
    if not isinstance(source_installed, dict):
        errors.append("coordinator source_to_installed parity must be an object")
    else:
        mode = source_installed.get("mode")
        expected = {
            "file_count",
            "installed_payload_sha256",
            "mode",
            "source_payload_sha256",
        }
        if mode == "manifest-version-cachebuster-only":
            expected |= {"installed_version", "source_version"}
        elif mode != "exact-byte-parity":
            errors.append("coordinator source_to_installed parity mode is invalid")
        errors.extend(
            exact_field_errors(
                source_installed, expected, "coordinator source_to_installed parity"
            )
        )
        if source_installed.get("source_payload_sha256") != source.get("payload_sha256"):
            errors.append("coordinator source_to_installed source payload is unbound")
        if source_installed.get("installed_payload_sha256") != installed.get("payload_sha256"):
            errors.append("coordinator source_to_installed installed payload is unbound")
        if mode == "manifest-version-cachebuster-only" and (
            source_installed.get("source_version") != source.get("version")
            or source_installed.get("installed_version") != installed.get("version")
        ):
            errors.append("coordinator source_to_installed versions are unbound")
    return errors


def validate_prompt_manifest_binding(
    raw: bytes,
    public_identity: object,
    receipts: dict[str, object],
) -> tuple[list[str], str]:
    errors: list[str] = []
    try:
        prompt_manifest = json_from_bytes(raw)
    except (UnicodeError, json.JSONDecodeError, DuplicateJSONKey) as error:
        return [f"sealed prompt manifest cannot be inspected: {error}"], "unknown"
    digest = sha256_bytes(raw)
    if not isinstance(public_identity, dict):
        return ["coordinator prompt_manifest must be an object"], digest
    errors.extend(
        exact_field_errors(
            public_identity, COORDINATOR_PROMPT_FIELDS, "coordinator prompt_manifest"
        )
    )
    if public_identity.get("sha256") != digest:
        errors.append("coordinator prompt manifest SHA-256 does not match exact bytes")
    if public_identity.get("byte_count") != len(raw):
        errors.append("coordinator prompt manifest byte count does not match exact bytes")
    if public_identity.get("hash_method") != RAW_HASH_METHOD:
        errors.append("coordinator prompt manifest hash method is invalid")
    if not isinstance(prompt_manifest, dict):
        return errors + ["sealed prompt manifest root must be an object"], digest
    errors.extend(
        exact_field_errors(
            prompt_manifest,
            {
                "evidence_class",
                "scenarios",
                "schema_version",
                "source_contract_schema_version",
            },
            "sealed prompt manifest",
        )
    )
    if (
        prompt_manifest.get("schema_version") != 1
        or prompt_manifest.get("source_contract_schema_version") != 3
        or prompt_manifest.get("evidence_class") != "prompt-only blind canary input"
    ):
        errors.append("sealed prompt manifest protocol identity is invalid")
    prompt_scenarios = prompt_manifest.get("scenarios")
    receipt_scenarios = receipts.get("scenarios")
    if not isinstance(prompt_scenarios, list) or not isinstance(receipt_scenarios, list):
        errors.append("sealed prompt and receipt scenario lists must be arrays")
    else:
        expected: list[dict[str, object]] = []
        for index, scenario in enumerate(receipt_scenarios, 1):
            if not isinstance(scenario, dict):
                errors.append(f"receipt scenario {index} cannot bind to prompt manifest")
                continue
            expected.append({"id": scenario.get("id"), "prompt": scenario.get("prompt")})
        if prompt_scenarios != expected:
            errors.append("sealed prompt manifest does not exactly match receipt IDs/prompts")
        for index, scenario in enumerate(prompt_scenarios, 1):
            if not isinstance(scenario, dict):
                errors.append(f"sealed prompt scenario {index} must be an object")
            else:
                errors.extend(
                    exact_field_errors(
                        scenario, {"id", "prompt"}, f"sealed prompt scenario {index}"
                    )
                )
    return errors, digest


def validate_coordinator_binding(
    root: Path,
    receipts: dict[str, object],
    receipt_raw: bytes,
    installed_files: dict[Path, bytes] | None,
    attestation_path: Path | None,
    expected_attestation_sha256: str | None,
    prompt_path: Path | None,
    task_prompt_path: Path | None,
    expected_source_revision: str | None,
) -> tuple[list[str], dict[str, str]]:
    errors: list[str] = []
    evidence = {
        "coordinator_attestation_sha256": "unknown",
        "prompt_manifest_sha256": "unknown",
        "raw_observation_sha256": "unknown",
        "task_prompt_sha256": "unknown",
    }
    if attestation_path is None:
        return ["sealed schema-v3 candidate proof requires --coordinator-attestation"], evidence
    if prompt_path is None:
        return ["sealed schema-v3 candidate proof requires --prompt-manifest"], evidence
    if task_prompt_path is None:
        return ["sealed schema-v3 candidate proof requires --task-prompt"], evidence

    attestation_raw, attestation_read_errors = read_regular_bytes(
        attestation_path, "coordinator attestation"
    )
    prompt_raw, prompt_read_errors = read_regular_bytes(
        prompt_path, "sealed prompt manifest"
    )
    task_prompt_raw, task_prompt_read_errors = read_regular_bytes(
        task_prompt_path, "canonical task prompt"
    )
    errors.extend(attestation_read_errors)
    errors.extend(prompt_read_errors)
    errors.extend(task_prompt_read_errors)
    if attestation_raw is None or prompt_raw is None or task_prompt_raw is None:
        return errors, evidence
    try:
        capture = json_from_bytes(attestation_raw)
    except (UnicodeError, json.JSONDecodeError, DuplicateJSONKey) as error:
        return [f"coordinator attestation cannot be inspected: {error}"], evidence
    attestation_digest = sha256_bytes(attestation_raw)
    evidence["coordinator_attestation_sha256"] = attestation_digest
    errors.extend(
        validate_sha256(
            expected_attestation_sha256, "expected coordinator attestation SHA-256"
        )
    )
    if expected_attestation_sha256 != attestation_digest:
        errors.append(
            "coordinator attestation bytes do not match the externally retained SHA-256"
        )
    if not isinstance(capture, dict):
        return errors + ["coordinator attestation root must be an object"], evidence
    errors.extend(exact_field_errors(capture, CAPTURE_FIELDS, "coordinator attestation"))
    errors.extend(validate_public_capture_values(capture))
    if (
        capture.get("schema_version") != 1
        or capture.get("protocol") != COORDINATOR_PROTOCOL
        or capture.get("evidence_class") != CAPTURE_EVIDENCE_CLASS
    ):
        errors.append("coordinator attestation protocol identity is invalid")
    if capture.get("coordinator_attestation") != COORDINATOR_ATTESTATION:
        errors.append("coordinator attestation statement or limitations were changed")

    nonce = capture.get("public_run_nonce")
    slug = capture.get("public_receipt_slug")
    if not isinstance(nonce, str) or not PUBLIC_NONCE.fullmatch(nonce):
        errors.append("coordinator public run nonce is invalid")
    if not isinstance(slug, str) or not PUBLIC_RECEIPT.fullmatch(slug):
        errors.append("coordinator public receipt slug is invalid")
    if isinstance(nonce, str) and isinstance(slug, str) and not slug.endswith(
        nonce.removeprefix("canary-")[:12]
    ):
        errors.append("coordinator public receipt slug is not nonce-bound")
    for field in (
        "launch_state_sha256",
        "private_task_binding_sha256",
    ):
        errors.extend(validate_sha256(capture.get(field), f"coordinator {field}"))

    launch_time, launch_errors = parse_utc_second(
        capture.get("launch_time_utc"), "coordinator launch_time_utc"
    )
    captured_at, capture_time_errors = parse_utc_second(
        capture.get("captured_at_utc"), "coordinator captured_at_utc"
    )
    errors.extend(launch_errors)
    errors.extend(capture_time_errors)
    if launch_time is not None and captured_at is not None:
        elapsed = (captured_at - launch_time).total_seconds()
        if elapsed < 0 or elapsed > MAX_CAPTURE_AGE_SECONDS:
            errors.append("coordinator capture is outside the permitted six-hour window")

    raw_observation = capture.get("raw_observation")
    receipt_raw_digest = sha256_bytes(receipt_raw)
    evidence["raw_observation_sha256"] = receipt_raw_digest
    if not isinstance(raw_observation, dict):
        errors.append("coordinator raw_observation must be an object")
    else:
        errors.extend(
            exact_field_errors(
                raw_observation, COORDINATOR_RAW_FIELDS, "coordinator raw_observation"
            )
        )
        if raw_observation.get("sha256") != receipt_raw_digest:
            errors.append("coordinator raw observation SHA-256 does not match receipt bytes")
        if raw_observation.get("byte_count") != len(receipt_raw):
            errors.append("coordinator raw observation byte count does not match receipt bytes")
        if raw_observation.get("hash_method") != RAW_HASH_METHOD:
            errors.append("coordinator raw observation hash method is invalid")

    prompt_errors, prompt_digest = validate_prompt_manifest_binding(
        prompt_raw, capture.get("prompt_manifest"), receipts
    )
    errors.extend(prompt_errors)
    evidence["prompt_manifest_sha256"] = prompt_digest

    source_git = capture.get("source_git")
    if not isinstance(source_git, dict):
        errors.append("coordinator source_git must be an object")
        source_git = {}
    else:
        errors.extend(
            exact_field_errors(
                source_git, COORDINATOR_SOURCE_GIT_FIELDS, "coordinator source_git"
            )
        )
    if source_git.get("clean") is not True or source_git.get("status_byte_count") != 0:
        errors.append("coordinator source Git identity is not clean")
    if source_git.get("status_sha256") != sha256_bytes(b""):
        errors.append("coordinator source Git empty-status digest is invalid")
    source_head = source_git.get("head")
    if not isinstance(source_head, str) or not SOURCE_REVISION.fullmatch(source_head):
        errors.append("coordinator source Git HEAD is invalid")
    if source_head != expected_source_revision:
        errors.append("coordinator source Git HEAD differs from expected source revision")

    identities = capture.get("plugin_identities")
    if not isinstance(identities, dict):
        errors.append("coordinator plugin_identities must be an object")
        identities = {}
    else:
        errors.extend(
            exact_field_errors(
                identities,
                COORDINATOR_PLUGIN_IDENTITIES_FIELDS,
                "coordinator plugin_identities",
            )
        )
    for label in ("source_package", "prepared_personal_source"):
        errors.extend(
            validate_coordinator_plugin_identity(
                identities.get(label), COORDINATOR_PLUGIN_IDENTITY_FIELDS, label
            )
        )
    errors.extend(
        validate_coordinator_plugin_identity(
            identities.get("installed_cache"),
            COORDINATOR_INSTALLED_IDENTITY_FIELDS,
            "installed_cache",
        )
    )
    errors.extend(validate_coordinator_parity(capture.get("parity"), identities))
    errors.extend(
        validate_source_installed_provenance(
            root,
            expected_source_revision,
            installed_files,
            identities,
            capture.get("parity"),
        )
    )

    installed_identity = identities.get("installed_cache")
    plugin_identity = receipts.get("plugin_identity")
    if not isinstance(installed_identity, dict) or not isinstance(plugin_identity, dict):
        errors.append("coordinator and receipt plugin identities must be objects")
    else:
        identity_mapping = {
            "name": "name",
            "installed_version": "version",
            "manifest_sha256": "manifest_sha256",
            "payload_sha256": "payload_sha256",
            "payload_hash_method": "payload_hash_method",
            "cache_relative_path": "cache_relative_path",
        }
        for receipt_field, capture_field in identity_mapping.items():
            if plugin_identity.get(receipt_field) != installed_identity.get(capture_field):
                errors.append(
                    f"receipt plugin_identity {receipt_field} is not coordinator-bound"
                )
        if plugin_identity.get("source_revision") != source_head:
            errors.append("receipt plugin_identity source_revision is not coordinator-bound")

    task_prompt_identity = capture.get("task_prompt")
    if not isinstance(task_prompt_identity, dict):
        errors.append("coordinator task_prompt must be an object")
    else:
        errors.extend(
            exact_field_errors(
                task_prompt_identity,
                COORDINATOR_TASK_PROMPT_FIELDS,
                "coordinator task_prompt",
            )
        )
    task_prompt_digest = sha256_bytes(task_prompt_raw)
    evidence["task_prompt_sha256"] = task_prompt_digest
    if isinstance(task_prompt_identity, dict):
        if task_prompt_identity.get("sha256") != task_prompt_digest:
            errors.append(
                "coordinator task prompt SHA-256 does not match exact bytes"
            )
        if task_prompt_identity.get("byte_count") != len(task_prompt_raw):
            errors.append(
                "coordinator task prompt byte count does not match exact bytes"
            )
        if task_prompt_identity.get("hash_method") != RAW_HASH_METHOD:
            errors.append("coordinator task prompt hash method is invalid")
        if task_prompt_identity.get("prompt_protocol") != TASK_PROMPT_PROTOCOL:
            errors.append("coordinator task prompt protocol is invalid")
    if isinstance(installed_identity, dict) and isinstance(source_git, dict):
        try:
            expected_task_prompt = render_task_prompt(
                prompt_raw,
                str(nonce),
                str(slug),
                source_git,
                installed_identity,
            )
        except (KeyError, TypeError, ValueError) as error:
            errors.append(
                f"canonical task prompt cannot be reconstructed: {error}"
            )
        else:
            if task_prompt_raw != expected_task_prompt:
                errors.append(
                    "task prompt bytes do not match the canonical blind prompt"
                )

    marketplace = capture.get("marketplace_entry")
    if not isinstance(marketplace, dict):
        errors.append("coordinator marketplace_entry must be an object")
        marketplace = {}
    else:
        errors.extend(
            exact_field_errors(
                marketplace,
                COORDINATOR_MARKETPLACE_FIELDS,
                "coordinator marketplace_entry",
            )
        )
    for field in ("file_sha256", "entry_sha256", "target_payload_sha256"):
        errors.extend(validate_sha256(marketplace.get(field), f"marketplace {field}"))
    if (
        marketplace.get("plugin_name") != "project-delivery"
        or marketplace.get("source_type") != "local"
    ):
        errors.append("coordinator marketplace entry identity is invalid")
    if isinstance(installed_identity, dict):
        if marketplace.get("marketplace_name") != installed_identity.get("marketplace"):
            errors.append("coordinator marketplace/cache names are not bound")
        prepared_identity = identities.get("prepared_personal_source")
        if isinstance(prepared_identity, dict) and (
            marketplace.get("target_payload_sha256")
            != prepared_identity.get("payload_sha256")
        ):
            errors.append("coordinator marketplace target payload is not bound")
    source_path = marketplace.get("source_path")
    if not isinstance(source_path, str) or Path(source_path).is_absolute() or ".." in Path(source_path).parts:
        errors.append("coordinator marketplace source_path must be portable and relative")

    boundary = capture.get("observation_boundary")
    if not isinstance(boundary, dict):
        errors.append("coordinator observation_boundary must be an object")
        boundary = {}
    else:
        errors.extend(
            exact_field_errors(
                boundary, COORDINATOR_BOUNDARY_FIELDS, "coordinator observation_boundary"
            )
        )
    if (
        boundary.get("mode") != "projectless"
        or boundary.get("repository_name") != "not-applicable"
        or boundary.get("revision") != "not-applicable"
        or boundary.get("working_tree_state") != "no-repository"
    ):
        errors.append("coordinator observation boundary is not projectless")
    instruction_files = boundary.get("instruction_files")
    if not isinstance(instruction_files, list) or not instruction_files:
        errors.append("coordinator observation boundary lacks instruction evidence")
    else:
        seen_instruction_labels: set[str] = set()
        for index, instruction in enumerate(instruction_files, 1):
            if not isinstance(instruction, dict):
                errors.append(f"coordinator instruction evidence {index} must be an object")
                continue
            errors.extend(
                exact_field_errors(
                    instruction,
                    COORDINATOR_INSTRUCTION_FIELDS,
                    f"coordinator instruction evidence {index}",
                )
            )
            label = instruction.get("label")
            if not isinstance(label, str) or not label.strip() or label in seen_instruction_labels:
                errors.append(f"coordinator instruction evidence {index} has invalid label")
            else:
                seen_instruction_labels.add(label)
            errors.extend(
                validate_sha256(
                    instruction.get("sha256"),
                    f"coordinator instruction evidence {index} sha256",
                )
            )
            if instruction.get("hash_method") != RAW_HASH_METHOD:
                errors.append(f"coordinator instruction evidence {index} hash method is invalid")
            if not isinstance(instruction.get("byte_count"), int) or instruction["byte_count"] < 1:
                errors.append(f"coordinator instruction evidence {index} byte count is invalid")

    task_identity = receipts.get("task_identity")
    if not isinstance(task_identity, dict):
        errors.append("receipt task_identity must be an object for coordinator binding")
    else:
        if task_identity.get("public_receipt_id") != slug:
            errors.append("receipt public_receipt_id is not coordinator-bound")
        selected_at, selected_errors = parse_utc_second(
            task_identity.get("selected_at"), "receipt task selected_at"
        )
        errors.extend(selected_errors)
        if (
            selected_at is not None
            and launch_time is not None
            and captured_at is not None
            and not (launch_time <= selected_at <= captured_at)
        ):
            errors.append("receipt selected_at is outside the sealed launch/capture window")

    repository_identity = receipts.get("repository_identity")
    if not isinstance(repository_identity, dict):
        errors.append("receipt repository_identity must be an object for coordinator binding")
    elif (
        repository_identity.get("name") != "projectless-canary"
        or repository_identity.get("revision") != boundary.get("revision")
        or repository_identity.get("working_tree_state")
        != boundary.get("working_tree_state")
    ):
        errors.append("receipt repository identity is not bound to projectless observation")
    return errors, evidence


def normalize_skill(value: str) -> str:
    prefix = "project-delivery:"
    return value[len(prefix) :] if value.startswith(prefix) else value


def validate_string_list(value: object, *, require_nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not require_nonempty)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def dotted_path_exists(value: object, path: object) -> bool:
    """Return whether a non-empty dotted dictionary path exists in value."""
    if (
        not isinstance(path, str)
        or not path
        or path.startswith(".")
        or path.endswith(".")
    ):
        return False
    current = value
    for part in path.split("."):
        if not part or not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    return True


def dotted_paths_related(left: str, right: str) -> bool:
    """Treat an exact path, an ancestor, or a descendant as structurally related."""
    return (
        left == right
        or left.startswith(f"{right}.")
        or right.startswith(f"{left}.")
    )


def has_linked_gap(
    gaps: object,
    related_path: str,
    evidence: object,
) -> bool:
    """Require a structurally related gap whose ID is cited by the disposition."""
    if not isinstance(gaps, list) or not validate_string_list(
        evidence, require_nonempty=True
    ):
        return False
    evidence_text = "\n".join(evidence)
    for gap in gaps:
        if not isinstance(gap, dict):
            continue
        gap_id = gap.get("id")
        gap_path = gap.get("related_field")
        if (
            isinstance(gap_id, str)
            and GAP_ID.fullmatch(gap_id)
            and isinstance(gap_path, str)
            and dotted_paths_related(gap_path, related_path)
            and re.search(
                rf"(?<![A-Z0-9-]){re.escape(gap_id)}(?![A-Z0-9-])",
                evidence_text,
            )
        ):
            return True
    return False


def exact_field_errors(
    value: dict[str, object],
    expected: set[str],
    label: str,
) -> list[str]:
    errors: list[str] = []
    missing = expected.difference(value)
    extra = set(value).difference(expected)
    if missing:
        errors.append(f"{label} missing fields: " + ", ".join(sorted(missing)))
    if extra:
        errors.append(
            f"{label} has unsupported fields: " + ", ".join(sorted(extra))
        )
    return errors


def required_instruction_paths(
    plugin_root: Path,
    skill: str,
) -> tuple[set[str], list[str]]:
    skill_relative = Path("skills") / skill / "SKILL.md"
    skill_path = plugin_root / skill_relative
    try:
        text = safe_read_text(skill_path, root=plugin_root, max_bytes=MAX_TEXT_BYTES)
    except (OSError, UnicodeError) as error:
        return {skill_relative.as_posix()}, [
            f"loaded specialist {skill} instruction closure cannot be derived: {error}"
        ]
    required = {skill_relative.as_posix()}
    errors: list[str] = []
    for reference in BACKTICKED_SHARED_REFERENCE.findall(text):
        resolved = Path(os.path.abspath(skill_path.parent / reference))
        try:
            relative = resolved.relative_to(plugin_root.absolute())
        except ValueError:
            errors.append(
                f"loaded specialist {skill} instruction reference escapes the installed plugin: {reference}"
            )
            continue
        try:
            safe_read_bytes(resolved, root=plugin_root, max_bytes=MAX_TEXT_BYTES)
        except OSError as error:
            errors.append(
                f"loaded specialist {skill} instruction reference cannot be read: {relative.as_posix()}: {error}"
            )
            continue
        required.add(relative.as_posix())
    return required, errors


def last_index(values: list[str], target: str) -> int:
    return len(values) - 1 - values[::-1].index(target)


def fresh_observation_sha256(receipts: dict[str, object]) -> str:
    if receipts.get("schema_version") == 3:
        observation = {
            field: receipts.get(field)
            for field in sorted(FRESH_V3_TOP_LEVEL_FIELDS - {"task_identity"})
        }
    else:
        observation = {
            field: receipts.get(field) for field in FRESH_OBSERVATION_HASH_FIELDS
        }
    canonical = json.dumps(
        observation,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_installed_identity(
    plugin_identity: dict[str, object],
    installed_plugin_root: Path | None,
    expected_source_revision: str | None,
    require_cache_shape: bool = False,
) -> list[str]:
    errors: list[str] = []
    if installed_plugin_root is None:
        return ["fresh-task evidence requires --installed-plugin-root"]
    if not installed_plugin_root.is_dir():
        return [f"installed plugin root is not a directory: {installed_plugin_root}"]
    if (
        not isinstance(expected_source_revision, str)
        or not SOURCE_REVISION.fullmatch(expected_source_revision)
    ):
        errors.append(
            "fresh-task evidence requires a hexadecimal --expected-source-revision"
        )
    elif plugin_identity.get("source_revision") != expected_source_revision:
        errors.append(
            "plugin_identity source_revision does not match the expected release revision"
        )

    manifest_path = installed_plugin_root / ".codex-plugin" / "plugin.json"
    try:
        manifest_bytes = safe_read_bytes(manifest_path, root=installed_plugin_root)
        manifest = json_from_bytes(manifest_bytes)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateJSONKey) as error:
        return errors + [f"installed plugin manifest cannot be inspected: {error}"]
    if not isinstance(manifest, dict):
        return errors + ["installed plugin manifest root must be an object"]

    if plugin_identity.get("name") != manifest.get("name"):
        errors.append("plugin_identity name does not match the installed manifest")
    if plugin_identity.get("installed_version") != manifest.get("version"):
        errors.append(
            "plugin_identity installed_version does not match the installed manifest"
        )
    manifest_digest = hashlib.sha256(manifest_bytes).hexdigest()
    if plugin_identity.get("manifest_sha256") != manifest_digest:
        errors.append(
            "plugin_identity manifest_sha256 does not match the installed manifest"
        )

    try:
        selected = sorted(select_paths(installed_plugin_root))
        boundary_errors = validate_source_boundary(installed_plugin_root, selected)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        errors.append(f"installed plugin payload cannot be inspected: {error}")
    else:
        errors.extend(
            f"installed plugin identity: {error}" for error in boundary_errors
        )
        if not boundary_errors:
            installed_payload_digest = payload_sha256(installed_plugin_root, selected)
            if plugin_identity.get("payload_sha256") != installed_payload_digest:
                errors.append(
                    "plugin_identity payload_sha256 does not match the installed payload"
                )

    if plugin_identity.get("payload_hash_method") != INSTALLED_PAYLOAD_HASH_METHOD:
        errors.append(
            "plugin_identity payload_hash_method does not match the canonical method"
        )
    cache_relative_path = plugin_identity.get("cache_relative_path")
    if isinstance(cache_relative_path, str) and cache_relative_path.strip():
        claimed_parts = Path(cache_relative_path).parts
        actual_parts = installed_plugin_root.parts
        if (
            len(claimed_parts) > len(actual_parts)
            or actual_parts[-len(claimed_parts) :] != claimed_parts
        ):
            errors.append(
                "plugin_identity cache_relative_path does not match the inspected root"
            )
        if require_cache_shape:
            version = plugin_identity.get("installed_version")
            expected_tail = (
                "plugins",
                "cache",
                claimed_parts[2] if len(claimed_parts) >= 5 else "",
                "project-delivery",
                version,
            )
            if (
                len(claimed_parts) != 5
                or claimed_parts[0:2] != ("plugins", "cache")
                or claimed_parts[3] != "project-delivery"
                or claimed_parts[4] != version
                or tuple(actual_parts[-5:]) != expected_tail
            ):
                errors.append(
                    "sealed fresh evidence requires an exact cache-shaped installed root"
                )
    return errors


def validate(
    root: Path,
    receipt_path: Path,
    allow_subset: bool = False,
    allow_historical_annotations: bool = False,
    allow_unsealed_fresh: bool = False,
    installed_plugin_root: Path | None = None,
    expected_source_revision: str | None = None,
    contracts_snapshot: dict[str, object] | None = None,
    receipts_snapshot: dict[str, object] | None = None,
) -> tuple[list[str], int, str]:
    errors: list[str] = []
    plugin_root = root / "plugins" / "project-delivery"
    if not plugin_root.is_dir():
        plugin_root = root
    contracts = contracts_snapshot
    receipts = receipts_snapshot
    if contracts is None:
        contracts, contract_errors = read_json(
            root / "tests" / "route-contracts.json", "route contracts", root=root
        )
        errors.extend(contract_errors)
    if receipts is None:
        receipts, receipt_errors = read_json(receipt_path, "route receipts")
        errors.extend(receipt_errors)
    if contracts is None or receipts is None:
        return errors, 0, "unknown"

    if receipts.get("evidence_class") == FRESH_EVIDENCE_CLASS:
        _, installed_errors = snapshot_installed_plugin(installed_plugin_root)
        if installed_errors:
            return errors + installed_errors, 0, FRESH_EVIDENCE_CLASS

    if contracts.get("schema_version") != 3:
        errors.append("route contracts must use schema version 3")
    if receipts.get("schema_version") not in {2, 3}:
        errors.append("route receipts must use historical schema 2 or sealed schema 3")
    evidence_class = receipts.get("evidence_class")
    if evidence_class not in {FRESH_EVIDENCE_CLASS, HISTORICAL_EVIDENCE_CLASS}:
        errors.append("receipts have an unsupported evidence class")
        evidence_class = "unknown"
    is_fresh = evidence_class == FRESH_EVIDENCE_CLASS
    is_fresh_v3 = is_fresh and receipts.get("schema_version") == 3
    is_unsealed_fresh_v2 = is_fresh and receipts.get("schema_version") == 2
    comparison_contracts = contracts
    if evidence_class == HISTORICAL_EVIDENCE_CLASS:
        historical_contracts, historical_contract_errors = read_json(
            root / HISTORICAL_CONTRACT_FIXTURE,
            "historical route contracts", root=root,
        )
        errors.extend(historical_contract_errors)
        if historical_contracts is not None:
            if historical_contracts.get("schema_version") != 2:
                errors.append("historical route contracts must use schema version 2")
            comparison_contracts = historical_contracts
    expected_contract_schema = (
        2
        if evidence_class == HISTORICAL_EVIDENCE_CLASS
        else contracts.get("schema_version")
    )
    if receipts.get("contract_schema_version") != expected_contract_schema:
        errors.append("receipt contract_schema_version does not match its evidence profile")
    if is_unsealed_fresh_v2 and not allow_unsealed_fresh:
        errors.append(
            "schema-v2 fresh self-attestation requires --allow-unsealed-fresh and cannot establish candidate proof"
        )
    if evidence_class == HISTORICAL_EVIDENCE_CLASS and receipts.get("schema_version") != 2:
        errors.append("historical route evidence must use schema version 2")
    all_semantics_blind = receipts.get(
        "semantic_fields_were_frozen_before_contract_comparison"
    )
    freeze_scope_value = receipts.get("semantic_freeze_scope")
    freeze_scope = set(freeze_scope_value) if validate_string_list(freeze_scope_value) else set()
    if not validate_string_list(freeze_scope_value):
        errors.append("semantic_freeze_scope must be a string list")
    elif len(freeze_scope) != len(freeze_scope_value):
        errors.append("semantic_freeze_scope must not contain duplicates")
    if not validate_string_list(
        receipts.get("semantic_freeze_evidence"), require_nonempty=True
    ):
        errors.append("receipts must include semantic freeze evidence")
    annotation_provenance = receipts.get("annotation_provenance")
    if is_fresh_v3:
        if not isinstance(annotation_provenance, dict):
            errors.append("sealed schema-v3 annotation_provenance must be an object")
        else:
            errors.extend(
                exact_field_errors(
                    annotation_provenance,
                    FRESH_V3_ANNOTATION_PROVENANCE_FIELDS,
                    "annotation_provenance",
                )
            )
            if (
                annotation_provenance.get("semantic_fields_origin")
                != "blind-before-contract-comparison"
            ):
                errors.append(
                    "annotation_provenance semantic_fields_origin must be blind-before-contract-comparison"
                )
            if annotation_provenance.get("contract_access") != "after-capture-only":
                errors.append(
                    "annotation_provenance contract_access must be after-capture-only"
                )
            if annotation_provenance.get("semantic_fields_revised_after_comparison") is not False:
                errors.append(
                    "annotation_provenance must deny post-comparison semantic revision"
                )
            allowed_enrichment = {
                "plugin_identity",
                "repository_identity",
                "task_identity.public_receipt_id",
                "task_identity.selected_at",
                "task_identity.source_observation_sha256",
            }
            enrichment = annotation_provenance.get("post_freeze_enrichment_fields")
            if not validate_string_list(enrichment):
                errors.append(
                    "annotation_provenance post_freeze_enrichment_fields must be a string list"
                )
            elif len(enrichment) != len(set(enrichment)):
                errors.append(
                    "annotation_provenance post_freeze_enrichment_fields must be unique"
                )
            elif set(enrichment).difference(allowed_enrichment):
                errors.append(
                    "annotation_provenance names unsupported post-freeze enrichment fields: "
                    + ", ".join(sorted(set(enrichment).difference(allowed_enrichment)))
                )
    elif not isinstance(annotation_provenance, str) or not annotation_provenance.strip():
        errors.append("receipts must explain annotation provenance")
    if is_fresh:
        expected_top_level = (
            FRESH_V3_TOP_LEVEL_FIELDS if is_fresh_v3 else FRESH_TOP_LEVEL_FIELDS
        )
        missing_top_level = expected_top_level.difference(receipts)
        extra_top_level = set(receipts).difference(expected_top_level)
        if missing_top_level:
            errors.append(
                "fresh-task envelope missing fields: "
                + ", ".join(sorted(missing_top_level))
            )
        if extra_top_level:
            errors.append(
                "fresh-task envelope has unsupported fields: "
                + ", ".join(sorted(extra_top_level))
            )
        if all_semantics_blind is not True:
            errors.append(
                "fresh-task evidence requires all semantic fields frozen before contract comparison"
            )
        expected_freeze_scope = (
            FRESH_V3_SEMANTIC_FREEZE_FIELDS
            if is_fresh_v3
            else FRESH_SEMANTIC_FREEZE_FIELDS
        )
        if freeze_scope != expected_freeze_scope:
            missing_scope = expected_freeze_scope.difference(freeze_scope)
            extra_scope = freeze_scope.difference(expected_freeze_scope)
            if missing_scope:
                errors.append(
                    "fresh-task semantic freeze omits fields: "
                    + ", ".join(sorted(missing_scope))
                )
            if extra_scope:
                errors.append(
                    "fresh-task semantic freeze names unknown fields: "
                    + ", ".join(sorted(extra_scope))
                )
    if evidence_class == HISTORICAL_EVIDENCE_CLASS:
        if all_semantics_blind is not False:
            errors.append(
                "historical evidence must mark the complete semantic record as post-hoc"
            )
        if "actual_route" not in freeze_scope:
            errors.append(
                "historical evidence must identify actual_route as frozen before comparison"
            )
        if not allow_historical_annotations:
            errors.append(
                "historical post-hoc semantics require --allow-historical-annotations"
            )
    for identity_field in ("plugin_identity", "task_identity", "repository_identity"):
        identity = receipts.get(identity_field)
        if not isinstance(identity, dict) or not identity:
            errors.append(f"receipts must include non-empty {identity_field}")
    plugin_identity = receipts.get("plugin_identity", {})
    if isinstance(plugin_identity, dict):
        required_plugin_identity = FRESH_PLUGIN_IDENTITY_FIELDS
        if evidence_class == FRESH_EVIDENCE_CLASS:
            errors.extend(
                exact_field_errors(
                    plugin_identity,
                    FRESH_PLUGIN_IDENTITY_FIELDS,
                    "plugin_identity",
                )
            )
        missing_identity = required_plugin_identity.difference(plugin_identity)
        if missing_identity:
            errors.append(
                "plugin_identity missing fields: " + ", ".join(sorted(missing_identity))
            )
        for field in ("name", "installed_version", "payload_hash_method", "cache_relative_path"):
            if not isinstance(plugin_identity.get(field), str) or not plugin_identity[field].strip():
                errors.append(f"plugin_identity field {field} must be a non-empty string")
        if plugin_identity.get("name") != "project-delivery":
            errors.append("plugin_identity name must be project-delivery")
        if not isinstance(plugin_identity.get("source_revision"), str) or not SOURCE_REVISION.fullmatch(
            plugin_identity["source_revision"]
        ):
            errors.append("plugin_identity source_revision must be a hexadecimal revision")
        for field in ("manifest_sha256", "payload_sha256"):
            if not isinstance(plugin_identity.get(field), str) or not SHA256.fullmatch(
                plugin_identity[field]
            ):
                errors.append(f"plugin_identity field {field} must be a SHA-256 digest")
        cache_relative_path = plugin_identity.get("cache_relative_path")
        if isinstance(cache_relative_path, str) and (
            cache_relative_path.startswith("/") or ".." in Path(cache_relative_path).parts
        ):
            errors.append("plugin_identity cache_relative_path must be portable and relative")
    if evidence_class == FRESH_EVIDENCE_CLASS:
        errors.extend(
            validate_installed_identity(
                plugin_identity if isinstance(plugin_identity, dict) else {},
                installed_plugin_root,
                expected_source_revision,
                require_cache_shape=is_fresh_v3,
            )
        )
    task_identity = receipts.get("task_identity", {})
    if isinstance(task_identity, dict):
        required_task_identity = FRESH_TASK_IDENTITY_FIELDS
        if evidence_class == FRESH_EVIDENCE_CLASS:
            errors.extend(
                exact_field_errors(
                    task_identity,
                    FRESH_TASK_IDENTITY_FIELDS,
                    "task_identity",
                )
            )
        missing_identity = required_task_identity.difference(task_identity)
        if missing_identity:
            errors.append(
                "task_identity missing fields: " + ", ".join(sorted(missing_identity))
            )
        for field in ("public_receipt_id", "selected_at"):
            if not isinstance(task_identity.get(field), str) or not task_identity[field].strip():
                errors.append(f"task_identity field {field} must be a non-empty string")
        public_receipt_id = task_identity.get("public_receipt_id")
        if isinstance(public_receipt_id, str) and (
            not PUBLIC_RECEIPT_ID.fullmatch(public_receipt_id)
            or INTERNAL_UUID.search(public_receipt_id)
        ):
            errors.append(
                "task_identity public_receipt_id must be a nonsecret public slug without an internal identifier"
            )
        selected_at = task_identity.get("selected_at")
        if isinstance(selected_at, str) and selected_at.strip():
            try:
                datetime.strptime(selected_at, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                errors.append("task_identity selected_at must be a UTC ISO-8601 timestamp")
        source_digest = task_identity.get("source_observation_sha256")
        if not isinstance(source_digest, str) or not SHA256.fullmatch(source_digest):
            errors.append("task_identity source_observation_sha256 must be a SHA-256 digest")
        elif evidence_class == FRESH_EVIDENCE_CLASS:
            expected_digest = fresh_observation_sha256(receipts)
            if source_digest != expected_digest:
                errors.append(
                    "task_identity source_observation_sha256 does not match the canonical fresh observation"
                )
    repository_identity = receipts.get("repository_identity", {})
    if isinstance(repository_identity, dict):
        required_repository_identity = FRESH_REPOSITORY_IDENTITY_FIELDS
        if evidence_class == FRESH_EVIDENCE_CLASS:
            errors.extend(
                exact_field_errors(
                    repository_identity,
                    FRESH_REPOSITORY_IDENTITY_FIELDS,
                    "repository_identity",
                )
            )
        missing_identity = required_repository_identity.difference(repository_identity)
        if missing_identity:
            errors.append(
                "repository_identity missing fields: "
                + ", ".join(sorted(missing_identity))
            )
        for field in required_repository_identity:
            if not isinstance(repository_identity.get(field), str) or not repository_identity[field].strip():
                errors.append(f"repository_identity field {field} must be a non-empty string")
    if receipts.get("observation_scope") != "route-only-no-effects":
        errors.append("receipt checker accepts only route-only-no-effects observations")
    effects_performed = receipts.get("effects_performed")
    if not validate_string_list(effects_performed) or effects_performed:
        errors.append("route-only observations must record an empty effects_performed list")
    legacy_runtime_events = receipts.get("legacy_runtime_events")
    if not validate_string_list(legacy_runtime_events) or legacy_runtime_events:
        errors.append("route-only observations must record no legacy runtime events")
    if not validate_string_list(receipts.get("legacy_administrative_visibility")):
        errors.append("legacy_administrative_visibility must be a string list")
    if is_fresh_v3:
        for field, label in (
            ("legacy_invocations", "legacy invocations"),
            ("legacy_branded_state_created", "legacy branded state"),
        ):
            value = receipts.get(field)
            if not validate_string_list(value) or value:
                errors.append(f"route-only observations must record no {label}")

    contract_items = comparison_contracts.get("scenarios")
    receipt_items = receipts.get("scenarios")
    if not isinstance(contract_items, list):
        return errors + ["route contract scenarios must be a list"], 0, str(evidence_class)
    if not isinstance(receipt_items, list):
        return errors + ["route receipt scenarios must be a list"], 0, str(evidence_class)

    contract_by_id = {
        item.get("id"): item
        for item in contract_items
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    receipt_by_id: dict[str, dict[str, object]] = {}
    for item in receipt_items:
        if not isinstance(item, dict):
            errors.append("route receipt scenario is not an object")
            continue
        scenario_id = item.get("id")
        if not isinstance(scenario_id, str):
            errors.append("route receipt scenario lacks an ID")
            continue
        if scenario_id in receipt_by_id:
            errors.append(f"duplicate route receipt scenario: {scenario_id}")
        receipt_by_id[scenario_id] = item

    unknown_receipts = set(receipt_by_id).difference(contract_by_id)
    if unknown_receipts:
        errors.append(
            "receipts reference unknown scenarios: " + ", ".join(sorted(unknown_receipts))
        )
    missing_receipts = set(contract_by_id).difference(receipt_by_id)
    if missing_receipts and not allow_subset:
        errors.append(
            "receipts omit canonical scenarios: " + ", ".join(sorted(missing_receipts))
        )
    if not receipt_by_id:
        errors.append("no route receipts found")
        return errors, 0, str(evidence_class)

    evidence_plugin_root = (
        installed_plugin_root
        if evidence_class == FRESH_EVIDENCE_CLASS and installed_plugin_root is not None
        else plugin_root
    )
    available_skills = {
        path.parent.name
        for path in (evidence_plugin_root / "skills").glob("*/SKILL.md")
    }
    loaded_items = receipts.get("loaded_specialists")
    loaded_skills: set[str] = set()
    if not isinstance(loaded_items, list) or not loaded_items:
        errors.append("receipts must include loaded_specialists")
        loaded_items = []
    for loaded_index, item in enumerate(loaded_items, 1):
        if not isinstance(item, dict):
            errors.append(f"loaded specialist {loaded_index} is not an object")
            continue
        if is_fresh:
            errors.extend(
                exact_field_errors(
                    item,
                    (
                        FRESH_V3_LOADED_SPECIALIST_FIELDS
                        if is_fresh_v3
                        else FRESH_LOADED_SPECIALIST_FIELDS
                    ),
                    f"loaded specialist {loaded_index}",
                )
            )
        skill = item.get("skill")
        relative_path = item.get("relative_path")
        state = item.get("state")
        if not isinstance(skill, str) or not skill.strip():
            errors.append(f"loaded specialist {loaded_index} lacks a skill")
            continue
        skill = normalize_skill(skill)
        if skill in loaded_skills:
            errors.append(f"duplicate loaded specialist: {skill}")
        loaded_skills.add(skill)
        if skill not in available_skills:
            errors.append(f"loaded specialist is unknown: {skill}")
            continue
        if relative_path != f"skills/{skill}/SKILL.md":
            errors.append(f"loaded specialist {skill} has an invalid relative path")
            continue
        if state != "loaded":
            errors.append(f"loaded specialist {skill} was not successfully loaded")
        if is_fresh:
            skill_sha256 = item.get("skill_sha256")
            if not is_fresh_v3:
                load_evidence = item.get("evidence")
                if not validate_string_list(load_evidence, require_nonempty=True):
                    errors.append(f"loaded specialist {skill} lacks read evidence")
            if not isinstance(skill_sha256, str) or not SHA256.fullmatch(skill_sha256):
                errors.append(f"loaded specialist {skill} lacks a valid skill_sha256")
            else:
                skill_path = evidence_plugin_root / "skills" / skill / "SKILL.md"
                try:
                    expected_skill_sha256 = hashlib.sha256(safe_read_bytes(
                        skill_path, root=evidence_plugin_root, max_bytes=MAX_TEXT_BYTES,
                    )).hexdigest()
                except OSError as error:
                    errors.append(f"loaded specialist {skill} cannot be hashed: {error}")
                else:
                    if skill_sha256 != expected_skill_sha256:
                        errors.append(
                            f"loaded specialist {skill} skill_sha256 does not match the inspected plugin"
                        )
            if is_fresh_v3:
                closure = item.get("instruction_closure")
                if not isinstance(closure, dict):
                    errors.append(
                        f"loaded specialist {skill} instruction_closure must be an object"
                    )
                    continue
                errors.extend(
                    exact_field_errors(
                        closure,
                        FRESH_V3_INSTRUCTION_CLOSURE_FIELDS,
                        f"loaded specialist {skill} instruction_closure",
                    )
                )
                if closure.get("state") != "complete":
                    errors.append(
                        f"loaded specialist {skill} instruction closure is not complete"
                    )
                unresolved = closure.get("unresolved_references")
                if not validate_string_list(unresolved) or unresolved:
                    errors.append(
                        f"loaded specialist {skill} instruction closure has unresolved references"
                    )
                closure_files = closure.get("files")
                if not isinstance(closure_files, list) or not closure_files:
                    errors.append(
                        f"loaded specialist {skill} instruction closure files must be a non-empty list"
                    )
                    closure_files = []
                declared_paths: set[str] = set()
                root_records = 0
                for closure_index, record in enumerate(closure_files, 1):
                    if not isinstance(record, dict):
                        errors.append(
                            f"loaded specialist {skill} instruction file {closure_index} is not an object"
                        )
                        continue
                    errors.extend(
                        exact_field_errors(
                            record,
                            FRESH_V3_INSTRUCTION_FILE_FIELDS,
                            f"loaded specialist {skill} instruction file {closure_index}",
                        )
                    )
                    closure_path = record.get("relative_path")
                    if not isinstance(closure_path, str) or not closure_path.strip():
                        errors.append(
                            f"loaded specialist {skill} instruction file {closure_index} lacks a relative path"
                        )
                        continue
                    path_parts = Path(closure_path).parts
                    if Path(closure_path).is_absolute() or ".." in path_parts:
                        errors.append(
                            f"loaded specialist {skill} instruction path must be portable and contained: {closure_path}"
                        )
                        continue
                    if closure_path in declared_paths:
                        errors.append(
                            f"loaded specialist {skill} instruction closure repeats path: {closure_path}"
                        )
                    declared_paths.add(closure_path)
                    role = record.get("role")
                    expected_role = (
                        "skill-root"
                        if closure_path == f"skills/{skill}/SKILL.md"
                        else "required-reference"
                    )
                    if role != expected_role:
                        errors.append(
                            f"loaded specialist {skill} instruction file {closure_path} has invalid role"
                        )
                    if role == "skill-root":
                        root_records += 1
                    if record.get("state") != "read-completely-before-route-freeze":
                        errors.append(
                            f"loaded specialist {skill} instruction file {closure_path} was not declared completely read before route freeze"
                        )
                    record_sha = record.get("sha256")
                    if not isinstance(record_sha, str) or not SHA256.fullmatch(record_sha):
                        errors.append(
                            f"loaded specialist {skill} instruction file {closure_path} lacks a valid SHA-256"
                        )
                    else:
                        instruction_path = evidence_plugin_root / closure_path
                        try:
                            actual_sha = hashlib.sha256(
                                safe_read_bytes(
                                    instruction_path, root=evidence_plugin_root,
                                    max_bytes=MAX_TEXT_BYTES,
                                )
                            ).hexdigest()
                        except OSError as error:
                            errors.append(
                                f"loaded specialist {skill} instruction file {closure_path} cannot be hashed: {error}"
                            )
                        else:
                            if record_sha != actual_sha:
                                errors.append(
                                    f"loaded specialist {skill} instruction file {closure_path} hash does not match the inspected plugin"
                                )
                            if role == "skill-root" and record_sha != skill_sha256:
                                errors.append(
                                    f"loaded specialist {skill} root closure hash does not match skill_sha256"
                                )
                required_paths, closure_errors = required_instruction_paths(
                    evidence_plugin_root,
                    skill,
                )
                errors.extend(closure_errors)
                missing_closure = required_paths.difference(declared_paths)
                extra_closure = declared_paths.difference(required_paths)
                if missing_closure:
                    errors.append(
                        f"loaded specialist {skill} instruction closure omits files: "
                        + ", ".join(sorted(missing_closure))
                    )
                if extra_closure:
                    errors.append(
                        f"loaded specialist {skill} instruction closure has undeclared files: "
                        + ", ".join(sorted(extra_closure))
                    )
                if root_records != 1:
                    errors.append(
                        f"loaded specialist {skill} instruction closure must contain exactly one skill-root"
                    )
    forbidden_dependencies = set(
        comparison_contracts.get("forbidden_runtime_dependencies", [])
    )
    selected_route_skills: set[str] = set()
    seen_gap_ids: set[str] = set()
    scenario_observation_unions: dict[str, set[str]] = {
        "effects_performed": set(),
        "legacy_administrative_visibility": set(),
        "legacy_branded_state_created": set(),
        "legacy_invocations": set(),
        "legacy_runtime_events": set(),
    }
    started = time.monotonic()
    selected_ids = [item.get("id") for item in contract_items if item.get("id") in receipt_by_id]
    for index, scenario_id in enumerate(selected_ids, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(selected_ids) - index)
        print(
            f"RECEIPT [{index}/{len(selected_ids)}] id={scenario_id} eta={eta:.1f}s",
            flush=True,
        )
        contract = contract_by_id[scenario_id]
        receipt = receipt_by_id[scenario_id]
        required_receipt_fields = (
            FRESH_V3_SCENARIO_FIELDS
            if is_fresh_v3
            else FRESH_REQUIRED_RECEIPT_FIELDS
            if is_fresh
            else REQUIRED_RECEIPT_FIELDS
        )
        missing_fields = required_receipt_fields.difference(receipt)
        if missing_fields:
            errors.append(
                f"{scenario_id} receipt missing fields: {', '.join(sorted(missing_fields))}"
            )
        if is_fresh:
            errors.extend(
                exact_field_errors(
                    receipt,
                    required_receipt_fields,
                    f"{scenario_id} receipt",
                )
            )
        if (
            evidence_class == FRESH_EVIDENCE_CLASS
            and receipt.get("prompt") != contract.get("prompt")
        ):
            errors.append(f"{scenario_id} prompt does not match the canonical blind prompt")

        outcome_state: str | None = None
        if is_fresh_v3:
            scenario_observation = receipt.get("scenario_observation")
            if not isinstance(scenario_observation, dict):
                errors.append(f"{scenario_id} scenario_observation must be an object")
            else:
                errors.extend(
                    exact_field_errors(
                        scenario_observation,
                        FRESH_V3_SCENARIO_OBSERVATION_FIELDS,
                        f"{scenario_id} scenario_observation",
                    )
                )
                if (
                    scenario_observation.get("observation_scope")
                    != receipts.get("observation_scope")
                ):
                    errors.append(
                        f"{scenario_id} scenario observation scope does not match the root"
                    )
                for field in scenario_observation_unions:
                    value = scenario_observation.get(field)
                    if not validate_string_list(value):
                        errors.append(
                            f"{scenario_id} scenario_observation {field} must be a string list"
                        )
                        continue
                    scenario_observation_unions[field].update(value)
                    if field != "legacy_administrative_visibility" and value:
                        errors.append(
                            f"{scenario_id} route-only scenario records forbidden {field}"
                        )

            outcome_observation = receipt.get("outcome_observation")
            if not isinstance(outcome_observation, dict):
                errors.append(f"{scenario_id} outcome_observation must be an object")
            else:
                errors.extend(
                    exact_field_errors(
                        outcome_observation,
                        FRESH_V3_OUTCOME_OBSERVATION_FIELDS,
                        f"{scenario_id} outcome_observation",
                    )
                )
                raw_outcome_state = outcome_observation.get("state")
                if raw_outcome_state not in ALLOWED_OUTCOME_STATES:
                    errors.append(
                        f"{scenario_id} outcome_observation has invalid state: {raw_outcome_state}"
                    )
                elif isinstance(raw_outcome_state, str):
                    outcome_state = raw_outcome_state
                if not validate_string_list(
                    outcome_observation.get("evidence"), require_nonempty=True
                ):
                    errors.append(
                        f"{scenario_id} outcome_observation must contain evidence"
                    )

        raw_route = receipt.get("actual_route")
        if not validate_string_list(raw_route) or not raw_route:
            errors.append(f"{scenario_id} actual_route must be a non-empty string list")
            continue
        route = [normalize_skill(item) for item in raw_route]
        selected_route_skills.update(route)
        unknown_skills = set(route).difference(available_skills)
        if unknown_skills:
            errors.append(
                f"{scenario_id} actual route references unknown skills: "
                + ", ".join(sorted(unknown_skills))
            )
        legacy_skills = set(route).intersection(forbidden_dependencies)
        if legacy_skills:
            errors.append(
                f"{scenario_id} actual route uses forbidden dependencies: "
                + ", ".join(sorted(legacy_skills))
            )
        unloaded_skills = set(route).difference(loaded_skills)
        if unloaded_skills:
            errors.append(
                f"{scenario_id} route includes specialists without load evidence: "
                + ", ".join(sorted(unloaded_skills))
            )

        accepted_taxonomy = {
            "scale": contract.get("accepted_scales", [contract.get("scale")]),
            "risk": contract.get("accepted_risks", [contract.get("risk")]),
        }
        for classification_field, accepted_values in accepted_taxonomy.items():
            if (
                not isinstance(accepted_values, list)
                or receipt.get(classification_field) not in accepted_values
            ):
                errors.append(
                    f"{scenario_id} {classification_field} is outside the accepted contract taxonomy"
                )
        if receipt.get("authority") != contract.get("authority"):
            errors.append(
                f"{scenario_id} authority does not match the contract taxonomy"
            )
        taxonomy_rationale = receipt.get("taxonomy_rationale")
        if not isinstance(taxonomy_rationale, str) or len(taxonomy_rationale.strip()) < 20:
            errors.append(f"{scenario_id} lacks a substantive taxonomy rationale")
        if not validate_string_list(
            receipt.get("taxonomy_evidence"), require_nonempty=True
        ):
            errors.append(f"{scenario_id} taxonomy_evidence must be a non-empty string list")

        required = set(contract.get("required_capabilities", []))
        missing_required = required.difference(route)
        if missing_required:
            errors.append(
                f"{scenario_id} misses required capabilities: "
                + ", ".join(sorted(missing_required))
            )
        lead = contract.get("lead_capability")
        if isinstance(lead, str) and lead not in route:
            errors.append(f"{scenario_id} misses lead capability: {lead}")
        if isinstance(lead, str) and evidence_class == FRESH_EVIDENCE_CLASS:
            lead_index = 1 if route[0] == "delivery-orchestrator" and lead != "delivery-orchestrator" else 0
            if len(route) <= lead_index or route[lead_index] != lead:
                errors.append(
                    f"{scenario_id} actual route does not open with lead capability: {lead}"
                )
        forbidden = set(contract.get("forbidden_capabilities", []))
        unsafe = forbidden.intersection(route)
        if unsafe:
            errors.append(
                f"{scenario_id} uses authority-forbidden capabilities: "
                + ", ".join(sorted(unsafe))
            )

        allowed_reentry = set(contract.get("allowed_reentry", []))
        repeated = {skill for skill, count in Counter(route).items() if count > 1}
        invalid_reentry = repeated.difference(allowed_reentry)
        if invalid_reentry:
            errors.append(
                f"{scenario_id} repeats capabilities without a re-entry contract: "
                + ", ".join(sorted(invalid_reentry))
            )
        for controller in contract.get("required_reentry", []):
            return_owners = contract.get("required_reentry_after", {}).get(controller, [])
            entry_owners = contract.get("required_reentry_before", {}).get(controller, [])
            selected_owners = [owner for owner in return_owners if owner in route]
            selected_entry_owners = [owner for owner in entry_owners if owner in route]
            if selected_owners and route.count(controller) < 2:
                errors.append(
                    f"{scenario_id} misses required controller re-entry: {controller}"
                )
                continue
            if selected_entry_owners and route.index(controller) >= min(
                route.index(owner) for owner in selected_entry_owners
            ):
                errors.append(
                    f"{scenario_id} controller {controller} does not enter before: "
                    + ", ".join(selected_entry_owners)
                )
            if selected_owners and last_index(route, controller) <= max(
                last_index(route, owner) for owner in selected_owners
            ):
                errors.append(
                    f"{scenario_id} controller {controller} does not return after: "
                    + ", ".join(selected_owners)
                )

        if evidence_class == FRESH_EVIDENCE_CLASS:
            for controller, owners in contract.get("required_final_after", {}).items():
                selected_owners = [owner for owner in owners if owner in route]
                if (
                    controller in route
                    and selected_owners
                    and last_index(route, controller)
                    <= max(last_index(route, owner) for owner in selected_owners)
                ):
                    errors.append(
                        f"{scenario_id} final {controller} disposition does not follow: "
                        + ", ".join(selected_owners)
                    )

        for before, after in contract.get("precedence", []):
            if before in route and after in route and route.index(before) >= route.index(after):
                errors.append(
                    f"{scenario_id} violates precedence: {before} must precede {after}"
                )

        raw_gaps = receipt.get("gaps")
        dispositions = receipt.get("conditional_dispositions")
        if not isinstance(dispositions, dict):
            errors.append(f"{scenario_id} conditional_dispositions must be an object")
            dispositions = {}
        expected_conditional = {
            item.get("skill")
            for item in contract.get("conditional_capabilities", [])
            if isinstance(item, dict) and isinstance(item.get("skill"), str)
        }
        missing_dispositions = expected_conditional.difference(dispositions)
        extra_dispositions = set(dispositions).difference(expected_conditional)
        if missing_dispositions:
            errors.append(
                f"{scenario_id} omits conditional dispositions: "
                + ", ".join(sorted(missing_dispositions))
            )
        invalid_extra_dispositions = extra_dispositions.intersection(
            required.union(forbidden).union({"delivery-orchestrator"})
        )
        unknown_extra_dispositions = extra_dispositions.difference(available_skills)
        if invalid_extra_dispositions:
            errors.append(
                f"{scenario_id} extra conditional dispositions duplicate required, forbidden, or controller capabilities: "
                + ", ".join(sorted(invalid_extra_dispositions))
            )
        if unknown_extra_dispositions:
            errors.append(
                f"{scenario_id} extra conditional dispositions reference unknown capabilities: "
                + ", ".join(sorted(unknown_extra_dispositions))
            )
        validated_dispositions = set(dispositions).difference(
            invalid_extra_dispositions.union(unknown_extra_dispositions)
        )
        for skill in validated_dispositions:
            disposition = dispositions[skill]
            if not isinstance(disposition, dict):
                errors.append(f"{scenario_id} disposition for {skill} must be an object")
                continue
            if is_fresh:
                errors.extend(
                    exact_field_errors(
                        disposition,
                        (
                            FRESH_V3_CONDITIONAL_DISPOSITION_FIELDS
                            if is_fresh_v3
                            else FRESH_CONDITIONAL_DISPOSITION_FIELDS
                        ),
                        f"{scenario_id} disposition for {skill}",
                    )
                )
            state = disposition.get("state")
            rationale = disposition.get("rationale")
            if state not in ALLOWED_CONDITIONAL_STATES:
                errors.append(f"{scenario_id} disposition for {skill} has invalid state: {state}")
            if not isinstance(rationale, str) or len(rationale.strip()) < 12:
                errors.append(f"{scenario_id} disposition for {skill} lacks a substantive rationale")
            if not validate_string_list(disposition.get("evidence"), require_nonempty=True):
                errors.append(f"{scenario_id} disposition for {skill} lacks evidence")
            if state == "planned-future" and skill not in PLANNED_FUTURE_CAPABILITIES:
                errors.append(
                    f"{scenario_id} disposition for {skill} cannot be planned-future"
                )
            if (
                is_unsealed_fresh_v2
                and skill == "retrospective-improvement"
                and state != "planned-future"
            ):
                errors.append(
                    f"{scenario_id} route-only retrospective must remain planned-future until a delivery outcome exists"
                )
            if is_fresh_v3:
                trigger_evaluation = disposition.get("trigger_evaluation")
                trigger_result: str | None = None
                if not isinstance(trigger_evaluation, dict):
                    errors.append(
                        f"{scenario_id} disposition for {skill} trigger_evaluation must be an object"
                    )
                else:
                    errors.extend(
                        exact_field_errors(
                            trigger_evaluation,
                            FRESH_V3_TRIGGER_EVALUATION_FIELDS,
                            f"{scenario_id} disposition for {skill} trigger_evaluation",
                        )
                    )
                    trigger_statement = trigger_evaluation.get("trigger_statement")
                    if (
                        not isinstance(trigger_statement, str)
                        or len(trigger_statement.strip()) < 12
                    ):
                        errors.append(
                            f"{scenario_id} disposition for {skill} lacks a substantive blind trigger statement"
                        )
                    if trigger_evaluation.get("source") != "installed-runtime":
                        errors.append(
                            f"{scenario_id} disposition for {skill} trigger source must be installed-runtime"
                        )
                    raw_trigger_result = trigger_evaluation.get("result")
                    if raw_trigger_result not in ALLOWED_TRIGGER_RESULTS:
                        errors.append(
                            f"{scenario_id} disposition for {skill} has invalid trigger result: {raw_trigger_result}"
                        )
                    elif isinstance(raw_trigger_result, str):
                        trigger_result = raw_trigger_result

                allowed_results_by_state = {
                    "activated": {"met"},
                    "blocked": {"met", "unknown"},
                    "deferred": {"met", "unknown"},
                    "not-applicable": {"not-met"},
                    "planned-future": {"future-pending"},
                }
                if state in allowed_results_by_state and trigger_result not in allowed_results_by_state[state]:
                    errors.append(
                        f"{scenario_id} disposition for {skill} state {state} contradicts trigger result {trigger_result}"
                    )
                if trigger_result == "unknown" and not has_linked_gap(
                    raw_gaps,
                    f"conditional_dispositions.{skill}",
                    disposition.get("evidence"),
                ):
                    errors.append(
                        f"{scenario_id} unknown trigger for {skill} requires a linked structured gap"
                    )
                if skill != "retrospective-improvement" and trigger_result == "future-pending":
                    errors.append(
                        f"{scenario_id} non-retrospective disposition for {skill} cannot be future-pending"
                    )
                if skill == "retrospective-improvement":
                    allowed_retrospective = {
                        "meaningful-outcome-observed": {
                            ("activated", "met"),
                            ("blocked", "met"),
                            ("deferred", "met"),
                        },
                        "no-meaningful-outcome-observed": {
                            ("planned-future", "future-pending")
                        },
                        "unknown": {
                            ("blocked", "unknown"),
                            ("deferred", "unknown"),
                        },
                    }
                    if (state, trigger_result) not in allowed_retrospective.get(
                        outcome_state, set()
                    ):
                        errors.append(
                            f"{scenario_id} retrospective disposition does not match outcome observation {outcome_state}"
                        )
            if skill in route and state not in {"activated", "planned-future"}:
                errors.append(
                    f"{scenario_id} selected conditional capability {skill} without an active or planned-future state"
                )
            if skill not in route and state == "activated":
                errors.append(
                    f"{scenario_id} marks omitted conditional capability {skill} as activated"
                )
            if (
                evidence_class == FRESH_EVIDENCE_CLASS
                and state == "planned-future"
                and skill in route
            ):
                errors.append(
                    f"{scenario_id} fresh receipt includes future-only capability {skill} in actual_route"
                )
            if state == "blocked":
                errors.append(
                    f"{scenario_id} has a blocked conditional branch and cannot pass route policy"
                )

        if is_fresh_v3 and "retrospective-improvement" in route:
            direct_unknown_intake = (
                "retrospective-improvement" in required
                and outcome_state == "unknown"
                and isinstance(outcome_observation, dict)
                and has_linked_gap(
                    raw_gaps,
                    "outcome_observation",
                    outcome_observation.get("evidence"),
                )
            )
            if (
                outcome_state != "meaningful-outcome-observed"
                and not direct_unknown_intake
            ):
                errors.append(
                    f"{scenario_id} selects retrospective-improvement without a meaningful observed outcome or linked direct-intake gap"
                )

        extra_justifications = receipt.get("extra_capability_justifications")
        if not isinstance(extra_justifications, dict):
            errors.append(f"{scenario_id} extra_capability_justifications must be an object")
            extra_justifications = {}
        selectable = required.union(validated_dispositions).union(
            {"delivery-orchestrator"}
        )
        extra_capabilities = set(route).difference(selectable)
        missing_extra_justifications = extra_capabilities.difference(extra_justifications)
        unexpected_extra_justifications = set(extra_justifications).difference(extra_capabilities)
        if missing_extra_justifications:
            errors.append(
                f"{scenario_id} lacks justification for extra capabilities: "
                + ", ".join(sorted(missing_extra_justifications))
            )
        if unexpected_extra_justifications:
            errors.append(
                f"{scenario_id} justifies capabilities that are not extra: "
                + ", ".join(sorted(unexpected_extra_justifications))
            )
        for skill in extra_capabilities.intersection(extra_justifications):
            justification = extra_justifications[skill]
            if not isinstance(justification, dict):
                errors.append(f"{scenario_id} extra-capability justification for {skill} must be an object")
                continue
            if evidence_class == FRESH_EVIDENCE_CLASS:
                errors.extend(
                    exact_field_errors(
                        justification,
                        FRESH_EXTRA_JUSTIFICATION_FIELDS,
                        f"{scenario_id} extra-capability justification for {skill}",
                    )
                )
            rationale = justification.get("rationale")
            if not isinstance(rationale, str) or len(rationale.strip()) < 12:
                errors.append(f"{scenario_id} extra-capability justification for {skill} lacks a substantive rationale")
            if not validate_string_list(justification.get("evidence"), require_nonempty=True):
                errors.append(f"{scenario_id} extra-capability justification for {skill} lacks evidence")

        if receipt.get("delivery_result") != "not-run":
            errors.append(
                f"{scenario_id} delivery_result must be not-run; this checker is route-only"
            )
        if not validate_string_list(receipt.get("evidence"), require_nonempty=True):
            errors.append(f"{scenario_id} evidence must be a non-empty string list")
        if is_fresh_v3:
            if not isinstance(raw_gaps, list):
                errors.append(f"{scenario_id} gaps must be a structured list")
                raw_gaps = []
            for gap_index, gap in enumerate(raw_gaps, 1):
                if not isinstance(gap, dict):
                    errors.append(
                        f"{scenario_id} gap {gap_index} must be an object"
                    )
                    continue
                errors.extend(
                    exact_field_errors(
                        gap,
                        FRESH_V3_GAP_FIELDS,
                        f"{scenario_id} gap {gap_index}",
                    )
                )
                gap_id = gap.get("id")
                if not isinstance(gap_id, str) or not GAP_ID.fullmatch(gap_id):
                    errors.append(f"{scenario_id} gap {gap_index} has an invalid ID")
                elif gap_id in seen_gap_ids:
                    errors.append(f"duplicate structured gap ID: {gap_id}")
                else:
                    seen_gap_ids.add(gap_id)
                if gap.get("kind") not in ALLOWED_GAP_KINDS:
                    errors.append(f"{scenario_id} gap {gap_id} has an invalid kind")
                route_effect = gap.get("route_effect")
                if route_effect not in ALLOWED_GAP_ROUTE_EFFECTS:
                    errors.append(
                        f"{scenario_id} gap {gap_id} has an invalid route_effect"
                    )
                elif route_effect == "blocks-route":
                    errors.append(
                        f"{scenario_id} gap {gap_id} blocks the route claim"
                    )
                related_field = gap.get("related_field")
                if not dotted_path_exists(receipt, related_field):
                    errors.append(
                        f"{scenario_id} gap {gap_id} references an unknown related_field"
                    )
                for field in ("summary", "next_action"):
                    value = gap.get(field)
                    if not isinstance(value, str) or len(value.strip()) < 12:
                        errors.append(
                            f"{scenario_id} gap {gap_id} field {field} must be substantive"
                        )
        elif not validate_string_list(raw_gaps):
            errors.append(f"{scenario_id} gaps must be a string list")

    if evidence_class == FRESH_EVIDENCE_CLASS:
        excess_loaded = loaded_skills.difference(selected_route_skills)
        missing_loaded = selected_route_skills.difference(loaded_skills)
        if excess_loaded:
            errors.append(
                "fresh-task loaded_specialists contains skills absent from every actual route: "
                + ", ".join(sorted(excess_loaded))
            )
        if missing_loaded:
            errors.append(
                "fresh-task actual routes lack exact load records: "
                + ", ".join(sorted(missing_loaded))
            )
    if is_fresh_v3:
        for field, observed_union in scenario_observation_unions.items():
            root_value = receipts.get(field)
            if isinstance(root_value, list) and root_value != sorted(observed_union):
                errors.append(
                    f"fresh-task root {field} does not equal the sorted unique scenario union"
                )

    return errors, len(selected_ids), str(evidence_class)


def write_grade_record(
    output: Path,
    root: Path,
    receipts: dict[str, object],
    contract_raw: bytes,
    checker_raw: bytes,
    scenario_count: int,
    evidence: dict[str, str],
    expected_source_revision: str,
    candidate_proof: str,
    verdict: str = "PASS",
    validation_errors: list[str] | None = None,
) -> str:
    if not output.is_absolute() or output.name in {"", ".", ".."}:
        raise ValueError("grade output must be an absolute new file path")
    if output.is_relative_to(root):
        raise ValueError("grade output must remain outside the source repository")
    if verdict not in {"PASS", "FAIL"}:
        raise ValueError("grade verdict must be PASS or FAIL")
    if verdict == "PASS" and validation_errors:
        raise ValueError("a PASS grade cannot contain validation errors")
    if verdict == "FAIL" and not validation_errors:
        raise ValueError("a FAIL grade must contain validation errors")
    if verdict == "FAIL" and candidate_proof != "not-established":
        raise ValueError("a FAIL grade cannot establish candidate proof")
    raw_errors = list(validation_errors or [])
    serialized_errors = json.dumps(
        raw_errors,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    public_error_records = [
        f"validation-error-{index:03d} sha256={sha256_bytes(error.encode('utf-8'))}"
        for index, error in enumerate(raw_errors, 1)
    ]
    installed_identity = receipts.get("plugin_identity")
    installed_payload = (
        installed_identity.get("payload_sha256")
        if isinstance(installed_identity, dict)
        else "unknown"
    )
    grade = {
        "schema_version": 1,
        "evidence_class": GRADE_EVIDENCE_CLASS,
        "verdict": verdict,
        "candidate_proof": candidate_proof,
        "scenario_count": scenario_count,
        "raw_observation_sha256": evidence["raw_observation_sha256"],
        "coordinator_attestation_sha256": evidence[
            "coordinator_attestation_sha256"
        ],
        "prompt_manifest_sha256": evidence["prompt_manifest_sha256"],
        "task_prompt_sha256": evidence["task_prompt_sha256"],
        "route_contract_sha256": sha256_bytes(contract_raw),
        "checker_sha256": sha256_bytes(checker_raw),
        "source_revision": expected_source_revision,
        "installed_payload_sha256": installed_payload,
        "graded_at_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "error_count": len(raw_errors),
        "error_set_sha256": sha256_bytes(serialized_errors),
        "errors": public_error_records,
        "limitations": [
            "This grade establishes only the bounded route-policy claim for the sealed scenarios.",
            "It does not establish implementation, release, decommission, UI-rendering, or production-readiness claims.",
            "Coordinator hashing binds bytes and launch facts but cannot prove model attention or absence of unrecorded effects.",
            "Independent task execution provenance remains bounded by the coordinator's private task-binding procedure.",
            "FAIL grades publish only ordered SHA-256 identities of validation errors; exact messages remain in local checker output to avoid reflecting untrusted content.",
        ],
    }
    field_errors = exact_field_errors(grade, GRADE_FIELDS, "grade record")
    if field_errors:
        raise ValueError("; ".join(field_errors))
    rendered = (json.dumps(grade, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    try:
        resolved_parent = output.parent.resolve(strict=True)
    except OSError as error:
        raise ValueError(f"grade output parent cannot be resolved: {error}") from error
    if resolved_parent.is_relative_to(root):
        raise ValueError("grade output must remain outside the source repository")
    parent_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(
        os, "O_NOFOLLOW", 0
    )
    parent_descriptor = os.open(output.parent, parent_flags)
    output_descriptor: int | None = None
    try:
        opened_parent = os.fstat(parent_descriptor)
        resolved_metadata = os.stat(resolved_parent, follow_symlinks=False)
        if not stat.S_ISDIR(opened_parent.st_mode) or (
            opened_parent.st_dev,
            opened_parent.st_ino,
        ) != (resolved_metadata.st_dev, resolved_metadata.st_ino):
            raise ValueError("grade output parent changed during validation")
        output_flags = (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_NOFOLLOW", 0)
        )
        output_descriptor = os.open(
            output.name,
            output_flags,
            0o600,
            dir_fd=parent_descriptor,
        )
        with os.fdopen(output_descriptor, "wb") as handle:
            output_descriptor = None
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        if output_descriptor is not None:
            os.close(output_descriptor)
        os.close(parent_descriptor)
    return sha256_bytes(rendered)


def printable_error(error: object) -> str:
    """Render one error as one escaped log token without control-line injection."""
    return json.dumps(str(error), ensure_ascii=True)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).expanduser().resolve()
    receipt_path = Path(args.receipts).expanduser().absolute()
    installed_plugin_root = (
        Path(args.installed_plugin_root).expanduser().absolute()
        if args.installed_plugin_root
        else None
    )
    contract_path = root / "tests" / "route-contracts.json"
    checker_path = Path(__file__).absolute()
    contract_raw, contract_read_errors = read_regular_bytes(
        contract_path, "route contracts", root=root
    )
    receipt_raw, receipt_read_errors = read_regular_bytes(
        receipt_path, "route receipts"
    )
    checker_raw, checker_read_errors = read_regular_bytes(
        checker_path, "receipt checker"
    )
    errors = [
        *contract_read_errors,
        *receipt_read_errors,
        *checker_read_errors,
    ]
    contracts: dict[str, object] | None = None
    receipts: dict[str, object] | None = None
    if contract_raw is not None:
        contracts, parse_errors = parse_json_bytes(contract_raw, "route contracts")
        errors.extend(parse_errors)
    if receipt_raw is not None:
        receipts, parse_errors = parse_json_bytes(receipt_raw, "route receipts")
        errors.extend(parse_errors)
    is_sealed_v3 = (
        receipts is not None
        and receipts.get("schema_version") == 3
        and receipts.get("evidence_class") == FRESH_EVIDENCE_CLASS
    )
    installed_snapshot: dict[Path, bytes] | None = None
    if is_sealed_v3 and not args.allow_unattested_v3:
        installed_snapshot, installed_snapshot_errors = snapshot_installed_plugin(
            installed_plugin_root
        )
        errors.extend(installed_snapshot_errors)
    scenario_count = 0
    evidence_class = "unknown"
    if (
        contracts is not None and receipts is not None
        and not (is_sealed_v3 and not args.allow_unattested_v3 and installed_snapshot is None)
    ):
        semantic_errors, scenario_count, evidence_class = validate(
            root,
            receipt_path,
            args.allow_subset,
            args.allow_historical_annotations,
            args.allow_unsealed_fresh,
            installed_plugin_root,
            args.expected_source_revision,
            contracts_snapshot=contracts,
            receipts_snapshot=receipts,
        )
        errors.extend(semantic_errors)
    binding_evidence = {
        "coordinator_attestation_sha256": "unknown",
        "prompt_manifest_sha256": "unknown",
        "raw_observation_sha256": "unknown",
        "task_prompt_sha256": "unknown",
    }
    if is_sealed_v3 and not args.allow_unattested_v3:
        if contract_raw is not None and checker_raw is not None:
            errors.extend(
                validate_grader_source(
                    root,
                    args.expected_source_revision,
                    contract_raw,
                    checker_raw,
                )
            )
        attestation_path = (
            Path(args.coordinator_attestation).expanduser().absolute()
            if args.coordinator_attestation
            else None
        )
        prompt_path = (
            Path(args.prompt_manifest).expanduser().absolute()
            if args.prompt_manifest
            else None
        )
        task_prompt_path = (
            Path(args.task_prompt).expanduser().absolute()
            if args.task_prompt
            else None
        )
        if receipt_raw is not None:
            binding_errors, binding_evidence = validate_coordinator_binding(
                root,
                receipts,
                receipt_raw,
                installed_snapshot,
                attestation_path,
                args.expected_attestation_sha256,
                prompt_path,
                task_prompt_path,
                args.expected_source_revision,
            )
            errors.extend(binding_errors)
        final_installed_snapshot, final_snapshot_errors = snapshot_installed_plugin(
            installed_plugin_root
        )
        errors.extend(final_snapshot_errors)
        if (
            installed_snapshot is not None
            and final_installed_snapshot is not None
            and installed_snapshot != final_installed_snapshot
        ):
            errors.append(
                "installed plugin package changed during sealed validation"
            )
        if not args.grade_output:
            errors.append("sealed schema-v3 candidate proof requires --grade-output")
    if errors:
        print("\n".join(f"ERROR {printable_error(error)}" for error in errors))
        if (
            is_sealed_v3
            and args.grade_output
            and receipts is not None
            and contract_raw is not None
            and checker_raw is not None
        ):
            grade_output = Path(args.grade_output).expanduser().absolute()
            expected_revision = (
                args.expected_source_revision
                if isinstance(args.expected_source_revision, str)
                else "unknown"
            )
            try:
                grade_sha = write_grade_record(
                    grade_output,
                    root,
                    receipts,
                    contract_raw,
                    checker_raw,
                    scenario_count,
                    binding_evidence,
                    expected_revision,
                    "not-established",
                    verdict="FAIL",
                    validation_errors=errors,
                )
            except (OSError, UnicodeError, ValueError) as error:
                print(
                    "ERROR independent failure grade could not be written: "
                    + printable_error(error)
                )
            else:
                print(
                    "FAIL_GRADE candidate_proof=not-established "
                    f"grade_sha256={grade_sha}"
                )
        return 1
    if evidence_class == HISTORICAL_EVIDENCE_CLASS:
        print(
            f"PASS scenarios={scenario_count} historical_route_shape_records={scenario_count} "
            "current_policy_claim=not-established "
            f"evidence_class={evidence_class}"
        )
    elif receipts is not None and receipts.get("schema_version") == 2:
        print(
            f"PASS scenarios={scenario_count} route_policy_records={scenario_count} "
            "candidate_proof=not-established evidence_profile=unsealed-schema-v2-self-attestation "
            f"evidence_class={evidence_class}"
        )
    elif args.allow_unattested_v3:
        print(
            f"PASS scenarios={scenario_count} route_policy_records={scenario_count} "
            "candidate_proof=requires-coordinator-attestation "
            f"evidence_class={evidence_class}"
        )
    else:
        assert receipts is not None
        assert contract_raw is not None
        assert checker_raw is not None
        assert isinstance(args.expected_source_revision, str)
        grade_output = Path(args.grade_output).expanduser().absolute()
        candidate_proof = (
            "established-for-subset-route-policy-only"
            if args.allow_subset
            else "established-for-route-policy-only"
        )
        try:
            grade_sha = write_grade_record(
                grade_output,
                root,
                receipts,
                contract_raw,
                checker_raw,
                scenario_count,
                binding_evidence,
                args.expected_source_revision,
                candidate_proof,
            )
        except (OSError, UnicodeError, ValueError) as error:
            print(
                "ERROR independent grade record could not be written: "
                + printable_error(error)
            )
            return 1
        print(
            f"PASS scenarios={scenario_count} route_policy_records={scenario_count} "
            f"candidate_proof={candidate_proof} "
            "evidence_profile=sealed-three-record "
            f"grade_sha256={grade_sha} evidence_class={evidence_class}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
