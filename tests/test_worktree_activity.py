"""Recoverable ownership is persistent, root-scoped, and safe under contention.

All repositories and thread identifiers here are disposable fixtures. These tests
prove the cooperative CLI contract, not live Desktop role authentication.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr
from copy import deepcopy
import fcntl
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest import mock

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "plugins/worktree-activity"
SKILL = PACKAGE / "skills/worktree-activity"
HELPER = SKILL / "scripts/worktree_activity.py"
SCHEMA = SKILL / "references/worktree-activity-v1.schema.json"
OWNER = "019a1111-1111-7111-8111-111111111111"
OTHER = "019a2222-2222-7222-8222-222222222222"
CHILD = "019a3333-3333-7333-8333-333333333333"
SESSION = "019a4444-4444-7444-8444-444444444444"


def clean_env(owner: str | None = OWNER) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("CODEX_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    if owner is not None:
        env["CODEX_THREAD_ID"] = owner
        env["CODEX_SESSION_ID"] = SESSION
    return env


def git(path: Path, *arguments: str) -> str:
    result = subprocess.run(["git", "-C", str(path), *arguments], env=clean_env(None),
                            text=True, capture_output=True, timeout=15)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


class WorktreeActivityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="worktree activity tést ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.project = self.base / "primary project"
        self.project.mkdir()
        git(self.project, "init", "-b", "main")
        git(self.project, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "--allow-empty", "-m", "fixture")
        self.worktree = self.new_worktree("feature ünicode", "codex/fixture")

    def new_worktree(self, name: str, branch: str) -> Path:
        path = self.project / ".worktrees" / name
        git(self.project, "worktree", "add", "-b", branch, str(path))
        return path

    def cli(self, *arguments: object, owner: str | None = OWNER, ok: bool = True,
            env: dict[str, str] | None = None, helper: Path = HELPER,
            cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        result = subprocess.run([sys.executable, str(helper), *map(str, arguments)],
                                env=env or clean_env(owner), cwd=cwd or self.base,
                                capture_output=True, text=True, timeout=30)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def register(self, task: str = "implement", *, owner: str = OWNER,
                 worktree: Path | None = None) -> dict:
        target = worktree or self.worktree
        self.cli("register", "--worktree", target, "--coordinator", "--surface", "codex-desktop",
                 "--task-id", task, "--description", "Implement and verify assignment", owner=owner)
        return self.record(owner, target)

    def path(self, owner: str = OWNER, worktree: Path | None = None) -> Path:
        return (worktree or self.worktree) / ".agent-activity" / (owner + ".activity.json")

    def record(self, owner: str = OWNER, worktree: Path | None = None) -> dict:
        return json.loads(self.path(owner, worktree).read_text())

    def task(self, task: str = "implement", **fields: str) -> None:
        arguments = ["task", "--worktree", str(self.worktree), "--coordinator", "--task-id", task]
        for key, value in fields.items():
            arguments += ["--" + key.replace("_", "-"), value]
        self.cli(*arguments)

    def test_two_roots_are_independent_and_finalize_preserves_other(self) -> None:
        self.register()
        self.register(owner=OTHER)
        other = self.path(OTHER).read_bytes()
        self.task(status="completed", verification="Focused regression passed")
        self.cli("finalize", "--worktree", self.worktree, "--coordinator")
        self.assertFalse(self.path().exists())
        self.assertEqual(self.path(OTHER).read_bytes(), other)
        self.assertTrue(self.path().parent.is_dir())

    def test_recovery_groups_worktrees_by_root_and_never_targets_assignees(self) -> None:
        second = self.new_worktree("second", "codex/second")
        self.register()
        self.register(worktree=second)
        self.task(assignee_thread_id=CHILD)
        result = self.cli("recovery", self.project, "--json", owner=None)
        value = json.loads(result.stdout)
        rendered = json.dumps(value)
        self.assertIn(OWNER, rendered)
        self.assertEqual(rendered.count("codex://threads/" + OWNER), 1)
        self.assertNotIn("codex://threads/" + CHILD, rendered)
        self.assertEqual(len(list(self.worktree.glob(".agent-activity/*.activity.json"))), 1)

    def test_recovery_consolidates_same_root_across_explicit_projects(self) -> None:
        self.register()
        other_project = self.base / "another project"
        other_project.mkdir()
        git(other_project, "init", "-b", "main")
        git(other_project, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "--allow-empty", "-m", "fixture")
        other_worktree = other_project / ".worktrees" / "feature"
        git(other_project, "worktree", "add", "-b", "codex/other", str(other_worktree))
        self.register(worktree=other_worktree)
        result = json.loads(self.cli("recovery", self.project, other_project, "--json", owner=None).stdout)
        self.assertEqual(len(result["owners"]), 1)
        self.assertEqual(result["owners"][0]["root_thread_id"], OWNER)
        self.assertEqual(len(result["owners"][0]["worktrees"]), 2)

    def test_repeated_registration_preserves_tasks_registration_and_progress(self) -> None:
        first = self.register()
        self.task(status="blocked", note="Waiting for approved fixture")
        blocked = self.record()
        self.task(status="blocked", note="Waiting for approved fixture")
        self.assertEqual(self.record(), blocked)
        again = self.register()
        self.assertEqual(again, blocked)
        self.assertEqual(again["tasks"][0]["registered_at"], first["tasks"][0]["registered_at"])
        self.register("additional")
        self.assertEqual(len(self.record()["tasks"]), 2)
        self.assertEqual(self.record()["tasks"][0], blocked["tasks"][0])

    def test_register_does_not_reopen_completed_task(self) -> None:
        self.register()
        self.task(status="completed", verification="Verified result")
        complete = self.record()
        self.register()
        self.assertEqual(self.record(), complete)
        before = self.path().read_bytes()
        self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                 "--status", "in_progress", ok=False)
        self.assertEqual(self.path().read_bytes(), before)

    def test_owner_identity_is_required_and_read_only_inspection_needs_none(self) -> None:
        self.register()
        before = self.path().read_bytes()
        for owner in (None, "../../escape", "not-a-native-id"):
            self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                     "--note", "must not write", owner=owner, ok=False)
        self.cli("inspect", "--worktree", self.worktree, owner=None)
        self.cli("validate", self.path(), owner=None)
        self.assertEqual(self.path().read_bytes(), before)

    def test_other_root_cannot_update_original_owner_record(self) -> None:
        self.register()
        before = self.path().read_bytes()
        self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                 "--note", "cannot impersonate", owner=OTHER, ok=False)
        self.cli("task", "--worktree", self.worktree, "--coordinator", "--root-id", OWNER,
                 "--task-id", "implement", owner=OTHER, ok=False)
        self.assertEqual(self.path().read_bytes(), before)

    def test_coordinator_assertion_required_and_session_identity_not_owner(self) -> None:
        self.cli("register", "--worktree", self.worktree, "--surface", "codex-desktop",
                 "--task-id", "implement", "--description", "Assignment", ok=False)
        self.register(owner=OTHER)  # Independent user-facing fork has its own thread.
        value = self.record(OTHER)
        self.assertEqual(value["root_thread_id"], OTHER)
        self.assertEqual(value["session_id"], SESSION)
        self.assertNotEqual(value["root_thread_id"], value["session_id"])

    def test_unavailable_session_is_null_and_surface_explicit(self) -> None:
        env = clean_env()
        env.pop("CODEX_SESSION_ID")
        self.cli("register", "--worktree", self.worktree, "--coordinator", "--surface", "codex-cli",
                 "--task-id", "implement", "--description", "Assignment", env=env)
        self.assertIsNone(self.record()["session_id"])
        self.assertEqual(self.record()["session_type"], "codex-cli")

    def test_finalization_refuses_unfinished_or_unverified_and_cancellation_needs_authority(self) -> None:
        self.register()
        self.cli("finalize", "--worktree", self.worktree, "--coordinator", ok=False)
        self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                 "--status", "completed", ok=False)
        for fields in ([], ["--cancellation-reason", "No longer needed"],
                       ["--authorization-ref", "User request in fixture"]):
            self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                     "--status", "canceled", *fields, ok=False)
        self.task(status="canceled", cancellation_reason="User withdrew assignment",
                  authorization_ref="Explicit user cancellation in fixture")
        self.cli("finalize", "--worktree", self.worktree, "--coordinator")
        self.assertFalse(self.path().exists())

    def test_old_records_never_expire_and_reads_do_not_refresh_progress(self) -> None:
        value = self.register()
        for task in value["tasks"]:
            task["registered_at"] = task["last_activity"] = "2000-01-01T00:00:00Z"
        self.path().write_text(json.dumps(value))
        before = self.path().read_bytes()
        for command in (("inspect", "--worktree", self.worktree), ("scan", self.project, "--json"),
                        ("recovery", self.project, "--json")):
            self.cli(*command, owner=None)
        self.assertEqual(self.path().read_bytes(), before)

    def test_detached_head_records_null_branch_and_target_not_shell_directory(self) -> None:
        git(self.worktree, "checkout", "--detach")
        value = self.register()
        self.assertIsNone(value["branch"])
        self.assertEqual(value["worktree_path"], str(self.worktree))
        self.assertNotEqual(value["worktree_path"], str(self.base))

    def test_branch_discrepancy_requires_explicit_reconciliation(self) -> None:
        self.register()
        git(self.worktree, "checkout", "-b", "codex/renamed")
        before = self.path().read_bytes()
        self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                 "--note", "do not reconcile silently", ok=False)
        self.assertEqual(self.path().read_bytes(), before)
        self.cli("reconcile", "--worktree", self.worktree, "--coordinator")
        self.assertEqual(self.record()["branch"], "codex/renamed")
        self.task(note="Metadata reconciled")

    def test_moved_worktree_metadata_requires_explicit_reconciliation(self) -> None:
        self.register()
        moved = self.project / ".worktrees" / "moved worktree"
        git(self.project, "worktree", "move", str(self.worktree), str(moved))
        self.worktree = moved
        old = self.path().read_bytes()
        self.cli("register", "--worktree", moved, "--coordinator", "--surface", "codex-desktop",
                 "--task-id", "implement", "--description", "Assignment", ok=False)
        self.assertEqual(self.path().read_bytes(), old)
        self.cli("reconcile", "--worktree", moved, "--coordinator")
        self.assertEqual(self.record()["worktree_path"], str(moved))

    def test_primary_checkout_is_not_registration_target(self) -> None:
        self.cli("register", "--worktree", self.project, "--coordinator", "--surface", "codex-desktop",
                 "--task-id", "implement", "--description", "Assignment", ok=False)
        self.assertFalse((self.project / ".agent-activity").exists())

    def test_external_registered_worktree_is_supported_warned_and_scanned(self) -> None:
        outside = self.base / "outside"
        git(self.project, "worktree", "add", "-b", "codex/outside", str(outside))
        # Existing worktree acceptance does not create or traverse other projects.
        unrelated = self.base / "unrelated project"
        unrelated.mkdir()
        git(unrelated, "init", "-b", "main")
        sentinel = unrelated / ".agent-activity" / (OTHER + ".activity.json")
        sentinel.parent.mkdir()
        sentinel.write_text("must not scan this unrequested project")
        before = sentinel.read_bytes()

        empty = json.loads(self.cli("scan", self.project, "--json", owner=None).stdout)
        self.assertFalse((outside / ".agent-activity").exists())
        self.assertIn(str(outside), {warning["path"] for warning in empty["warnings"]})

        registered = json.loads(self.cli("register", "--worktree", outside, "--coordinator",
                                        "--surface", "codex-desktop", "--task-id", "external",
                                        "--description", "Existing external worktree assignment", "--json").stdout)
        self.assertEqual(registered["record"]["worktree_path"], str(outside))
        self.assertTrue(self.path(worktree=outside).is_file())
        self.assertIn(str(outside), {warning["path"] for warning in registered["warnings"]})
        self.cli("task", "--worktree", outside, "--coordinator", "--task-id", "external",
                 "--status", "blocked", "--note", "Awaiting result")
        self.assertEqual(self.record(worktree=outside)["tasks"][0]["status"], "blocked")
        for command in ("inspect", "validate", "scan", "recovery"):
            arguments = {"inspect": ["--worktree", outside], "validate": [self.path(worktree=outside)],
                         "scan": [self.project], "recovery": [self.project]}[command]
            value = json.loads(self.cli(command, *arguments, "--json", owner=None).stdout)
            self.assertFalse(value.get("errors"), value)
            self.assertIn(str(outside), {warning["path"] for warning in value["warnings"]})
            if command in ("scan", "recovery"):
                self.assertEqual({item["record"]["worktree_path"] for item in value["records"]}, {str(outside)})
        self.cli("task", "--worktree", outside, "--coordinator", "--task-id", "external",
                 "--status", "completed", "--verification", "External assignment verified")
        self.cli("finalize", "--worktree", outside, "--coordinator")
        self.assertFalse(self.path(worktree=outside).exists())
        self.assertEqual(sentinel.read_bytes(), before)

    def test_stale_git_registration_cannot_scan_reused_unrelated_worktree(self) -> None:
        self.register()
        valid_target = self.new_worktree("still owned", "codex/still-owned")
        self.register(worktree=valid_target)
        displaced = self.base / "displaced interrupted checkout"
        # Deliberately reproduce stale Git metadata inside this disposable fixture.
        # Repairing the move would remove the failure condition under test.
        self.worktree.rename(displaced)
        displaced_record = self.path(worktree=displaced)
        displaced_before = displaced_record.read_bytes()

        unrelated = self.base / "unrelated replacement primary"
        unrelated.mkdir()
        git(unrelated, "init", "-b", "main")
        git(unrelated, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "--allow-empty", "-m", "fixture")
        git(unrelated, "worktree", "add", "-b", "codex/replacement", str(self.worktree))
        self.register(owner=OTHER)
        unrelated_record = self.path(OTHER)
        unrelated_before = unrelated_record.read_bytes()
        requested_before = self.path(worktree=valid_target).read_bytes()

        for command in ("scan", "recovery"):
            with self.subTest(command=command):
                result = self.cli(command, self.project, "--json", owner=None, ok=False)
                self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                value = json.loads(result.stdout)
                self.assertTrue(value["errors"])
                self.assertIn(str(self.worktree), {error["path"] for error in value["errors"]})
                self.assertEqual({item["record"]["worktree_path"] for item in value["records"]},
                                 {str(valid_target)})
                self.assertNotIn(OTHER, json.dumps(value))
                if command == "recovery":
                    self.assertEqual([item["root_thread_id"] for item in value["owners"]], [OWNER])
        # Explicitly requesting the second primary authorizes its own scan. The
        # stale entry from the first primary must not suppress that valid target.
        both = json.loads(self.cli("recovery", self.project, unrelated, "--json",
                                   owner=None, ok=False).stdout)
        self.assertTrue(both["errors"])
        self.assertEqual({item["record"]["worktree_path"] for item in both["records"]},
                         {str(valid_target), str(self.worktree)})
        self.assertEqual(len(both["records"]), 2)
        self.assertEqual({item["root_thread_id"] for item in both["owners"]}, {OWNER, OTHER})
        self.assertEqual(unrelated_record.read_bytes(), unrelated_before)
        self.assertEqual(displaced_record.read_bytes(), displaced_before)
        self.assertEqual(self.path(worktree=valid_target).read_bytes(), requested_before)

    def test_corrupt_unsupported_duplicate_and_wrong_filename_records_are_preserved(self) -> None:
        original = self.register()
        alterations = ["{", json.dumps({**original, "schema_version": 2}),
                       json.dumps({**original, "tasks": original["tasks"] * 2}),
                       json.dumps({**original, "root_thread_id": OTHER})]
        for content in alterations:
            with self.subTest(content=content):
                self.path().write_text(content)
                self.cli("validate", self.path(), owner=None, ok=False)
                self.cli("register", "--worktree", self.worktree, "--coordinator", "--surface", "codex-desktop",
                         "--task-id", "implement", "--description", "Assignment", ok=False)
                self.assertEqual(self.path().read_text(), content)

    def test_schema_rejects_wrong_formats_unknown_fields_and_semantic_duplicates(self) -> None:
        valid = self.register()
        schema = json.loads(SCHEMA.read_text())
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertEqual(list(validator.iter_errors(valid)), [])
        cases = []
        for field, value in (("schema_version", True), ("schema_version", 2), ("root_thread_id", "../../bad"),
                             ("session_id", "invented"), ("worktree_path", "relative"),
                             ("tasks", []), ("unexpected", "field")):
            altered = deepcopy(valid)
            altered[field] = value
            cases.append(altered)
        for field, value in (("description", ""), ("status", "running"), ("registered_at", "not-a-time"),
                             ("registered_at", "2026-02-30T12:00:00Z"),
                             ("last_activity", "2026-11-10T12:00:00+01:00"), ("id", "../escape"),
                             ("assignee_thread_id", "not-native")):
            altered = deepcopy(valid)
            altered["tasks"][0][field] = value
            cases.append(altered)
        for altered in cases:
            with self.subTest(record=altered):
                self.assertTrue(list(validator.iter_errors(altered)))

    def test_impossible_utc_date_fails_runtime_validation_without_overwrite(self) -> None:
        value = self.register()
        value["tasks"][0]["registered_at"] = "2026-02-30T12:00:00Z"
        self.path().write_text(json.dumps(value))
        before = self.path().read_bytes()
        self.cli("validate", self.path(), owner=None, ok=False)
        self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                 "--note", "invalid date must survive", ok=False)
        self.assertEqual(self.path().read_bytes(), before)

    def test_newline_suffixed_identifiers_fail_schema_and_runtime(self) -> None:
        original = self.register()
        validator = Draft202012Validator(json.loads(SCHEMA.read_text()), format_checker=FormatChecker())
        for field in ("session_id", "assignee_thread_id", "id"):
            value = deepcopy(original)
            if field == "session_id":
                value[field] = SESSION + "\n"
            else:
                value["tasks"][0][field] = (CHILD if field == "assignee_thread_id" else "implement") + "\n"
            with self.subTest(field=field):
                self.assertTrue(list(validator.iter_errors(value)))
                self.path().write_text(json.dumps(value))
                before = self.path().read_bytes()
                self.cli("validate", self.path(), owner=None, ok=False)
                self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                         "--note", "must preserve malformed evidence", ok=False)
                self.assertEqual(self.path().read_bytes(), before)

    def test_validation_rejects_nested_registry_even_with_correct_record_metadata(self) -> None:
        self.register()
        nested = self.worktree / "subdirectory" / ".agent-activity" / self.path().name
        nested.parent.mkdir(parents=True)
        nested.write_bytes(self.path().read_bytes())
        self.cli("validate", nested, owner=None, ok=False)

    def test_symlink_record_and_activity_directory_are_never_followed(self) -> None:
        self.register()
        saved = self.path().read_bytes()
        target = self.base / "valuable.json"
        target.write_bytes(saved)
        self.path().unlink()
        self.path().symlink_to(target)
        self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                 "--note", "unsafe", ok=False)
        self.cli("scan", self.project, "--json", owner=None, ok=False)
        self.assertEqual(target.read_bytes(), saved)
        self.path().unlink()
        # Stable mutex files intentionally remain, so use a fresh worktree.
        second = self.new_worktree("symlink activity", "codex/symlink")
        (second / ".agent-activity").symlink_to(target.parent, target_is_directory=True)
        self.cli("register", "--worktree", second, "--coordinator", "--surface", "codex-desktop",
                 "--task-id", "implement", "--description", "Assignment", ok=False)
        self.assertFalse((target.parent / (OWNER + ".activity.json")).exists())

    def test_scan_is_read_only_bounded_and_exposes_partial_errors(self) -> None:
        self.register()
        second = self.new_worktree("invalid", "codex/invalid")
        (second / ".agent-activity").mkdir()
        (second / ".agent-activity" / (OTHER + ".activity.json")).write_text("{")
        before = {str(p): p.read_bytes() for p in self.project.glob(".worktrees/*/.agent-activity/*") if p.is_file()}
        result = self.cli("scan", self.project, "--json", owner=None, ok=False)
        value = json.loads(result.stdout)
        self.assertIn(OWNER, json.dumps(value))
        self.assertIn("errors", value)
        self.assertTrue(value["errors"])
        self.cli("scan", self.project, "--json", "--max-worktrees", "1", owner=None, ok=False)
        after = {str(p): p.read_bytes() for p in self.project.glob(".worktrees/*/.agent-activity/*") if p.is_file()}
        self.assertEqual(after, before)

    def test_empty_read_only_scan_creates_no_registry_and_partial_recovery_is_explicit(self) -> None:
        self.cli("scan", self.project, "--json", owner=None)
        self.assertFalse((self.worktree / ".agent-activity").exists())
        self.register()
        self.register(owner=OTHER)
        bounded = json.loads(self.cli("scan", self.project, "--max-records", "1", "--json",
                                     owner=None, ok=False).stdout)
        self.assertTrue(bounded["errors"])
        partial = json.loads(self.cli("recovery", self.project, self.base / "missing project", "--json",
                                     owner=None, ok=False).stdout)
        self.assertTrue(partial["errors"])
        self.assertEqual({item["root_thread_id"] for item in partial["owners"]}, {OWNER, OTHER})

    def test_unreadable_registry_is_partial_error_not_empty_success(self) -> None:
        self.register()
        second = self.new_worktree("unreadable registry", "codex/unreadable")
        directory = second / ".agent-activity"
        directory.mkdir()
        directory.chmod(0)
        try:
            result = json.loads(self.cli("scan", self.project, "--json", owner=None, ok=False).stdout)
        finally:
            directory.chmod(0o700)
        self.assertTrue(result["errors"])
        self.assertIn(OWNER, json.dumps(result["records"]))

    def test_concurrent_additions_do_not_lose_tasks_and_readers_see_complete_json(self) -> None:
        self.register()
        stop = threading.Event()
        invalid: list[str] = []
        def read_until_done() -> None:
            while not stop.is_set():
                try:
                    json.loads(self.path().read_bytes())
                except Exception as error:
                    invalid.append(repr(error))
                    return
        reader = threading.Thread(target=read_until_done)
        reader.start()
        try:
            def add(index: int) -> None:
                self.task("parallel-" + str(index), description="Independent delegated task " + str(index))
            with ThreadPoolExecutor(max_workers=8) as executor:
                list(executor.map(add, range(12)))
        finally:
            stop.set()
            reader.join(timeout=5)
        self.assertFalse(invalid, invalid)
        self.assertEqual({t["id"] for t in self.record()["tasks"]}, {"implement", *("parallel-" + str(i) for i in range(12))})

    def test_update_finalize_contention_never_deletes_unfinished_or_resurrects_record(self) -> None:
        self.register()
        self.task(status="completed", verification="Verified initial task")
        barrier = threading.Barrier(2)
        def invoke(arguments: list[str]) -> subprocess.CompletedProcess[str]:
            barrier.wait(timeout=10)
            return subprocess.run([sys.executable, str(HELPER), *arguments],
                                  env=clean_env(), capture_output=True, text=True, timeout=30)
        with ThreadPoolExecutor(max_workers=2) as executor:
            added = executor.submit(invoke, ["task", "--worktree", str(self.worktree), "--coordinator",
                                            "--task-id", "new-assignment", "--description", "Unfinished work"])
            finalized = executor.submit(invoke, ["finalize", "--worktree", str(self.worktree), "--coordinator"])
            add_result, final_result = added.result(), finalized.result()
        self.assertEqual(sorted([add_result.returncode == 0, final_result.returncode == 0]), [False, True],
                         add_result.stdout + add_result.stderr + final_result.stdout + final_result.stderr)
        if add_result.returncode == 0:
            self.assertIn("new-assignment", {t["id"] for t in self.record()["tasks"]})
        else:
            self.assertFalse(self.path().exists())

    def test_packaged_helper_relocates_and_runs_from_unrelated_checkout(self) -> None:
        # Other tools may have left ignored bytecode in the shared source tree.
        # Preserve it and validate a clean disposable package copy instead.
        clean_source = self.base / "clean source" / "worktree-activity"
        shutil.copytree(PACKAGE, clean_source, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        destination = self.base / "relocated plugin ü" / "worktree-activity"
        result = subprocess.run([sys.executable, str(ROOT / "scripts/check_distribution_bundle.py"),
                                 str(clean_source), "--output", str(destination)], env=clean_env(None),
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        helper = destination / "skills/worktree-activity/scripts/worktree_activity.py"
        self.assertTrue(helper.is_file())
        self.cli("register", "--worktree", self.worktree, "--coordinator", "--surface", "codex-desktop",
                 "--task-id", "relocated", "--description", "Relocated package works", helper=helper,
                 cwd=self.project)
        self.assertEqual(self.record()["tasks"][0]["id"], "relocated")
        self.assertFalse((destination / ".agent-activity").exists())

    def test_failed_atomic_replacement_preserves_last_valid_record(self) -> None:
        self.register()
        before = self.path().read_bytes()
        spec = importlib.util.spec_from_file_location("worktree_activity_tested", HELPER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        error_output = io.StringIO()
        with redirect_stderr(error_output), mock.patch.dict(os.environ, clean_env(), clear=True), mock.patch.object(
                module.os, "replace", side_effect=OSError("injected replacement failure")):
            result = module.main(["task", "--worktree", str(self.worktree), "--coordinator",
                                  "--task-id", "implement", "--note", "must not replace"])
        self.assertNotEqual(result, 0)
        self.assertIn("injected replacement failure", error_output.getvalue())
        self.assertEqual(self.path().read_bytes(), before)
        self.cli("validate", self.path(), owner=None)

    def test_contract_fixtures_agree_with_published_schema(self) -> None:
        validator = Draft202012Validator(json.loads(SCHEMA.read_text()), format_checker=FormatChecker())
        fixtures = ROOT / "tests/fixtures/worktree-activity"
        self.assertEqual(list(validator.iter_errors(json.loads((fixtures / "valid.json").read_text()))), [])
        self.assertTrue(list(validator.iter_errors(json.loads((fixtures / "invalid-timestamp.json").read_text()))))
        self.assertTrue(list(validator.iter_errors(json.loads((fixtures / "invalid-calendar-date.json").read_text()))))
        for example in (SKILL / "examples").glob("valid-*.json"):
            with self.subTest(example=example.name):
                self.assertEqual(list(validator.iter_errors(json.loads(example.read_text()))), [])
        unknown = SKILL / "examples/invalid-unknown-version.json"
        self.assertTrue(list(validator.iter_errors(json.loads(unknown.read_text()))))

    def test_lock_timeout_preserves_record_and_mutex_target(self) -> None:
        self.register()
        before = self.path().read_bytes()
        mutex = self.path().parent / ("." + OWNER + ".mutex")
        self.assertTrue(mutex.is_file())
        with mutex.open("r+") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            inode = mutex.stat().st_ino
            self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                     "--note", "contended", "--lock-timeout", "0.05", ok=False)
            self.assertEqual(mutex.stat().st_ino, inode)
        self.assertEqual(self.path().read_bytes(), before)

    def test_unsafe_record_filename_and_mutex_symlink_are_visible_errors(self) -> None:
        self.register()
        unsafe = self.path().parent / "not-native.activity.json"
        unsafe.write_bytes(self.path().read_bytes())
        self.cli("scan", self.project, "--json", owner=None, ok=False)
        unsafe.unlink()
        mutex = self.path().parent / ("." + OWNER + ".mutex")
        mutex.unlink()
        protected = self.base / "protected mutex"
        protected.write_text("untouched")
        mutex.symlink_to(protected)
        before = self.path().read_bytes()
        self.cli("task", "--worktree", self.worktree, "--coordinator", "--task-id", "implement",
                 "--note", "unsafe mutex", ok=False)
        self.assertEqual(protected.read_text(), "untouched")
        self.assertEqual(self.path().read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
