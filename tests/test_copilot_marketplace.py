"""Copilot discovery must resolve the same packages and retain their components."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_validation import add_portable_manifest, create_minimal_plugin


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/check_copilot_marketplace.py"
CATALOG = Path(".github/plugin/marketplace.json")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def run_checker(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root), *arguments],
        capture_output=True, text=True, timeout=30,
    )


def create_fixture(root: Path) -> Path:
    package = root / "plugins/example-plugin"
    create_minimal_plugin(package, name="example-plugin")
    add_portable_manifest(package)
    write_json(root / ".agents/plugins/marketplace.json", {
        "name": "sealad886-codex-marketplace",
        "plugins": [{"name": "example-plugin", "source": {
            "source": "local", "path": "./plugins/example-plugin",
        }}],
    })
    return package


class CopilotMarketplaceTests(unittest.TestCase):
    def test_repository_catalog_and_all_plugins_are_discoverable(self) -> None:
        result = run_checker(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_generate_then_check_and_detect_catalog_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_fixture(root)
            result = run_checker(root, "--write")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            result = run_checker(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            catalog = json.loads((root / CATALOG).read_text())
            self.assertEqual(catalog["plugins"][0]["source"], "./plugins/example-plugin")
            for field, value in (("version", "99.0.0"), ("source", "../outside")):
                with self.subTest(field=field):
                    altered = json.loads(json.dumps(catalog))
                    altered["plugins"][0][field] = value
                    write_json(root / CATALOG, altered)
                    result = run_checker(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("out of date", result.stdout)

    def test_missing_and_invalid_portable_manifests_fail(self) -> None:
        for content in (None, "[]", "{", '{"name":"other"}'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                package = create_fixture(root)
                self.assertEqual(run_checker(root, "--write").returncode, 0)
                manifest = package / "plugin.json"
                if content is None:
                    manifest.unlink()
                else:
                    manifest.write_text(content)
                result = run_checker(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("portable manifest", result.stdout)

    def test_unsafe_and_mismatched_canonical_sources_fail_without_writing(self) -> None:
        for source in ("../outside", "/tmp/outside", "plugins/missing"):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                create_fixture(root)
                path = root / ".agents/plugins/marketplace.json"
                catalog = json.loads(path.read_text())
                catalog["plugins"][0]["source"]["path"] = source
                write_json(path, catalog)
                result = run_checker(root, "--write")
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((root / CATALOG).exists())

    def test_portable_mcp_required_and_checked_against_codex_server(self) -> None:
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
                "cwd": ".", "tool_timeout_sec": 30,
            }}})
            result = run_checker(root, "--write")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("mcp.json", result.stdout)
            portable = {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {"example": {
                    "type": "stdio", "command": "python3",
                    "args": ["${PLUGIN_ROOT}/mcp/server.py"], "cwd": "${PLUGIN_ROOT}",
                }},
            }
            write_json(package / "mcp.json", portable)
            result = run_checker(root, "--write")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            portable["mcpServers"]["example"]["args"] = ["./missing.py"]
            write_json(package / "mcp.json", portable)
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("mcp.json", result.stdout)

    def test_generation_rejects_symlinked_catalog_ancestors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            create_fixture(root)
            outside = Path(temporary) / "outside"
            outside.mkdir()
            (root / ".github").symlink_to(outside, target_is_directory=True)
            result = run_checker(root, "--write")
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse((outside / "plugin/marketplace.json").exists())


if __name__ == "__main__":
    unittest.main()
