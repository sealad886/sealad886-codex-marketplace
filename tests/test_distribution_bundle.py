from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path, PureWindowsPath


REPOSITORY_ROOT = Path(__file__).parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "project-delivery"
CONVERSATION_VISUALS_ROOT = REPOSITORY_ROOT / "plugins" / "conversation-visuals"
CHECKER = REPOSITORY_ROOT / "scripts" / "check_distribution_bundle.py"
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_distribution_bundle import (  # noqa: E402
    add_python_module_dependencies,
    is_absolute_path,
    materialize_runtime_closure,
    python_launch_operand,
)


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
SUBPROCESS_TIMEOUT_SECONDS = 30


def run_checker(*arguments: str, root: Path = PLUGIN_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root), *arguments],
        check=False,
        capture_output=True,
        text=True,
        timeout=SUBPROCESS_TIMEOUT_SECONDS,
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

    def test_invalid_manifest_name_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            manifest_path = source / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["name"] = "bad/name"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("plugin name must be lower-case hyphen-case", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_overlong_manifest_name_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            manifest_path = source / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["name"] = "a" * 240
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must not exceed 64 characters", result.stdout)
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

    def test_non_object_mcp_config_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text("[]", encoding="utf-8")

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("local MCP config must contain an object", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_non_object_mcp_server_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps({"mcpServers": {"conversation-visuals": []}}),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("server config must contain an object", result.stdout)

    def test_absolute_local_mcp_dependency_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["/tmp/server.py"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not portable", result.stdout)

    def test_windows_absolute_local_mcp_dependency_returns_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": [r"C:\Users\alice\server.py"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("absolute local MCP dependency is not portable", result.stdout)

    def test_posix_absolute_paths_are_recognized_independently_of_host(self) -> None:
        with (
            mock.patch.object(Path, "is_absolute", return_value=False),
            mock.patch.object(PureWindowsPath, "is_absolute", return_value=False),
        ):
            self.assertTrue(is_absolute_path("/etc/passwd"))

    def test_absolute_local_mcp_command_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "/home/alice/server",
                                "args": [],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("absolute local MCP command is not portable", result.stdout)

    def test_unresolved_bare_local_mcp_command_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp").rmdir()
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "definitely-missing-server",
                                "args": [],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "unresolved bare local MCP command is not portable",
                result.stdout,
            )

    def test_bare_local_mcp_command_does_not_resolve_from_server_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            coincident_command = source / "server"
            coincident_command.write_text("#!/bin/sh\n", encoding="utf-8")
            os.chmod(
                coincident_command,
                coincident_command.stat().st_mode | 0o100,
            )
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "server",
                                "args": [],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "unresolved bare local MCP command is not portable",
                result.stdout,
            )

    def test_relative_local_mcp_command_is_included(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "launcher.py").write_text(
                "#!/usr/bin/env python3\n",
                encoding="utf-8",
            )
            launcher = source / "mcp" / "launcher.py"
            os.chmod(launcher, launcher.stat().st_mode | 0o100)
            (source / "mcp" / "server.py").unlink()
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "./mcp/launcher.py",
                                "args": [],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)
            os.chmod(launcher, launcher.stat().st_mode & ~0o111)
            nonexecutable = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(nonexecutable.returncode, 0)
            self.assertIn(
                "local MCP command is not executable",
                nonexecutable.stdout,
            )

    def test_local_mcp_dependency_resolves_from_server_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["./server.py"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_inline_local_mcp_dependency_is_included(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
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
            (source / ".mcp.json").unlink()

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_remote_mcp_server_has_no_local_dependency(self) -> None:
        for inline in (False, True):
            with (
                self.subTest(inline=inline),
                tempfile.TemporaryDirectory() as temporary,
            ):
                source = Path(temporary) / "conversation-visuals"
                shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
                remote_servers = {
                    "conversation-visuals": {
                        "type": "http",
                        "url": "https://example.com/mcp",
                    }
                }
                (source / "mcp" / "server.py").unlink()
                (source / "mcp").rmdir()
                if inline:
                    manifest_path = source / ".codex-plugin" / "plugin.json"
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    manifest["mcpServers"] = remote_servers
                    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                    (source / ".mcp.json").unlink()
                else:
                    (source / ".mcp.json").write_text(
                        json.dumps({"mcpServers": remote_servers}),
                        encoding="utf-8",
                    )

                result = run_checker(root=source)

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_remote_mcp_url_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "type": "http",
                                "url": "not a url",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("remote MCP server url is invalid", result.stdout)

    def test_remote_mcp_url_with_authority_whitespace_is_rejected(self) -> None:
        for url in ("https://exa mple.com/mcp", "https://example.\tcom/mcp"):
            with (
                self.subTest(url=url),
                tempfile.TemporaryDirectory() as temporary,
            ):
                source = Path(temporary) / "conversation-visuals"
                shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
                (source / ".mcp.json").write_text(
                    json.dumps(
                        {
                            "mcpServers": {
                                "conversation-visuals": {
                                    "type": "http",
                                    "url": url,
                                }
                            }
                        }
                    ),
                    encoding="utf-8",
                )

                result = run_checker(root=source)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("remote MCP server url is invalid", result.stdout)

    def test_remote_mcp_url_with_encoded_hostname_is_rejected(self) -> None:
        for url in (
            "https://exa%20mple.com/mcp",
            "https://%31%32%37.0.0.1/mcp",
            "https://exa％20mple.com/mcp",
            "https://exa^mple.com/mcp",
            "https://exa|mple.com/mcp",
            "https://exa<mple.com/mcp",
            "https://exa>mple.com/mcp",
            "https://256.1.1.1/mcp",
            "https://1.2.3.4.5/mcp",
            "https://[v1.foo]/mcp",
        ):
            with (
                self.subTest(url=url),
                tempfile.TemporaryDirectory() as temporary,
            ):
                source = Path(temporary) / "conversation-visuals"
                shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
                (source / ".mcp.json").write_text(
                    json.dumps(
                        {
                            "mcpServers": {
                                "conversation-visuals": {
                                    "type": "http",
                                    "url": url,
                                }
                            }
                        }
                    ),
                    encoding="utf-8",
                )

                result = run_checker(root=source)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("remote MCP server url is invalid", result.stdout)

    def test_python_module_launch_dependency_is_included(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["-m", "mcp.server"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_grouped_python_options_identify_the_launch_operand(self) -> None:
        launches = (
            (["-Bm", "mcp.server"], ("module", "mcp.server")),
            (["-Bmmcp.server"], ("module", "mcp.server")),
            (["-Xdev", "-Wignore", "server"], ("script", "server")),
            (["-B", "-X", "dev", "-m", "mcp.server"], ("module", "mcp.server")),
        )

        for arguments, expected in launches:
            with self.subTest(arguments=arguments):
                self.assertEqual(
                    python_launch_operand("python3", arguments),
                    expected,
                )

    def test_python_exit_only_options_cannot_serve_an_mcp(self) -> None:
        exit_only_options = (
            "-?",
            "-V",
            "-VV",
            "-h",
            "--help",
            "--help-all",
            "--help-env",
            "--help-xoptions",
            "--version",
        )

        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"

            for option in exit_only_options:
                with self.subTest(option=option):
                    config_path.write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "python3",
                                        "args": [option, "./mcp/server.py"],
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "exit-only option cannot serve an MCP server",
                        result.stdout,
                    )

    def test_python_hash_pyc_policy_must_match_runtime_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"

            for arguments, expected_success in (
                (["--check-hash-based-pycs", "always", "./mcp/server.py"], True),
                (["--check-hash-based-pycs", "default", "./mcp/server.py"], True),
                (["--check-hash-based-pycs", "never", "./mcp/server.py"], True),
                (["--check-hash-based-pycs", "bogus", "./mcp/server.py"], False),
                (["--check-hash-based-pycs=default", "./mcp/server.py"], False),
            ):
                with self.subTest(arguments=arguments):
                    config_path.write_text(
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

                    if expected_success:
                        self.assertEqual(
                            result.returncode,
                            0,
                            result.stdout + result.stderr,
                        )
                    else:
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn(
                            "local Python --check-hash-based-pycs",
                            result.stdout,
                        )

    def test_python_startup_options_must_be_explicitly_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"

            for option in ("--definitely-invalid", "-J"):
                with self.subTest(option=option):
                    config_path.write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "python3",
                                        "args": [option, "./mcp/server.py"],
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "unsupported local Python startup option",
                        result.stdout,
                    )

    def test_python_safe_path_options_cannot_launch_bundled_modules(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"

            for arguments in (
                ["-P", "-m", "mcp.server"],
                ["-I", "-m", "mcp.server"],
                ["-IPm", "mcp.server"],
            ):
                with self.subTest(arguments=arguments):
                    config_path.write_text(
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
                    self.assertIn(
                        "safe-path option cannot launch a bundled module",
                        result.stdout,
                    )

    def test_python_xoptions_must_match_runtime_contract(self) -> None:
        valid_values = (
            "utf8",
            "utf8=0",
            "utf8=1",
            "cpu_count=1",
            "cpu_count=default",
            "context_aware_warnings=0",
            "context_aware_warnings=1",
            "frozen_modules=on",
            "frozen_modules=off",
            "int_max_str_digits=0",
            "int_max_str_digits=640",
            "thread_inherit_context=0",
            "thread_inherit_context=1",
            "tracemalloc",
            "tracemalloc=0",
            "tracemalloc=1",
            "importtime",
            "importtime=1",
            "importtime=2",
            "custom_runtime_option=enabled",
        )
        invalid_values = (
            "utf8=bogus",
            "cpu_count=0",
            "cpu_count=bogus",
            "context_aware_warnings=bogus",
            "frozen_modules=bogus",
            "int_max_str_digits=639",
            "int_max_str_digits=bogus",
            "thread_inherit_context=bogus",
            "tracemalloc=bogus",
            "importtime=3",
        )

        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"

            for attached in (False, True):
                for value in (*valid_values, *invalid_values):
                    with self.subTest(attached=attached, value=value):
                        option = f"-X{value}" if attached else "-X"
                        arguments = (
                            [option, "./mcp/server.py"]
                            if attached
                            else [option, value, "./mcp/server.py"]
                        )
                        config_path.write_text(
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

                        if value in valid_values:
                            self.assertEqual(
                                result.returncode,
                                0,
                                result.stdout + result.stderr,
                            )
                        else:
                            self.assertNotEqual(result.returncode, 0)
                            self.assertIn(
                                "local Python -X option value is invalid",
                                result.stdout,
                            )

    def test_node_exit_only_options_cannot_serve_an_mcp(self) -> None:
        exit_only_options = (
            "-h",
            "-v",
            "--completion-bash",
            "--help",
            "--v8-options",
            "--version",
        )

        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"

            for option in exit_only_options:
                with self.subTest(option=option):
                    config_path.write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "node",
                                        "args": [option, "./mcp/server.py"],
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "exit-only option cannot serve an MCP server",
                        result.stdout,
                    )

    def test_node_debugger_wait_options_cannot_serve_an_mcp(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"

            for option in (
                "--inspect-brk",
                "--inspect-brk=127.0.0.1:9229",
                "--inspect-wait",
                "--inspect-wait=127.0.0.1:9229",
            ):
                with self.subTest(option=option):
                    config_path.write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "node",
                                        "args": [option, "./mcp/server.py"],
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "debugger-wait option cannot serve an MCP server",
                        result.stdout,
                    )

    def test_node_replacement_modes_cannot_serve_an_mcp(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"

            for option in (
                "--build-snapshot",
                "--build-snapshot-config=./snapshot.json",
                "--experimental-sea-config=./sea.json",
                "--prof-process",
                "--test",
            ):
                with self.subTest(option=option):
                    config_path.write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "node",
                                        "args": [option, "./mcp/server.py"],
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "replacement mode cannot serve an MCP server",
                        result.stdout,
                    )

    def test_node_package_script_command_must_be_executable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            launcher = source / "mcp" / "server"
            launcher.write_text("#!/bin/sh\n", encoding="utf-8")
            (source / "mcp" / "package.json").write_text(
                json.dumps({"scripts": {"mcp": "./server"}}),
                encoding="utf-8",
            )
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["--run=mcp"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            nonexecutable = run_checker(root=source)
            os.chmod(launcher, launcher.stat().st_mode | 0o100)
            executable = run_checker(root=source)

            self.assertNotEqual(nonexecutable.returncode, 0)
            self.assertIn(
                "local Node package script command is not executable",
                nonexecutable.stdout,
            )
            self.assertEqual(
                executable.returncode,
                0,
                executable.stdout + executable.stderr,
            )

    def test_grouped_python_module_launch_dependency_is_included(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["-Bm", "mcp.server"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unresolved_python_module_launch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"

            for module, expected_error in (
                ("definitely_missing_module", "cannot be resolved"),
                ("not-a-module", "name is invalid"),
            ):
                with self.subTest(module=module):
                    config_path.write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "python3",
                                        "args": ["-m", module],
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        f"local Python module {expected_error}",
                        result.stdout,
                    )

    def test_python_package_launch_requires_main_module(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp").rmdir()
            package = source / "package_server"
            package.mkdir()
            (package / "__init__.py").write_text("", encoding="utf-8")
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["-m", "package_server"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            missing_entrypoint = run_checker(root=source)
            (package / "__main__.py").write_text(
                "print('ready')\n",
                encoding="utf-8",
            )
            included_entrypoint = run_checker(root=source)

            self.assertNotEqual(missing_entrypoint.returncode, 0)
            self.assertIn(
                "local Python package launch requires __main__.py",
                missing_entrypoint.stdout,
            )
            self.assertEqual(
                included_entrypoint.returncode,
                0,
                included_entrypoint.stdout + included_entrypoint.stderr,
            )

    def test_python_application_arguments_do_not_select_modules(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            module = root / "application" / "package.py"
            module.parent.mkdir()
            module.write_text("", encoding="utf-8")
            selected: set[Path] = set()

            add_python_module_dependencies(
                root,
                root,
                selected,
                "python3",
                ["runner", "-m", "application.package"],
            )

            self.assertEqual(selected, set())

    def test_nested_python_package_launch_includes_parent_initializer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp").rmdir()
            package = source / "pkg"
            subpackage = package / "subpkg"
            subpackage.mkdir(parents=True)
            (package / "__init__.py").write_text("", encoding="utf-8")
            (subpackage / "__init__.py").write_text("", encoding="utf-8")
            (subpackage / "__main__.py").write_text("", encoding="utf-8")
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["-m", "pkg.subpkg"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_python_script_operand_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp").rmdir()
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["server.py"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("local MCP dependency does not exist", result.stdout)

    def test_python_directory_launch_requires_main_module(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["./mcp"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            missing_entrypoint = run_checker(root=source)
            (source / "mcp" / "__main__.py").write_text(
                "print('ready')\n",
                encoding="utf-8",
            )
            included_entrypoint = run_checker(root=source)

            self.assertNotEqual(missing_entrypoint.returncode, 0)
            self.assertIn(
                "local Python directory launch requires __main__.py",
                missing_entrypoint.stdout,
            )
            self.assertEqual(
                included_entrypoint.returncode,
                0,
                included_entrypoint.stdout + included_entrypoint.stderr,
            )

    def test_missing_python_command_or_module_operand_returns_an_error(self) -> None:
        for launch_option in ("-c", "-m"):
            with (
                self.subTest(launch_option=launch_option),
                tempfile.TemporaryDirectory() as temporary,
            ):
                source = Path(temporary) / "conversation-visuals"
                shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
                (source / "mcp" / "server.py").unlink()
                (source / "mcp").rmdir()
                (source / ".mcp.json").write_text(
                    json.dumps(
                        {
                            "mcpServers": {
                                "conversation-visuals": {
                                    "command": "python3",
                                    "args": [launch_option],
                                }
                            }
                        }
                    ),
                    encoding="utf-8",
                )

                result = run_checker(root=source)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    f"local Python {launch_option} launch requires an operand",
                    result.stdout,
                )

    def test_missing_node_script_operand_returns_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp").rmdir()
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["server.js"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("local MCP dependency does not exist", result.stdout)

    def test_node_eval_launch_does_not_require_a_script(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp").rmdir()
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["--eval", "console.log('ready')"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_node_eval_launch_rejects_unbounded_module_loading(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": [
                                    "--eval",
                                    "require('./mcp/definitely-missing.js')",
                                ],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "local Node inline program dependencies cannot be established",
                result.stdout,
            )

    def test_python_command_launch_rejects_unbounded_imports(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["-c", "import definitely_missing_module"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "local Python inline program dependencies cannot be established",
                result.stdout,
            )

    def test_node_debug_port_options_consume_separate_operands(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp" / "server.js").write_text(
                "console.log('ready');\n",
                encoding="utf-8",
            )
            (source / "mcp" / "bootstrap.js").write_text(
                "globalThis.ready = true;\n",
                encoding="utf-8",
            )
            config_path = source / ".mcp.json"

            for option in ("--debug-port", "--inspect-port"):
                with self.subTest(option=option):
                    config_path.write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "node",
                                        "args": [
                                            option,
                                            "9333",
                                            "--require",
                                            "./mcp/bootstrap",
                                            "./mcp/server.js",
                                        ],
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertEqual(
                        result.returncode,
                        0,
                        result.stdout + result.stderr,
                    )

            config_path.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": [
                                    "--debug-port=99999",
                                    "./mcp/server.js",
                                ],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            invalid_port = run_checker(root=source)

            self.assertNotEqual(invalid_port.returncode, 0)
            self.assertIn(
                "local Node --debug-port value is invalid",
                invalid_port.stdout,
            )

    def test_node_input_type_supports_inline_eval_launches(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp").rmdir()
            config_path = source / ".mcp.json"

            for arguments in (
                ["--input-type=module", "--eval", "console.log('ready')"],
                ["--input-type", "module", "--eval", "console.log('ready')"],
                ["--input-type=commonjs", "-e", "console.log('ready')"],
            ):
                with self.subTest(arguments=arguments):
                    config_path.write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "node",
                                        "args": arguments,
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertEqual(
                        result.returncode,
                        0,
                        result.stdout + result.stderr,
                    )

    def test_node_startup_options_must_be_explicitly_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            config_path = source / ".mcp.json"
            config = {
                "mcpServers": {
                    "conversation-visuals": {
                        "command": "node",
                        "args": ["--no-warnings", "./mcp/server.py"],
                    }
                }
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")

            supported = run_checker(root=source)
            config["mcpServers"]["conversation-visuals"]["args"][0] = (
                "--definitely-invalid"
            )
            config_path.write_text(json.dumps(config), encoding="utf-8")
            unsupported = run_checker(root=source)

            self.assertEqual(
                supported.returncode,
                0,
                supported.stdout + supported.stderr,
            )
            self.assertNotEqual(unsupported.returncode, 0)
            self.assertIn(
                "unsupported local Node startup option",
                unsupported.stdout,
            )

    def test_node_syntax_check_cannot_serve_as_an_mcp_launch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            server = source / "mcp" / "server.js"
            server.write_text("console.log('checked');\n", encoding="utf-8")
            for check_option in ("-c", "--check"):
                with self.subTest(check_option=check_option):
                    (source / ".mcp.json").write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "node",
                                        "args": [
                                            check_option,
                                            "./mcp/server.js",
                                        ],
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "local Node syntax-check mode cannot serve an MCP server",
                        result.stdout,
                    )

    def test_node_package_script_launch_includes_bundled_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            server = source / "mcp" / "server.js"
            package = source / "mcp" / "package.json"
            server.write_text("console.log('ready');\n", encoding="utf-8")
            package.write_text(
                json.dumps(
                    {
                        "scripts": {
                            "mcp": "node ./server.js",
                        }
                    }
                ),
                encoding="utf-8",
            )
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["--run=mcp"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            included = run_checker(root=source)
            server.unlink()
            missing = run_checker(root=source)

            self.assertEqual(
                included.returncode,
                0,
                included.stdout + included.stderr,
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("local MCP dependency does not exist", missing.stdout)

    def test_node_package_script_cannot_redirect_the_mcp_transport(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            package_path = source / "package.json"
            package_path.write_text(
                json.dumps(
                    {
                        "scripts": {
                            "mcp": "python3 ./mcp/server.py > mcp.log",
                        }
                    }
                ),
                encoding="utf-8",
            )
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["--run=mcp"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "local Node package script contains unsupported shell control",
                result.stdout,
            )

    def test_nested_node_package_script_launch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "package.json").write_text(
                json.dumps(
                    {
                        "scripts": {
                            "mcp": "node --run=serve",
                            "serve": "node ./missing.js",
                        }
                    }
                ),
                encoding="utf-8",
            )
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["--run=mcp"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "nested local Node package-script launches are unsupported",
                result.stdout,
            )

    def test_interpreter_launch_cannot_consume_mcp_transport_as_source(self) -> None:
        invalid_launches = (
            ("python3", []),
            ("python3", ["-"]),
            ("node", []),
            ("node", ["-"]),
        )
        for command, arguments in invalid_launches:
            with (
                self.subTest(command=command, arguments=arguments),
                tempfile.TemporaryDirectory() as temporary,
            ):
                source = Path(temporary) / "conversation-visuals"
                shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
                (source / ".mcp.json").write_text(
                    json.dumps(
                        {
                            "mcpServers": {
                                "conversation-visuals": {
                                    "command": command,
                                    "args": arguments,
                                }
                            }
                        }
                    ),
                    encoding="utf-8",
                )

                result = run_checker(root=source)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("MCP launch requires", result.stdout)

    def test_attached_node_preload_dependency_is_included(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            server = source / "mcp" / "server.js"
            preload = source / "mcp" / "bootstrap.js"
            server.write_text("console.log('ready');\n", encoding="utf-8")
            preload.write_text("globalThis.ready = true;\n", encoding="utf-8")
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["--require=./bootstrap.js", "server.js"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_extensionless_commonjs_preload_dependency_is_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            server = source / "mcp" / "server.js"
            preload = source / "mcp" / "bootstrap.js"
            server.write_text("console.log('ready');\n", encoding="utf-8")
            preload.write_text("globalThis.ready = true;\n", encoding="utf-8")
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["--require", "./bootstrap", "server.js"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_commonjs_preload_directory_requires_an_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            server = source / "mcp" / "server.js"
            preload = source / "mcp" / "bootstrap"
            server.write_text("console.log('ready');\n", encoding="utf-8")
            preload.mkdir()
            (preload / "notes.txt").write_text("not executable\n", encoding="utf-8")
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["--require", "./bootstrap", "server.js"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            unresolved = run_checker(root=source)
            (preload / "index.js").write_text(
                "globalThis.ready = true;\n",
                encoding="utf-8",
            )
            resolved = run_checker(root=source)
            (preload / "index.js").unlink()
            (preload / "package.json").write_text(
                json.dumps({"main": "entry"}),
                encoding="utf-8",
            )
            (preload / "entry.js").write_text(
                "globalThis.ready = true;\n",
                encoding="utf-8",
            )
            package_resolved = run_checker(root=source)

            self.assertNotEqual(unresolved.returncode, 0)
            self.assertIn(
                "local Node CommonJS preload directory has no entrypoint",
                unresolved.stdout,
            )
            self.assertEqual(
                resolved.returncode,
                0,
                resolved.stdout + resolved.stderr,
            )
            self.assertEqual(
                package_resolved.returncode,
                0,
                package_resolved.stdout + package_resolved.stderr,
            )

    def test_esm_preload_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp" / "server.js").write_text(
                "console.log('ready');\n",
                encoding="utf-8",
            )
            preload = source / "mcp" / "bootstrap"
            preload.mkdir()
            (preload / "index.js").write_text(
                "globalThis.ready = true;\n",
                encoding="utf-8",
            )
            config_path = source / ".mcp.json"

            for option in ("--import", "--loader"):
                with self.subTest(option=option):
                    config_path.write_text(
                        json.dumps(
                            {
                                "mcpServers": {
                                    "conversation-visuals": {
                                        "command": "node",
                                        "args": [
                                            option,
                                            "./mcp/bootstrap",
                                            "./mcp/server.js",
                                        ],
                                    }
                                }
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_checker(root=source)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "local Node ESM preload cannot be a directory",
                        result.stdout,
                    )

    def test_node_env_file_cannot_hide_startup_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp" / "server.js").write_text(
                "console.log('ready');\n",
                encoding="utf-8",
            )
            environment = source / "mcp" / "config.env"
            environment.write_text(
                'NODE_OPTIONS="--require ./definitely-missing.js"\n',
                encoding="utf-8",
            )
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": [
                                    "--env-file",
                                    "./mcp/config.env",
                                    "./mcp/server.js",
                                ],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            hidden_dependency = run_checker(root=source)
            environment.write_text("VISUALS=enabled\n", encoding="utf-8")
            bounded_environment = run_checker(root=source)

            self.assertNotEqual(hidden_dependency.returncode, 0)
            self.assertIn(
                "local Node env file NODE_OPTIONS cannot establish closure",
                hidden_dependency.stdout,
            )
            self.assertEqual(
                bounded_environment.returncode,
                0,
                bounded_environment.stdout + bounded_environment.stderr,
            )

    def test_node_declaration_env_cannot_hide_startup_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp" / "server.js").write_text(
                "console.log('ready');\n",
                encoding="utf-8",
            )
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["./mcp/server.js"],
                                "env": {
                                    "NODE_OPTIONS": (
                                        "--require ./definitely-missing.js"
                                    )
                                },
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "local Node MCP env NODE_OPTIONS cannot establish closure",
                result.stdout,
            )

    def test_node_env_file_operand_must_be_a_regular_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            (source / "mcp" / "server.js").write_text(
                "console.log('ready');\n",
                encoding="utf-8",
            )
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": [
                                    "--env-file",
                                    "./mcp",
                                    "./mcp/server.js",
                                ],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "local Node env-file dependency must be a regular file",
                result.stdout,
            )

    def test_bare_node_preload_must_be_a_known_builtin_module(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            server = source / "mcp" / "server.js"
            server.write_text("console.log('ready');\n", encoding="utf-8")
            config_path = source / ".mcp.json"
            config = {
                "mcpServers": {
                    "conversation-visuals": {
                        "command": "node",
                        "args": ["--require", "fs", "./mcp/server.js"],
                    }
                }
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")

            builtin = run_checker(root=source)
            config["mcpServers"]["conversation-visuals"]["args"][1] = (
                "definitely-missing-preload"
            )
            config_path.write_text(json.dumps(config), encoding="utf-8")
            unresolved = run_checker(root=source)
            coincident_directory = source / "definitely-missing-preload"
            coincident_directory.mkdir()
            (coincident_directory / "index.js").write_text(
                "globalThis.ready = true;\n",
                encoding="utf-8",
            )
            coincident = run_checker(root=source)

            self.assertEqual(
                builtin.returncode,
                0,
                builtin.stdout + builtin.stderr,
            )
            self.assertNotEqual(unresolved.returncode, 0)
            self.assertIn(
                "local Node preload module cannot be resolved",
                unresolved.stdout,
            )
            self.assertNotEqual(coincident.returncode, 0)
            self.assertIn(
                "local Node preload module cannot be resolved",
                coincident.stdout,
            )

    def test_attached_node_env_file_is_included_and_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            server = source / "mcp" / "server.js"
            environment = source / "mcp" / "config.env"
            server.write_text("console.log('ready');\n", encoding="utf-8")
            environment.write_text("VISUALS=enabled\n", encoding="utf-8")
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": ["--env-file=./config.env", "server.js"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            included = run_checker(root=source)
            environment.unlink()
            missing = run_checker(root=source)
            mcp_config_path = source / ".mcp.json"
            mcp_config = json.loads(mcp_config_path.read_text(encoding="utf-8"))
            mcp_config["mcpServers"]["conversation-visuals"]["args"][0] = (
                "--env-file=config.env"
            )
            mcp_config_path.write_text(json.dumps(mcp_config), encoding="utf-8")
            bare_missing = run_checker(root=source)
            mcp_config["mcpServers"]["conversation-visuals"]["args"][0] = (
                "--env-file-if-exists=./config.env"
            )
            mcp_config_path.write_text(json.dumps(mcp_config), encoding="utf-8")
            optional_missing = run_checker(root=source)

            self.assertEqual(
                included.returncode,
                0,
                included.stdout + included.stderr,
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("local MCP dependency does not exist", missing.stdout)
            self.assertNotEqual(bare_missing.returncode, 0)
            self.assertIn(
                "local Node runtime dependency cannot be resolved",
                bare_missing.stdout,
            )
            self.assertEqual(
                optional_missing.returncode,
                0,
                optional_missing.stdout + optional_missing.stderr,
            )

    def test_attached_node_snapshot_blob_is_included_and_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / "mcp" / "server.py").unlink()
            server = source / "mcp" / "server.js"
            snapshot = source / "mcp" / "server.blob"
            server.write_text("console.log('ready');\n", encoding="utf-8")
            snapshot.write_bytes(b"node snapshot placeholder")
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "node",
                                "args": [
                                    "--snapshot-blob=./mcp/server.blob",
                                    "./mcp/server.js",
                                ],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            included = run_checker(root=source)
            snapshot.unlink()
            missing = run_checker(root=source)

            self.assertEqual(
                included.returncode,
                0,
                included.stdout + included.stderr,
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("local MCP dependency does not exist", missing.stdout)

    def test_extensionless_python_script_operand_is_included(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            server = source / "mcp" / "server"
            (source / "mcp" / "server.py").rename(server)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["server"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_directory_mcp_dependency_is_included(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            resources = source / "mcp" / "resources"
            resources.mkdir()
            (resources / "prompt.txt").write_text("visual prompt\n", encoding="utf-8")
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["server.py", "resources"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_scripts_component_is_allowed_outside_project_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            scripts = source / "scripts"
            scripts.mkdir()
            (scripts / "render.js").write_text("export {};\n", encoding="utf-8")
            manifest_path = source / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["scripts"] = "./scripts/"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unprefixed_local_mcp_dependency_resolves_from_server_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["server.py"],
                                "cwd": "mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_local_mcp_dependency_cannot_escape_plugin_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "conversation-visuals"
            shutil.copytree(CONVERSATION_VISUALS_ROOT, source)
            (source / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "conversation-visuals": {
                                "command": "python3",
                                "args": ["../../outside.py"],
                                "cwd": "./mcp",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_checker(root=source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("local MCP dependency escapes plugin root", result.stdout)

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

    def test_replace_non_object_manifest_is_refused_without_a_traceback(self) -> None:
        for manifest in ([], None):
            with (
                self.subTest(manifest=manifest),
                tempfile.TemporaryDirectory() as temporary,
            ):
                output = Path(temporary) / "project-delivery"
                (output / ".codex-plugin").mkdir(parents=True)
                (output / ".codex-plugin" / "plugin.json").write_text(
                    json.dumps(manifest),
                    encoding="utf-8",
                )

                result = run_checker("--output", str(output), "--replace")

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "refusing to replace output with invalid identity",
                    result.stdout,
                )
                self.assertNotIn("Traceback", result.stderr)

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
