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
from check_copilot_marketplace import validate_portable_mcp  # noqa: E402
from test_validation import add_portable_manifest, create_minimal_plugin


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
    def test_local_translation_runtime_and_configuration_ship_together(self) -> None:
        # Installed tools must retain their imported modules and setup examples.
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source/local-translation"
            create_minimal_plugin(source, name="local-translation")
            overlay_path = source / ".codex-plugin/plugin.json"
            overlay = json.loads(overlay_path.read_text())
            overlay.update({"skills": "./skills/", "mcpServers": "./.mcp.json"})
            overlay_path.write_text(json.dumps(overlay))
            portable = add_portable_manifest(source)
            portable.pop("skills")
            portable.pop("mcpServers")
            (source / "plugin.json").write_text(json.dumps(portable))
            (source / "mcp").mkdir()
            (source / "mcp/helper.py").write_text("READY = True\n")
            (source / "mcp/server.py").write_text("from helper import READY\nassert READY\n")
            (source / "examples").mkdir()
            (source / "examples/config.json").write_text('{"model":"local-index"}\n')
            (source / "assets").mkdir()
            (source / "assets/banner.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"/>'
            )
            (source / ".mcp.json").write_text(json.dumps({"mcpServers": {
                "local-translation": {"command": "python3", "cwd": ".",
                                      "args": ["./mcp/server.py"],
                                      "env_vars": ["EXAMPLE_TOKEN", "_private_name"]},
            }}))
            (source / "mcp.json").write_text(json.dumps({
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {"local-translation": {"type": "stdio",
                    "command": "python3", "cwd": "${PLUGIN_ROOT}",
                    "args": ["${PLUGIN_ROOT}/mcp/server.py"]}},
            }))
            output = Path(temporary) / "dist/local-translation"
            result = run_checker("--output", str(output), root=source)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(validate_portable_mcp(output, overlay), [])
            for relative in ("mcp/helper.py", "mcp/server.py", "examples/config.json", "assets/banner.svg",
                             "plugin.json", "mcp.json", ".mcp.json"):
                self.assertEqual((source / relative).read_bytes(),
                                 (output / relative).read_bytes())
            launch = subprocess.run([sys.executable, "-B", str(output / "mcp/server.py")],
                                    cwd=temporary, capture_output=True, text=True,
                                    timeout=SUBPROCESS_TIMEOUT_SECONDS)
            self.assertEqual(launch.returncode, 0, launch.stderr)

    def test_malformed_mcp_environment_allowlists_are_rejected(self) -> None:
        for names in (None, {}, "TOKEN", ["TOKEN", "TOKEN"], [None], [1],
                      ["KEY=value"], ["bad-name"], ["1BAD"], [""]):
            with self.subTest(names=names), tempfile.TemporaryDirectory() as temporary:
                source = copy_conversation_visuals(temporary)
                write_mcp_server(source, {"command": "python3", "cwd": ".",
                    "args": ["./mcp/server.py"], "env_vars": names})
                result = run_checker(root=source)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("env_vars must contain unique environment variable names",
                              result.stdout + result.stderr)

    def test_camofox_node_bundle_retains_setup_helpers_and_portable_config(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source/camofox-mcp"
            create_minimal_plugin(source, name="camofox-mcp")
            manifest_path = source / ".codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text())
            manifest.update({"skills": "./skills/", "mcpServers": "./.mcp.json"})
            manifest_path.write_text(json.dumps(manifest))
            portable = add_portable_manifest(source)
            portable.pop("skills")
            portable.pop("mcpServers")
            (source / "plugin.json").write_text(json.dumps(portable))
            (source / "scripts").mkdir()
            (source / "scripts/runtime-paths.mjs").write_text(
                "export const ready = 'packaged helper ready';\n"
            )
            for name in ("launch.mjs", "setup.mjs"):
                (source / "scripts" / name).write_text(
                    "import { ready } from './runtime-paths.mjs';\n"
                    "console.log(ready);\n"
                )
            write_mcp_server(source, {
                "command": "node", "args": ["./scripts/launch.mjs"], "cwd": ".",
            })
            (source / "mcp.json").write_text(json.dumps({
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {"camofox": {
                    "type": "stdio", "command": "node",
                    "args": ["${PLUGIN_ROOT}/scripts/launch.mjs"],
                    "cwd": "${PLUGIN_ROOT}",
                }},
            }))
            (source / "assets").mkdir()
            (source / "assets/banner.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"/>'
            )
            (source / "README.md").write_text("![Banner](assets/banner.svg)\n")
            output = Path(temporary) / "dist/camofox-mcp"

            result = run_checker("--output", str(output), root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for relative in ("scripts/launch.mjs", "scripts/setup.mjs",
                             "scripts/runtime-paths.mjs", "mcp.json", "assets/banner.svg"):
                self.assertEqual((source / relative).read_bytes(),
                                 (output / relative).read_bytes())
            node = shutil.which("node")
            if node is not None:
                for name in ("launch.mjs", "setup.mjs"):
                    launched = subprocess.run(
                        [node, str(output / "scripts" / name)], cwd=temporary,
                        capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_SECONDS,
                    )
                    self.assertEqual(launched.returncode, 0, launched.stderr)
                    self.assertEqual(launched.stdout.strip(), "packaged helper ready")

    def test_portable_manifest_survives_distribution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source/example-plugin"
            create_minimal_plugin(source, name="example-plugin")
            overlay_path = source / ".codex-plugin/plugin.json"
            overlay = json.loads(overlay_path.read_text())
            overlay["skills"] = "./skills/"
            overlay_path.write_text(json.dumps(overlay))
            portable = add_portable_manifest(source)
            portable.pop("skills")
            (source / "plugin.json").write_text(json.dumps(portable))
            portable_mcp = {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {},
            }
            (source / "mcp.json").write_text(json.dumps(portable_mcp))
            output = Path(temporary) / "dist/example-plugin"
            result = run_checker("--output", str(output), root=source)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((source / "plugin.json").read_bytes(),
                             (output / "plugin.json").read_bytes())
            self.assertTrue((output / "skills/sample/SKILL.md").is_file())
            self.assertEqual(json.loads((output / "mcp.json").read_text()), portable_mcp)

    def test_single_skill_plugin_rejects_an_extra_skill(self) -> None:
        for name in ("conventional-commit", "repository-guidance"):
            with self.subTest(plugin=name), tempfile.TemporaryDirectory() as temporary:
                source = Path(temporary) / name
                create_minimal_plugin(source, name=name)
                overlay_path = source / ".codex-plugin/plugin.json"
                overlay = json.loads(overlay_path.read_text())
                overlay["skills"] = "./skills/"
                overlay_path.write_text(json.dumps(overlay))
                shutil.copytree(source / "skills/sample", source / "skills/extra")
                result = run_checker(root=source)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("must contain 1 skills", result.stdout)

    def test_dark_artwork_is_included_in_distribution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source/example-plugin"
            create_minimal_plugin(source, name="example-plugin")
            overlay_path = source / ".codex-plugin/plugin.json"
            overlay = json.loads(overlay_path.read_text())
            overlay["skills"] = "./skills/"
            overlay["interface"]["logoDark"] = "./dark.svg"
            overlay["interface"]["composerIconDark"] = "./dark-composer.svg"
            overlay_path.write_text(json.dumps(overlay))
            for name in ("dark.svg", "dark-composer.svg"):
                (source / name).write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
            portable = add_portable_manifest(source)
            portable.pop("skills")
            (source / "plugin.json").write_text(json.dumps(portable))
            output = Path(temporary) / "dist/example-plugin"
            result = run_checker("--output", str(output), root=source)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name in ("dark.svg", "dark-composer.svg"):
                self.assertEqual((source / name).read_bytes(), (output / name).read_bytes())

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

    def test_icloud_materialized_bundle_launches_and_serves_setup(self) -> None:
        # The installed runtime must resolve every setup dependency without the
        # source checkout, and serve its packaged page without credential access.
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "icloud-mail"
            source = Path(temporary) / "source" / "icloud-mail"
            shutil.copytree(
                REPOSITORY_ROOT / "plugins" / "icloud-mail", source,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            result = run_checker("--output", str(output), root=source)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            check = subprocess.run(
                [sys.executable, "-E", "-B", str(output / "mcp" / "server.py"),
                 "--self-test"],
                cwd=temporary, capture_output=True, text=True,
                timeout=SUBPROCESS_TIMEOUT_SECONDS,
            )
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            probe = """
import http.client
import sys
import threading
sys.path.insert(0, sys.argv[1])
import server
import setup
import keychain
with setup.SetupServer(server, None, lifetime=5) as endpoint:
    worker = threading.Thread(target=endpoint.handle_request)
    worker.start()
    client = http.client.HTTPConnection("127.0.0.1", endpoint.server_port, timeout=5)
    client.request("GET", endpoint.path)
    response = client.getresponse()
    assert response.status == 200, response.status
    assert response.getheader("Content-Type").startswith("text/html")
    assert response.read(), "packaged setup page is empty"
    client.close()
    worker.join(timeout=5)
    assert not worker.is_alive()
"""
            check = subprocess.run(
                [sys.executable, "-I", "-B", "-c", probe, str(output / "mcp")],
                cwd=temporary, capture_output=True, text=True,
                timeout=SUBPROCESS_TIMEOUT_SECONDS,
            )
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

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

    def test_node_mcp_requires_a_contained_mjs_script(self) -> None:
        invalid_scripts = (
            ("/tmp/launch.mjs", "unsafe manifest path"),
            (r"C:\Users\alice\launch.mjs", "unsafe manifest path"),
            ("../outside.mjs", "unsafe manifest path"),
            ("./mcp/server.py", "must launch a .mjs script"),
        )
        for script, message in invalid_scripts:
            with self.subTest(script=script), tempfile.TemporaryDirectory() as temporary:
                source = copy_conversation_visuals(temporary)
                write_mcp_server(source, {
                    "command": "node", "args": [script], "cwd": ".",
                })
                result = run_checker(root=source)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stdout)

    def test_unsupported_mcp_launch_modes_are_rejected(self) -> None:
        launchers = (
            (
                {"command": "node", "args": ["./mcp/server.py"], "cwd": "."},
                "must launch a .mjs script",
            ),
            (
                {"command": "ruby", "args": ["./mcp/server.py"], "cwd": "."},
                "command must be python3 or node",
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
