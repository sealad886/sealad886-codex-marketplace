from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "project-delivery"
CONVERSATION_VISUALS_ROOT = REPOSITORY_ROOT / "plugins" / "conversation-visuals"
CHECKER = REPOSITORY_ROOT / "scripts" / "check_distribution_bundle.py"
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_distribution_bundle import materialize_runtime_closure  # noqa: E402


FORBIDDEN_PARTS = {
    ".git",
    ".github",
    ".venv",
    "__pycache__",
    "node_modules",
    "references",
    "scripts",
    "tests",
}


def run_checker(*arguments: str, root: Path = PLUGIN_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


class DistributionBundleTests(unittest.TestCase):
    def test_malformed_manifest_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".codex-plugin" / "plugin.json").write_text(
                "{",
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("cannot resolve plugin identity", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_non_array_mcp_args_returns_a_validation_error(self) -> None:
        invalid_values = (
            (None, "local MCP server args must be an array"),
            (
                ["./mcp/server.py", 1],
                "local MCP server args must contain only strings",
            ),
        )
        for arguments, expected_error in invalid_values:
            with (
                self.subTest(arguments=arguments),
                tempfile.TemporaryDirectory() as temporary,
            ):
                source = Path(temporary) / "conversation-visuals"
                shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
                (source / ".mcp.json").write_text(
                    json.dumps(
                        {
                            "mcpServers": {
                                "conversation-visuals": {
                                    "command": "python3",
                                    "args": arguments,
                                }
                            }
                        }
                    ),
                    encoding="utf-8",
                )

                result = run_checker(root=source)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_error, result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_materialized_distribution_is_exact_and_source_free(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "project-delivery"
            result = run_checker("--output", str(output))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("action=materialized", result.stdout)

            files = [path for path in output.rglob("*") if path.is_file()]
            self.assertEqual(len(files), 64)
            for path in files:
                self.assertFalse(
                    FORBIDDEN_PARTS.intersection(path.relative_to(output).parts),
                    path,
                )

    def test_replace_clean_distribution_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "project-delivery"
            first = run_checker("--output", str(output))
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            second = run_checker("--output", str(output), "--replace")
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)

    def test_replace_source_checkout_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "project-delivery"
            (output / ".codex-plugin").mkdir(parents=True)
            (output / ".git").mkdir()
            (output / ".codex-plugin" / "plugin.json").write_text(
                json.dumps({"name": "project-delivery"}),
                encoding="utf-8",
            )
            result = run_checker("--output", str(output), "--replace")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source checkout or Python environment", result.stdout)

    def test_replace_distribution_with_extra_file_is_refused_and_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "project-delivery"
            first = run_checker("--output", str(output))
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            extra = output / "user-notes.txt"
            extra.write_text("preserve me\n", encoding="utf-8")

            result = run_checker("--output", str(output), "--replace")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unclean output", result.stdout)
            self.assertEqual(extra.read_text(encoding="utf-8"), "preserve me\n")

    def test_replace_distribution_with_nested_environment_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "project-delivery"
            first = run_checker("--output", str(output))
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            nested_environment = output / "local" / ".venv"
            nested_environment.mkdir(parents=True)

            result = run_checker("--output", str(output), "--replace")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("forbidden path", result.stdout)
            self.assertTrue(nested_environment.is_dir())

    def test_replace_distribution_inside_git_ancestor_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkout = Path(temporary) / "checkout"
            (checkout / ".git").mkdir(parents=True)
            output = checkout / "prepared" / "project-delivery"
            shutil.copytree(PLUGIN_ROOT, output)

            result = run_checker("--output", str(output), "--replace")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source checkout or Python environment", result.stdout)
            self.assertTrue((output / ".codex-plugin" / "plugin.json").is_file())

    def test_output_symlink_is_refused_without_touching_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            real_output = Path(temporary) / "real-project-delivery"
            shutil.copytree(PLUGIN_ROOT, real_output)
            output = Path(temporary) / "project-delivery"
            output.symlink_to(real_output, target_is_directory=True)

            result = run_checker("--output", str(output), "--replace")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output symlink", result.stdout)
            self.assertTrue(output.is_symlink())
            self.assertTrue((real_output / ".codex-plugin" / "plugin.json").is_file())

    def test_failed_swap_restores_prior_clean_distribution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "project-delivery"
            first = run_checker("--output", str(output))
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
                    PLUGIN_ROOT,
                    output,
                    replace=True,
                )

            self.assertTrue(errors)
            self.assertIn("prior output was preserved", errors[0])
            self.assertEqual((output / "README.md").read_bytes(), prior_readme)
            self.assertFalse(
                list(output.parent.glob(".project-delivery-previous-*")),
                "a successful rollback must not leave a hidden backup",
            )

    def test_undeclared_package_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source" / "project-delivery"
            output = Path(temporary) / "output" / "project-delivery"
            shutil.copytree(PLUGIN_ROOT, source)
            (source / ".github").mkdir()
            (source / ".github" / "unexpected.yml").write_text("unexpected: true\n")
            result = run_checker("--output", str(output), root=source)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("package boundary contains undeclared file", result.stdout)

    def test_executable_package_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source" / "project-delivery"
            output = Path(temporary) / "output" / "project-delivery"
            shutil.copytree(PLUGIN_ROOT, source)
            readme = source / "README.md"
            os.chmod(readme, readme.stat().st_mode | 0o100)
            result = run_checker("--output", str(output), root=source)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("package boundary contains executable file", result.stdout)

    def test_empty_forbidden_package_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source" / "project-delivery"
            output = Path(temporary) / "output" / "project-delivery"
            shutil.copytree(PLUGIN_ROOT, source)
            (source / "tests").mkdir()

            result = run_checker("--output", str(output), root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("package boundary contains forbidden path: tests", result.stdout)

    def test_empty_undeclared_package_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source" / "project-delivery"
            output = Path(temporary) / "output" / "project-delivery"
            shutil.copytree(PLUGIN_ROOT, source)
            (source / "scratch").mkdir()

            result = run_checker("--output", str(output), root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("package boundary contains undeclared directory: scratch", result.stdout)

    def test_symlinked_package_content_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source" / "project-delivery"
            output = Path(temporary) / "output" / "project-delivery"
            shutil.copytree(PLUGIN_ROOT, source)
            readme = source / "README.md"
            readme.unlink()
            readme.symlink_to("LICENSE")

            result = run_checker("--output", str(output), root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("package boundary contains unsupported symlink", result.stdout)


if __name__ == "__main__":
    unittest.main()
