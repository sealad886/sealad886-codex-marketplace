from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).parents[1]
PROJECT_DELIVERY_ROOT = REPOSITORY_ROOT / "plugins" / "project-delivery"
CONVERSATION_VISUALS_ROOT = REPOSITORY_ROOT / "plugins" / "conversation-visuals"
CHECKER = REPOSITORY_ROOT / "scripts" / "check_distribution_bundle.py"
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_distribution_bundle import materialize_runtime_closure  # noqa: E402


UNIVERSAL_FORBIDDEN_PARTS = {
    ".git",
    ".github",
    ".venv",
    "__pycache__",
    "node_modules",
    "tests",
}
SUBPROCESS_TIMEOUT_SECONDS = 30


def run_checker(
    *arguments: str,
    root: Path = PROJECT_DELIVERY_ROOT,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root), *arguments],
        check=False,
        capture_output=True,
        text=True,
        timeout=SUBPROCESS_TIMEOUT_SECONDS,
    )


def copy_conversation_visuals(temporary: str) -> Path:
    source = Path(temporary) / "source" / "conversation-visuals"
    shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
    return source


def write_mcp_server(source: Path, server: object) -> None:
    (source / ".mcp.json").write_text(
        json.dumps({"mcpServers": {"conversation-visuals": server}}),
        encoding="utf-8",
    )


class DistributionBundleTests(unittest.TestCase):
    def test_project_delivery_package_still_validates(self) -> None:
        result = run_checker()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("plugin=project-delivery", result.stdout)
        self.assertIn("skills=13", result.stdout)

    def test_conversation_visuals_materializes_declared_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "conversation-visuals"
            result = run_checker(
                "--output",
                str(output),
                root=CONVERSATION_VISUALS_ROOT,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("plugin=conversation-visuals", result.stdout)
            self.assertIn("skills=4", result.stdout)
            self.assertTrue((output / ".mcp.json").is_file())
            self.assertTrue((output / "mcp" / "server.py").is_file())
            packaged_self_test = subprocess.run(
                [sys.executable, str(output / "mcp" / "server.py"), "--self-test"],
                check=False,
                capture_output=True,
                text=True,
                timeout=SUBPROCESS_TIMEOUT_SECONDS,
            )
            self.assertEqual(
                packaged_self_test.returncode,
                0,
                packaged_self_test.stdout + packaged_self_test.stderr,
            )
            files = [path for path in output.rglob("*") if path.is_file()]
            for path in files:
                self.assertFalse(
                    UNIVERSAL_FORBIDDEN_PARTS.intersection(
                        path.relative_to(output).parts
                    ),
                    path,
                )

    def test_missing_mcp_script_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            (source / "mcp" / "server.py").unlink()

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("script is not a regular file", result.stdout)

    def test_directory_as_mcp_script_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            script = source / "mcp" / "server.py"
            script.unlink()
            script.mkdir()

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("script is not a regular file", result.stdout)

    def test_absolute_and_escaping_mcp_scripts_are_rejected(self) -> None:
        invalid_scripts = (
            "/tmp/server.py",
            r"C:\Users\alice\server.py",
            "../outside.py",
        )
        for script in invalid_scripts:
            with (
                self.subTest(script=script),
                tempfile.TemporaryDirectory() as temporary,
            ):
                source = copy_conversation_visuals(temporary)
                write_mcp_server(
                    source,
                    {
                        "command": "python3",
                        "args": [script],
                        "cwd": ".",
                    },
                )

                result = run_checker(root=source)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("unsafe manifest path", result.stdout)

    def test_unsupported_mcp_launch_modes_are_rejected(self) -> None:
        launchers = (
            (
                {"command": "node", "args": ["./mcp/server.py"], "cwd": "."},
                "command must be python3",
            ),
            (
                {"command": "python3", "args": ["-m", "server"], "cwd": "."},
                "args must contain one Python script",
            ),
            (
                {"command": "python3", "args": ["-c", "pass"], "cwd": "."},
                "args must contain one Python script",
            ),
            (
                {
                    "command": "python3",
                    "args": ["./mcp/server.py"],
                    "cwd": "./mcp",
                },
                "cwd must be '.'",
            ),
            (
                {
                    "command": "python3",
                    "args": ["./mcp/server.py"],
                    "cwd": ".",
                    "env": {"TOKEN": "secret"},
                },
                "unsupported local MCP server fields: env",
            ),
            (
                {
                    "command": "python3",
                    "args": ["./mcp/server.py"],
                    "cwd": ".",
                    "tool_timeout_sec": 0,
                },
                "tool_timeout_sec must be a positive finite number",
            ),
            (
                {
                    "command": "python3",
                    "args": ["./mcp/server.py"],
                    "cwd": ".",
                    "tool_timeout_sec": float("nan"),
                },
                "non-standard JSON constant: NaN",
            ),
            (
                {
                    "command": "python3",
                    "args": ["./mcp/server.py"],
                    "cwd": ".",
                    "tool_timeout_sec": float("inf"),
                },
                "non-standard JSON constant: Infinity",
            ),
            (
                {"url": "https://example.invalid/mcp"},
                "unsupported local MCP server fields: url",
            ),
        )
        for server, expected_error in launchers:
            with (
                self.subTest(server=server),
                tempfile.TemporaryDirectory() as temporary,
            ):
                source = copy_conversation_visuals(temporary)
                write_mcp_server(source, server)

                result = run_checker(root=source)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_error, result.stdout)

    def test_inline_mcp_declaration_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            manifest_path = source / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["mcpServers"] = {
                "conversation-visuals": {
                    "command": "python3",
                    "args": ["./mcp/server.py"],
                    "cwd": ".",
                }
            }
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must declare a local config file", result.stdout)

    def test_conversation_visuals_requires_its_mcp_declaration(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            manifest_path = source / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.pop("mcpServers")
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must declare its local MCP config", result.stdout)

    def test_malformed_manifest_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            (source / ".codex-plugin" / "plugin.json").write_text(
                "{",
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("cannot resolve plugin identity", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_invalid_manifest_name_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            manifest_path = source / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["name"] = "bad/name"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("plugin name must be lower-case hyphen-case", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_replace_clean_distribution_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "conversation-visuals"
            first = run_checker(
                "--output",
                str(output),
                root=CONVERSATION_VISUALS_ROOT,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)

            second = run_checker(
                "--output",
                str(output),
                "--replace",
                root=CONVERSATION_VISUALS_ROOT,
            )

            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)

    def test_replace_distribution_with_extra_file_is_refused_and_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "conversation-visuals"
            first = run_checker(
                "--output",
                str(output),
                root=CONVERSATION_VISUALS_ROOT,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            extra = output / "user-notes.txt"
            extra.write_text("preserve me\n", encoding="utf-8")

            result = run_checker(
                "--output",
                str(output),
                "--replace",
                root=CONVERSATION_VISUALS_ROOT,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unclean output", result.stdout)
            self.assertEqual(extra.read_text(encoding="utf-8"), "preserve me\n")

    def test_replace_distribution_inside_git_ancestor_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkout = Path(temporary) / "checkout"
            (checkout / ".git").mkdir(parents=True)
            output = checkout / "prepared" / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, output)

            result = run_checker(
                "--output",
                str(output),
                "--replace",
                root=CONVERSATION_VISUALS_ROOT,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source checkout or Python environment", result.stdout)
            self.assertTrue((output / ".codex-plugin" / "plugin.json").is_file())

    def test_output_symlink_is_refused_without_touching_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            real_output = Path(temporary) / "real-conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, real_output)
            output = Path(temporary) / "conversation-visuals"
            output.symlink_to(real_output, target_is_directory=True)

            result = run_checker(
                "--output",
                str(output),
                "--replace",
                root=CONVERSATION_VISUALS_ROOT,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output symlink", result.stdout)
            self.assertTrue(output.is_symlink())
            self.assertTrue((real_output / ".codex-plugin" / "plugin.json").is_file())

    def test_failed_swap_restores_prior_clean_distribution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "conversation-visuals"
            first = run_checker(
                "--output",
                str(output),
                root=CONVERSATION_VISUALS_ROOT,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            prior_readme = (output / "README.md").read_bytes()
            original_replace = os.replace
            calls = 0

            def fail_staging_swap(source: object, destination: object) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected staging swap failure")
                original_replace(source, destination)

            with mock.patch(
                "check_distribution_bundle.os.replace",
                side_effect=fail_staging_swap,
            ):
                errors, _, _ = materialize_runtime_closure(
                    CONVERSATION_VISUALS_ROOT,
                    output,
                    replace=True,
                )

            self.assertTrue(errors)
            self.assertIn("prior output was preserved", errors[0])
            self.assertEqual((output / "README.md").read_bytes(), prior_readme)
            self.assertFalse(
                list(output.parent.glob(".conversation-visuals-previous-*")),
                "a successful rollback must not leave a hidden backup",
            )

    def test_undeclared_package_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            output = Path(temporary) / "output" / "conversation-visuals"
            (source / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")

            result = run_checker("--output", str(output), root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("package boundary contains undeclared file", result.stdout)

    def test_executable_package_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            readme = source / "README.md"
            os.chmod(readme, readme.stat().st_mode | 0o100)

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("package boundary contains executable file", result.stdout)

    def test_empty_forbidden_package_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            (source / "tests").mkdir()

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("package boundary contains forbidden path: tests", result.stdout)

    def test_symlinked_package_content_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = copy_conversation_visuals(temporary)
            readme = source / "README.md"
            readme.unlink()
            readme.symlink_to("LICENSE")

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("package boundary contains unsupported symlink", result.stdout)


if __name__ == "__main__":
    unittest.main()
