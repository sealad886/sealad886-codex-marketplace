#!/usr/bin/env python3
"""Check complete source-to-package coverage and per-skill review evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlparse

from safe_files import read_text


EXPECTED_SKILLS = 265
SHA256 = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"[0-9a-f]{40}")


def nonempty_strings(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


def validate(root: Path) -> tuple[list[str], int]:
    root = root.resolve()
    errors: list[str] = []
    evidence = root / "docs/reviews/mindrally-skills"
    package = root / "plugins/mindrally-skills"
    try:
        inventory = json.loads(read_text(evidence / "source-inventory.json", root=root))
        entries = inventory["skills"]
        source_commit = inventory["source_commit"]
        if not COMMIT.fullmatch(source_commit):
            raise ValueError("invalid pinned source commit")
        if inventory["skill_count"] != EXPECTED_SKILLS or len(entries) != EXPECTED_SKILLS:
            raise ValueError(f"expected {EXPECTED_SKILLS} source skills")
        expected: dict[str, dict] = {}
        for entry in entries:
            name = entry["skill"]
            if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                raise ValueError("invalid source skill name")
            if name in expected:
                raise ValueError(f"duplicate source skill {name}")
            if not SHA256.fullmatch(entry["source_sha256"]):
                raise ValueError(f"invalid source hash for {name}")
            if entry["source_path"] != f"{name}/SKILL.md":
                raise ValueError(f"unexpected source path for {name}")
            expected[name] = entry
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        return [f"invalid source inventory: {error}"], 0

    actual = {path.parent.name for path in (package / "skills").glob("*/SKILL.md")}
    for name in sorted(expected.keys() - actual):
        errors.append(f"missing packaged skill: {name}")
    for name in sorted(actual - expected.keys()):
        errors.append(f"skill absent from pinned source inventory: {name}")

    reviewed: set[str] = set()
    for audit_path in sorted(evidence.glob("audit-batch-*.json")):
        try:
            audit = json.loads(read_text(audit_path, root=root))
            if audit["source_commit"] != source_commit or not isinstance(audit["records"], list):
                raise ValueError("source commit mismatch or invalid records")
            records = audit["records"]
        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
            errors.append(f"invalid audit {audit_path.name}: {error}")
            continue
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("skill"), str):
                errors.append(f"invalid review record in {audit_path.name}")
                continue
            name = record["skill"]
            if name not in expected:
                errors.append(f"review names unknown source skill: {name}")
                continue
            if name in reviewed:
                errors.append(f"duplicate review record: {name}")
            reviewed.add(name)
            if record.get("source_sha256") != expected[name]["source_sha256"]:
                errors.append(f"review source hash mismatch: {name}")
            for field in ("reviewed_source_sections", "corrections", "verification_limits", "references"):
                if not nonempty_strings(record.get(field)):
                    errors.append(f"missing review evidence {field}: {name}")
            sources = record.get("primary_sources")
            if not isinstance(sources, list) or not sources:
                errors.append(f"missing primary sources: {name}")
            else:
                for source in sources:
                    if not isinstance(source, dict):
                        errors.append(f"invalid primary source: {name}")
                        continue
                    url = source.get("url", "")
                    claim = source.get("checked_claim")
                    if not isinstance(url, str):
                        errors.append(f"invalid primary source URL: {name}")
                        continue
                    try:
                        parsed = urlparse(url)
                        valid_url = parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username
                    except ValueError:
                        valid_url = False
                    if not valid_url or not isinstance(claim, str) or not claim.strip():
                        errors.append(f"primary source lacks HTTPS URL or checked claim: {name}")
            skill_root = package / "skills" / name
            try:
                skill = read_text(skill_root / "SKILL.md", root=package)
            except (OSError, UnicodeError, ValueError) as error:
                errors.append(f"unreadable skill {name}: {error}")
                continue
            if len(skill.splitlines()) > 500:
                errors.append(f"entry point exceeds progressive disclosure budget: {name}")
            references = record.get("references")
            if not isinstance(references, list):
                continue
            for reference in references:
                if not isinstance(reference, str):
                    continue
                path = PurePosixPath(reference)
                if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != "references":
                    errors.append(f"reference escapes owning skill reference directory: {name}")
                    continue
                try:
                    read_text(skill_root / reference, root=skill_root)
                except (OSError, UnicodeError, ValueError) as error:
                    errors.append(f"missing or unsafe reference {name}/{reference}: {error}")
                targets = re.findall(r"\[[^]]+\]\(([^)]+)\)", skill)
                if reference not in targets:
                    errors.append(f"reference not directly routed from entry point: {name}/{reference}")

    for name in sorted(expected.keys() - reviewed):
        errors.append(f"missing individual review: {name}")
    return errors, len(reviewed)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    errors, reviewed = validate(args.root)
    for error in errors:
        print(f"ERROR {error}")
    print(f"{'FAIL' if errors else 'PASS'} individual_reviews={reviewed}/{EXPECTED_SKILLS}")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
