"""Claude discovery must preserve membership, metadata and portable runtime paths."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_copilot_marketplace import create_fixture, write_json
from test_validation import add_claude_manifest, run_checker as check_package


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/check_claude_marketplace.py"
CATALOG = Path(".claude-plugin/marketplace.json")


def run_checker(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(CHECKER), str(root), *arguments],
                          capture_output=True, text=True, timeout=30)


class ClaudeMarketplaceTests(unittest.TestCase):
    def test_repository_catalog_matches_every_eligible_package(self) -> None:
        result = run_checker(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        canonical = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        actual = json.loads((ROOT / CATALOG).read_text())
        self.assertEqual({entry["name"] for entry in actual["plugins"]},
                         {entry["name"] for entry in canonical["plugins"]} - {"worktree-activity"})

    def test_generate_check_and_reject_catalog_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_fixture(root)
            result = run_checker(root, "--write")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            catalog = json.loads((root / CATALOG).read_text())
            self.assertEqual(catalog["plugins"][0]["source"], "./plugins/example-plugin")
            self.assertEqual(run_checker(root).returncode, 0)
            catalog["plugins"][0]["version"] = "99.0.0"
            write_json(root / CATALOG, catalog)
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("out of date", result.stdout)

    def test_codex_only_membership_does_not_bypass_portable_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = create_fixture(root)
            manifest = json.loads((package / "plugin.json").read_text())
            manifest["extensions"]["com.sealad886.marketplace"] = {
                "clients": ["codex"], "reason": "Requires native Codex identity",
            }
            write_json(package / "plugin.json", manifest)
            (package / ".claude-plugin/plugin.json").unlink()
            result = run_checker(root, "--write")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads((root / CATALOG).read_text())["plugins"], [])
            self.assertEqual(check_package(package).returncode, 0)
            manifest["version"] = "99.0.0"
            write_json(package / "plugin.json", manifest)
            result = run_checker(root, "--write")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("portable manifest", result.stdout)

    def test_missing_malformed_and_unsynchronized_manifests_fail_without_writing(self) -> None:
        for change in (None, "{", "[]", {"version": "99.0.0"}, {"skills": "../outside"}):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                package = create_fixture(root)
                path = package / ".claude-plugin/plugin.json"
                if change is None:
                    path.unlink()
                elif isinstance(change, str):
                    path.write_text(change)
                else:
                    manifest = json.loads(path.read_text())
                    manifest.update(change)
                    write_json(path, manifest)
                result = run_checker(root, "--write")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Claude manifest", result.stdout)
                self.assertFalse((root / CATALOG).exists())
                self.assertNotEqual(check_package(package).returncode, 0)

    def test_explicit_client_policy_must_match_three_client_contract(self) -> None:
        for clients, accepted in ((["codex", "copilot", "claude"], True),
                                  (["codex", "copilot"], False), (["claude"], False)):
            with self.subTest(clients=clients), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                package = create_fixture(root)
                manifest = json.loads((package / "plugin.json").read_text())
                manifest["extensions"]["com.sealad886.marketplace"] = {
                    "clients": clients, "reason": "Explicit repository client scope",
                }
                write_json(package / "plugin.json", manifest)
                result = run_checker(root, "--write")
                self.assertEqual(result.returncode == 0, accepted, result.stdout + result.stderr)

    def test_inline_mcp_replaces_codex_relative_paths_and_rejects_runtime_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = create_fixture(root)
            path = package / ".codex-plugin/plugin.json"
            overlay = json.loads(path.read_text())
            overlay["mcpServers"] = "./.mcp.json"
            write_json(path, overlay)
            (package / "mcp").mkdir()
            (package / "mcp/server.py").write_text("print('ready')\n")
            write_json(package / ".mcp.json", {"mcpServers": {"example": {
                "command": "python3", "args": ["./mcp/server.py"],
                "cwd": ".", "tool_timeout_sec": 30, "env_vars": ["EXAMPLE_TOKEN"],
            }}})
            write_json(package / "mcp.json", {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {"example": {
                    "type": "stdio", "command": "python3", "cwd": "${PLUGIN_ROOT}",
                    "args": ["${PLUGIN_ROOT}/mcp/server.py"],
                }},
            })
            manifest = add_claude_manifest(package)
            result = run_checker(root, "--write")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            server = manifest["mcpServers"]["example"]
            self.assertEqual(server["args"], ["${CLAUDE_PLUGIN_ROOT}/mcp/server.py"])
            for change in ({"args": ["./mcp/server.py"]}, {"command": "node"},
                           {"tool_timeout_sec": 30}, {"args": ["${PLUGIN_ROOT}/mcp/server.py"]}):
                with self.subTest(change=change):
                    altered = json.loads(json.dumps(manifest))
                    altered["mcpServers"]["example"].update(change)
                    write_json(package / ".claude-plugin/plugin.json", altered)
                    result = run_checker(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Claude manifest", result.stdout)

    def test_generation_rejects_symlinked_catalog_and_package_metadata(self) -> None:
        for target in ("catalog-directory", "catalog-file", "manifest-file"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "repo"
                root.mkdir()
                package = create_fixture(root)
                outside = Path(temporary) / "outside"
                outside.mkdir()
                sentinel = outside / "sentinel.json"
                sentinel.write_text("{}")
                if target == "catalog-directory":
                    (root / ".claude-plugin").symlink_to(outside, target_is_directory=True)
                elif target == "catalog-file":
                    (root / ".claude-plugin").mkdir()
                    (root / CATALOG).symlink_to(sentinel)
                else:
                    path = package / ".claude-plugin/plugin.json"
                    path.unlink()
                    path.symlink_to(sentinel)
                result = run_checker(root, "--write")
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(sentinel.read_text(), "{}")
                self.assertFalse((outside / "marketplace.json").exists())


if __name__ == "__main__":
    unittest.main()
