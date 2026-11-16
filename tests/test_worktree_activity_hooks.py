"""PostToolUse activation preserves trust, correlates asynchronous creation, and relocates.

Fixtures emulate native tool results; no Git worktrees or user settings are created.
The hook supplies instructions only. It must never mutate ownership records.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "plugins/worktree-activity"
SCRIPT_RELATIVE = Path("skills/worktree-activity/scripts/post_tool_use.py")
SKILL_RELATIVE = Path("skills/worktree-activity/SKILL.md")
OPERATION = "worktree-test-operation-a"
OTHER_OPERATION = "worktree-test-operation-b"


class WorktreeActivityHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="activity hook tést ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.package = self.base / "plugin source ü" / "worktree-activity"
        shutil.copytree(PACKAGE, self.package, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.data = self.base / "plugin data ü"
        self.checkout = self.base / "fixture checkout ü"
        self.registry = self.checkout / ".agent-activity" / "019a1111-1111-7111-8111-111111111111.activity.json"
        self.registry.parent.mkdir(parents=True)
        self.registry.write_bytes(b"Existing recoverable evidence; hook must not read or mutate registry.\n")
        self.registry_before = self.registry.read_bytes()

    def tearDown(self) -> None:
        self.assertEqual(self.registry.read_bytes(), self.registry_before)
        self.assertEqual(list(self.registry.parent.iterdir()), [self.registry])

    def environment(self, *, package: Path | None = None, data: Path | None = None) -> dict[str, str]:
        env = {key: value for key, value in os.environ.items()
               if not key.startswith("CODEX_") and key not in {"PLUGIN_ROOT", "PLUGIN_DATA"}}
        env.update(PYTHONDONTWRITEBYTECODE="1", PLUGIN_ROOT=str(package or self.package),
                   PLUGIN_DATA=str(data or self.data))
        return env

    def created(self, **fields: object) -> dict:
        return {"type": "created", "worktreeGitRoot": str(self.checkout),
                "worktreeWorkspaceRoot": str(self.checkout), **fields}

    def event(self, payload: object, *, tool: str = "create_worktree",
              operation: str = OPERATION, wrapper: str = "plain") -> dict:
        if wrapper == "mcp":
            payload = {"content": [{"type": "text", "text": json.dumps(payload)}]}
        elif wrapper == "dynamic":
            payload = {"success": True, "contentItems": [{"type": "inputText", "text": json.dumps(payload)}]}
        elif wrapper == "native-text":
            payload = json.dumps(payload)
        return {"hook_event_name": "PostToolUse", "tool_name": "mcp__codex_app__" + tool,
                "tool_input": {"operationId": operation} if tool == "get_worktree_creation_status" else {},
                "tool_response": payload}

    def status(self, *, operation: str = OPERATION, stage: str = "completed",
               result: dict | None = None, **fields: object) -> dict:
        return {"operationId": operation, "stage": stage,
                "result": self.created() if result is None else result, **fields}

    def invoke(self, event: object, *, ok: bool = True, package: Path | None = None,
               env: dict[str, str] | None = None, raw: bool = False,
               command: str | None = None) -> subprocess.CompletedProcess[str]:
        target = package or self.package
        arguments = command if command is not None else [sys.executable, "-S", str(target / SCRIPT_RELATIVE)]
        result = subprocess.run(arguments, input=event if raw else json.dumps(event),
                                shell=command is not None, executable="/bin/sh" if command else None,
                                text=True, capture_output=True, timeout=10, cwd=self.base,
                                env=env or self.environment(package=target))
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def assert_injected(self, result: subprocess.CompletedProcess[str], *, package: Path | None = None) -> str:
        target = package or self.package
        value = json.loads(result.stdout)
        output = value["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "PostToolUse")
        context = output["additionalContext"]
        self.assertIn((target / SKILL_RELATIVE).read_text().strip(), context)
        self.assertIn(str(target / SKILL_RELATIVE), context)
        return context

    def pending(self, operation: str = OPERATION) -> Path:
        return self.data / "worktree-activity-pending" / (operation + ".pending")

    def begin_pending(self, operation: str = OPERATION) -> None:
        result = self.invoke(self.event({"type": "pending", "operationId": operation, "revision": 0,
                                        "stage": "preparing", "progress": None, "result": None}))
        self.assertEqual(result.stdout, "")
        self.assertTrue(self.pending(operation).is_file())

    def test_created_results_inject_trusted_skill_from_both_native_wrappers(self) -> None:
        for wrapper in ("mcp", "dynamic", "native-text"):
            with self.subTest(wrapper=wrapper):
                event = self.event(self.created(untrustedText="UNTRUSTED_TOOL_RESPONSE_INSTRUCTION"), wrapper=wrapper)
                # Native transport may signal setup failure after Git creation.
                if wrapper in ("mcp", "dynamic"):
                    event["tool_response"]["isError" if wrapper == "mcp" else "success"] = wrapper == "mcp"
                context = self.assert_injected(self.invoke(event))
                self.assertNotIn("UNTRUSTED_TOOL_RESPONSE_INSTRUCTION", context)
        self.assertFalse(self.data.exists())

    def test_physically_created_result_still_injects_when_setup_failed(self) -> None:
        result = self.invoke(self.event(self.created(setupError="Fixture setup command failed"), wrapper="mcp"))
        self.assert_injected(result)
        self.begin_pending()
        terminal = self.status(stage="failed", result=self.created(setupError="Fixture setup command failed"))
        self.assert_injected(self.invoke(self.event(terminal, tool="get_worktree_creation_status")))
        self.assertFalse(self.pending().exists())

    def test_unrelated_failed_missing_and_invalid_payloads_are_noops(self) -> None:
        events = [self.event({}), self.event({"type": "failed", "error": "Not created"}),
                  self.event({"type": "created", "worktreeGitRoot": "relative", "worktreeWorkspaceRoot": "relative"}),
                  self.event({"type": "created", "worktreeGitRoot": str(self.checkout)}),
                  self.event({"type": "pending"}), {}, [], None]
        unrelated = self.event(self.created())
        unrelated["tool_name"] = "mcp__codex_app__attach_worktree"
        events.append(unrelated)
        wrong_event = self.event(self.created())
        wrong_event["hook_event_name"] = "PreToolUse"
        events.append(wrong_event)
        for event in events:
            with self.subTest(event=event):
                self.assertEqual(self.invoke(event).stdout, "")
        for text in ("{", "", "not JSON"):
            self.assertEqual(self.invoke(text, raw=True).stdout, "")
        self.assertFalse(self.data.exists())

    def test_pending_only_injects_matching_completed_creation(self) -> None:
        self.begin_pending()
        mismatched = self.event(self.status(operation=OTHER_OPERATION), tool="get_worktree_creation_status")
        self.assertEqual(self.invoke(mismatched).stdout, "")
        self.assertTrue(self.pending().exists())
        missing_result = self.status()
        missing_result.pop("result")
        null_result = self.status()
        null_result["result"] = None
        invalid_result = self.status(result={"type": "created", "worktreeGitRoot": "relative",
                                             "worktreeWorkspaceRoot": "relative"})
        for malformed in (missing_result, null_result, invalid_result):
            self.assertEqual(self.invoke(self.event(malformed, tool="get_worktree_creation_status")).stdout, "")
            self.assertTrue(self.pending().exists())
        result = self.invoke(self.event(self.status(), tool="get_worktree_creation_status", wrapper="dynamic"))
        self.assert_injected(result)
        self.assertFalse(self.pending().exists())
        self.assertEqual(self.invoke(self.event(self.status(), tool="get_worktree_creation_status")).stdout, "")

    def test_unobserved_status_and_attachment_completion_do_not_inject(self) -> None:
        self.assertEqual(self.invoke(self.event(self.status(), tool="get_worktree_creation_status")).stdout, "")
        self.begin_pending()
        attached = self.status(result={"type": "attached", "worktreeGitRoot": str(self.checkout),
                                       "worktreeWorkspaceRoot": str(self.checkout)})
        self.assertEqual(self.invoke(self.event(attached, tool="get_worktree_creation_status")).stdout, "")
        self.assertTrue(self.pending().exists())

    def test_pending_polls_preserve_marker_regardless_of_age(self) -> None:
        self.begin_pending()
        os.utime(self.pending(), (1, 1))
        original = self.pending().stat().st_mtime_ns
        for stage in ("preparing", "creating", "registering"):
            status = self.status(stage=stage)
            status["result"] = None
            self.assertEqual(self.invoke(self.event(status,
                                                   tool="get_worktree_creation_status")).stdout, "")
            self.assertTrue(self.pending().exists())
            self.assertEqual(self.pending().stat().st_mtime_ns, original)
        self.assert_injected(self.invoke(self.event(self.status(), tool="get_worktree_creation_status")))

    def test_failed_terminal_removes_only_its_transient_marker(self) -> None:
        self.begin_pending()
        self.begin_pending(OTHER_OPERATION)
        failed = self.status(stage="failed", result={"type": "failed", "error": "Fixture failure"})
        self.assertEqual(self.invoke(self.event(failed, tool="get_worktree_creation_status")).stdout, "")
        self.assertFalse(self.pending().exists())
        self.assertTrue(self.pending(OTHER_OPERATION).exists())

    def test_independent_concurrent_pending_operations_retain_their_own_markers(self) -> None:
        operations = ["worktree-parallel-" + str(index) for index in range(8)]
        with ThreadPoolExecutor(max_workers=8) as executor:
            list(executor.map(self.begin_pending, operations))
        self.assertEqual({path.name for path in self.pending().parent.iterdir()},
                         {operation + ".pending" for operation in operations})
        def complete(operation: str) -> None:
            self.assert_injected(self.invoke(self.event(self.status(operation=operation),
                                                       operation=operation, tool="get_worktree_creation_status")))
        with ThreadPoolExecutor(max_workers=8) as executor:
            list(executor.map(complete, operations))
        self.assertEqual(list(self.pending().parent.iterdir()), [])

    def test_concurrent_completion_claims_same_operation_only_once(self) -> None:
        self.begin_pending()
        event = self.event(self.status(), tool="get_worktree_creation_status")
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: self.invoke(event), range(2)))
        self.assertEqual(sum(bool(result.stdout) for result in results), 1)
        self.assert_injected(next(result for result in results if result.stdout))
        self.assertFalse(self.pending().exists())

    def test_unsafe_operation_identifiers_never_escape_plugin_data(self) -> None:
        for operation in ("../outside", "/absolute", "unsafe/child", "unsafe\\child", "trailing\n", "a" * 129):
            with self.subTest(operation=operation):
                result = self.invoke(self.event({"type": "pending", "operationId": operation}))
                self.assertEqual(result.stdout, "")
        self.assertFalse(self.data.exists())
        self.assertFalse((self.base / "outside.pending").exists())

    def test_symlink_pending_directory_and_marker_cannot_write_outside_data(self) -> None:
        outside = self.base / "outside protected"
        outside.mkdir()
        self.data.mkdir()
        self.pending().parent.symlink_to(outside, target_is_directory=True)
        self.invoke(self.event({"type": "pending", "operationId": OPERATION}), ok=False)
        self.assertEqual(list(outside.iterdir()), [])
        self.pending().parent.unlink()
        self.pending().parent.mkdir()
        protected = outside / "protected"
        protected.write_text("preserve")
        self.pending().symlink_to(protected)
        self.invoke(self.event(self.status(), tool="get_worktree_creation_status"), ok=False)
        self.assertEqual(protected.read_text(), "preserve")
        self.assertTrue(self.pending().is_symlink())

    def test_missing_skill_errors_before_consuming_pending_recovery_context(self) -> None:
        self.begin_pending()
        path = self.package / SKILL_RELATIVE
        saved = path.read_bytes()
        path.unlink()
        try:
            self.invoke(self.event(self.created()), ok=False)
            self.invoke(self.event(self.status(), tool="get_worktree_creation_status"), ok=False)
            self.assertTrue(self.pending().exists())
        finally:
            path.write_bytes(saved)
        self.assert_injected(self.invoke(self.event(self.status(), tool="get_worktree_creation_status")))
        self.assertFalse(self.pending().exists())

    def test_missing_plugin_data_does_not_block_immediate_creation_but_cannot_track_pending(self) -> None:
        env = self.environment()
        env.pop("PLUGIN_DATA")
        self.assert_injected(self.invoke(self.event(self.created()), env=env))
        self.invoke(self.event({"type": "pending", "operationId": OPERATION}), env=env, ok=False)
        self.assertFalse(self.data.exists())

    def test_packaged_native_hook_command_runs_after_relocation(self) -> None:
        relocated = self.base / "relocated distribution ü" / "worktree-activity"
        build = subprocess.run([sys.executable, str(ROOT / "scripts/check_distribution_bundle.py"),
                                str(self.package), "--output", str(relocated)],
                               env=self.environment(), text=True, capture_output=True, timeout=20)
        self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
        # The portable OpenAI extension owns the packaged hook declaration.
        manifest = json.loads((relocated / "plugin.json").read_text())
        selected = manifest["extensions"]["com.openai"]
        hook_config = json.loads((relocated / selected["hooks"]).read_text())
        matches = [entry for entry in hook_config["hooks"]["PostToolUse"]
                   if re.fullmatch(entry["matcher"], "mcp__codex_app__create_worktree")]
        self.assertTrue(matches)
        command = matches[0]["hooks"][0]["command"]
        self.assertTrue((relocated / SCRIPT_RELATIVE).is_file())
        result = self.invoke(self.event(self.created(), wrapper="mcp"), package=relocated, command=command)
        self.assert_injected(result, package=relocated)
        self.assertFalse((relocated / ".agent-activity").exists())

    def test_explicit_toml_configuration_executes_its_declared_command(self) -> None:
        template = self.package / "skills/worktree-activity/references/post-tool-use.toml"
        config = tomllib.loads(template.read_text())
        entry = config["hooks"]["PostToolUse"][0]
        portable = json.loads((self.package / "plugin.json").read_text())
        hook_path = portable["extensions"]["com.openai"]["hooks"]
        packaged = json.loads((self.package / hook_path).read_text())
        self.assertEqual(entry["matcher"], packaged["hooks"]["PostToolUse"][0]["matcher"])
        self.assertIsNotNone(re.fullmatch(entry["matcher"], "mcp__codex_app__create_worktree"))
        command = entry["hooks"][0]["command"]
        command = command.replace("/absolute/path/to/worktree-activity-data", str(self.data))
        command = command.replace("/absolute/path/to/worktree-activity", str(self.package))
        env = self.environment()
        env.pop("PLUGIN_DATA")
        env.pop("PLUGIN_ROOT")
        self.assert_injected(self.invoke(self.event(self.created(), wrapper="native-text"),
                                         env=env, command=command))
        pending = self.event({"type": "pending", "operationId": OPERATION}, wrapper="native-text")
        self.assertEqual(self.invoke(pending, env=env, command=command).stdout, "")
        self.assertTrue(self.pending().is_file())
        completed = self.event(self.status(), tool="get_worktree_creation_status", wrapper="native-text")
        self.assert_injected(self.invoke(completed, env=env, command=command))
        self.assertFalse(self.pending().exists())


if __name__ == "__main__":
    unittest.main()
