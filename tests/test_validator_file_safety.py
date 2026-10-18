from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_distribution_bundle as distribution
import check_marketplace as marketplace
import check_plugin as plugin
import check_route_receipts as receipts
import check_routes as routes
import export_route_prompts as prompts
from tests.test_validation import create_minimal_plugin
from safe_files import MAX_CONTROL_BYTES, MAX_PAYLOAD_BYTES, read_bytes


class ValidatorFileSafetyTests(unittest.TestCase):
    def test_regular_plugin_accepts_universal_text_newlines(self) -> None:
        for newline in (b"\r\n", b"\r"):
            with self.subTest(newline=newline), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "project-delivery"
                create_minimal_plugin(root)
                skill = root / "skills" / "sample" / "SKILL.md"
                skill.write_bytes(skill.read_bytes().replace(b"\n", newline))
                errors, _, _ = plugin.validate(root, "source")
                self.assertEqual(errors, [])

    def test_linked_skill_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            skill = root / "skills" / "sample"
            outside = Path(temporary) / "outside"
            skill.rename(outside)
            skill.symlink_to(outside, target_is_directory=True)
            errors, _, _ = plugin.validate(root, "source")
            self.assertTrue(any("symlink" in error for error in errors), errors)

    def test_mandatory_control_files_reject_links_before_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin_root = root / "project-delivery"
            create_minimal_plugin(plugin_root)
            manifest = plugin_root / ".codex-plugin" / "plugin.json"
            manifest.rename(root / "external-manifest.json")
            manifest.symlink_to(root / "external-manifest.json")
            errors, _, _ = plugin.validate(plugin_root, "source")
            self.assertTrue(any("symlink" in error for error in errors), errors)
            with self.assertRaisesRegex(OSError, "symlink"):
                distribution.select_paths(plugin_root)

            (root / "tests").mkdir()
            contract = root / "tests" / "route-contracts.json"
            shutil.copyfile(ROOT / "tests" / "route-contracts.json", root / "outside.json")
            contract.symlink_to(root / "outside.json")
            with self.assertRaisesRegex(OSError, "symlink"):
                prompts.build_prompt_manifest(root)
            errors, _, _ = routes.validate(root)
            self.assertTrue(any("symlink" in error for error in errors), errors)

            (root / ".agents" / "plugins").mkdir(parents=True)
            catalog = root / ".agents" / "plugins" / "marketplace.json"
            catalog.symlink_to(ROOT / ".agents" / "plugins" / "marketplace.json")
            errors = marketplace.validate_repository_marketplace(root)
            self.assertTrue(any("symlink" in error for error in errors), errors)

    def test_reader_rejects_component_links_and_root_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "inside").mkdir()
            target = root / "inside" / "file.json"
            target.write_text("{}")
            (root / "alias").symlink_to(root / "inside", target_is_directory=True)
            with self.assertRaisesRegex(OSError, "symlink"):
                read_bytes(root / "alias" / "file.json", root=root)
            with self.assertRaisesRegex(OSError, "symlink"):
                read_bytes(root / "alias" / "file.json", root=root / "alias")
            with self.assertRaisesRegex(OSError, "escapes"):
                read_bytes(root.parent / "outside.json", root=root)
            self.assertEqual(read_bytes(target, root=root), b"{}")

    def test_fifo_is_rejected_without_waiting_for_writer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fifo = root / "route-contracts.json"
            os.mkfifo(fifo)
            code = (
                "from pathlib import Path; import sys; "
                "sys.path.insert(0, sys.argv[1]); "
                "from safe_files import read_bytes; "
                "read_bytes(Path(sys.argv[2]), root=Path(sys.argv[3]))"
            )
            result = subprocess.run(
                [sys.executable, "-c", code, str(ROOT / "scripts"), str(fifo), str(root)],
                capture_output=True, text=True, timeout=3,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("regular non-symlink file", result.stderr)

    def test_oversized_control_is_rejected_and_asset_budget_is_larger(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "tests").mkdir()
            control = root / "tests" / "route-contracts.json"
            with control.open("wb") as handle:
                handle.truncate(MAX_CONTROL_BYTES + 1)
            with self.assertRaisesRegex(OSError, "limit"):
                prompts.build_prompt_manifest(root)
            self.assertLess(MAX_CONTROL_BYTES, MAX_PAYLOAD_BYTES)
            self.assertEqual(len(read_bytes(control, root=root, max_bytes=MAX_PAYLOAD_BYTES)), MAX_CONTROL_BYTES + 1)
            control.write_bytes(b"1234")
            self.assertEqual(read_bytes(control, root=root, max_bytes=4), b"1234")
            with self.assertRaisesRegex(OSError, "limit"):
                read_bytes(control, root=root, max_bytes=3)

    def test_unknown_specialists_never_reach_filesystem_reads(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract = json.loads((ROOT / "tests" / "route-contracts.json").read_text())
            observation = json.loads((ROOT / "tests" / "fixtures" / "blind-route-observations-v1.3.1.json").read_text())
            observation["evidence_class"] = receipts.FRESH_EVIDENCE_CLASS
            outside = root / "outside"
            observation["loaded_specialists"] = [{
                "skill": str(outside), "relative_path": "invalid",
                "state": "loaded", "skill_sha256": "0" * 64,
                "evidence": ["synthetic"],
            }]
            original = receipts.safe_read_bytes

            def guarded_read(path, **kwargs):
                if path == outside / "SKILL.md":
                    self.fail("unknown specialist reached a filesystem read")
                return original(path, **kwargs)

            with patch.object(receipts, "safe_read_bytes", guarded_read):
                errors, _, _ = receipts.validate(
                    ROOT, root / "unused.json", True, False, True,
                    ROOT / "plugins" / "project-delivery", "e8fac87", contract, observation,
                )
            self.assertTrue(any("specialist is unknown" in error for error in errors), errors)

    def test_rejected_installed_link_is_never_reopened_for_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            installed = Path(temporary) / "project-delivery"
            shutil.copytree(ROOT / "plugins" / "project-delivery", installed)
            manifest = installed / ".codex-plugin" / "plugin.json"
            target = Path(temporary) / "manifest.json"
            manifest.rename(target)
            manifest.symlink_to(target)
            contract = json.loads((ROOT / "tests" / "route-contracts.json").read_text())
            observation = json.loads((ROOT / "tests" / "fixtures" / "blind-route-observations-v1.3.1.json").read_text())
            observation["evidence_class"] = receipts.FRESH_EVIDENCE_CLASS
            observation["schema_version"] = 2
            original = Path.open

            def guarded_open(path, *args, **kwargs):
                if path == manifest:
                    self.fail("rejected installed manifest reopened")
                return original(path, *args, **kwargs)

            with patch.object(Path, "open", guarded_open):
                errors, _, _ = receipts.validate(
                    ROOT, Path(temporary) / "unused.json", True, False, True,
                    installed, "e8fac87", contract, observation,
                )
            self.assertTrue(any("symlink" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
