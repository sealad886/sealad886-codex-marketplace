from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "check_plugin.py"


def create_minimal_plugin(root: Path, name: str = "project-delivery", version: str = "1.3.0") -> None:
    (root / ".codex-plugin").mkdir(parents=True)
    (root / "skills" / "sample").mkdir(parents=True)
    manifest = {
        "name": name,
        "version": version,
        "description": "Test plugin",
        "author": {"name": "Test Author"},
        "interface": {
            "displayName": "Test Plugin",
            "shortDescription": "Test plugin structure",
        },
    }
    (root / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    (root / "skills" / "sample" / "SKILL.md").write_text(
        "---\n"
        "name: sample\n"
        "description: A sample skill used by validator tests.\n"
        "---\n\n"
        "# Sample\n\n"
        "## When to invoke\n\nFor validation.\n\n"
        "## Inputs and evidence\n\nA fixture.\n\n"
        "## Workflow\n\nValidate it.\n\n"
        "## Outputs and handoff\n\nA result.\n\n"
        "## Completion evidence\n\nThe result.\n\n"
        "## Must not\n\nInvent evidence.\n",
        encoding="utf-8",
    )
    for relative in (".codexignore", "LICENSE", "README.md", "SECURITY.md"):
        (root / relative).write_text(f"fixture: {relative}\n", encoding="utf-8")


def run_checker(root: Path, layout: str = "auto") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root), "--layout", layout],
        check=False,
        capture_output=True,
        text=True,
    )


def add_portable_manifest(root: Path) -> dict:
    overlay = json.loads((root / ".codex-plugin/plugin.json").read_text())
    portable = {key: value for key, value in overlay.items() if key != "interface"}
    portable["$schema"] = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    portable["extensions"] = {"com.openai": {"interface": overlay["interface"]}}
    (root / "plugin.json").write_text(json.dumps(portable), encoding="utf-8")
    return portable


class PluginCheckerTests(unittest.TestCase):
    def test_matching_portable_manifest_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "example-plugin"
            create_minimal_plugin(root, name="example-plugin")
            add_portable_manifest(root)
            result = run_checker(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_portable_identity_and_presentation_drift_fail(self) -> None:
        for field, value in (("name", "other"), ("version", "9.0.0"),
                             ("description", "Different purpose"),
                             ("extensions", {"com.openai": {"interface": {}}})):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "example-plugin"
                create_minimal_plugin(root, name="example-plugin")
                portable = add_portable_manifest(root)
                portable[field] = value
                (root / "plugin.json").write_text(json.dumps(portable))
                result = run_checker(root)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("portable manifest", result.stdout)

    def test_invalid_portable_manifest_fails(self) -> None:
        for content in ("{", "[]", '{"$schema": "wrong"}'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "example-plugin"
                create_minimal_plugin(root, name="example-plugin")
                (root / "plugin.json").write_text(content)
                result = run_checker(root)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("portable manifest", result.stdout)

    def test_portable_cannot_use_legacy_component_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "example-plugin"
            create_minimal_plugin(root, name="example-plugin")
            portable = add_portable_manifest(root)
            portable["skills"] = "./skills/"
            (root / "plugin.json").write_text(json.dumps(portable))
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("portable manifest", result.stdout)

    def test_portable_schema_types_and_unknown_fields_are_rejected(self) -> None:
        changes = ({"unknown": 1}, {"description": []}, {"author": "Someone"},
                   {"author": {"name": 7}}, {"author": {"unknown": "field"}},
                   {"keywords": [2]}, {"extensions": {"example.org": []}})
        for change in changes:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "example-plugin"
                create_minimal_plugin(root, name="example-plugin")
                overlay_path = root / ".codex-plugin/plugin.json"
                overlay = json.loads(overlay_path.read_text())
                overlay.update(change)
                overlay_path.write_text(json.dumps(overlay))
                portable = add_portable_manifest(root)
                portable.update(change)
                (root / "plugin.json").write_text(json.dumps(portable))
                result = run_checker(root)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("portable manifest", result.stdout)

    def test_portable_artwork_must_be_contained_regular_file(self) -> None:
        for target in ("../outside.svg", "./missing.svg", "./linked.svg"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "example-plugin"
                create_minimal_plugin(root, name="example-plugin")
                outside = Path(temporary) / "outside.svg"
                outside.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
                if target == "./linked.svg":
                    (root / "linked.svg").symlink_to(outside)
                overlay_path = root / ".codex-plugin/plugin.json"
                overlay = json.loads(overlay_path.read_text())
                overlay["interface"]["logo"] = target
                overlay_path.write_text(json.dumps(overlay))
                add_portable_manifest(root)
                result = run_checker(root)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("portable manifest", result.stdout)

    def test_source_layout_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            result = run_checker(root, "source")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_versioned_cache_layout_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery" / "1.3.0+codex.test"
            create_minimal_plugin(root, version="1.3.0+codex.test")
            result = run_checker(root, "cache")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_wrong_source_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "wrong-name"
            create_minimal_plugin(root)
            result = run_checker(root, "source")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("plugin path must be", result.stdout)

    def test_malformed_manifest_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            (root / ".codex-plugin").mkdir(parents=True)
            (root / ".codex-plugin" / "plugin.json").write_text("{", encoding="utf-8")
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid manifest", result.stdout)

    def test_missing_skills_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            skill = root / "skills" / "sample" / "SKILL.md"
            skill.unlink()
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no skills found", result.stdout)

    def test_incomplete_skill_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            skill = root / "skills" / "sample" / "SKILL.md"
            skill.write_text(
                skill.read_text(encoding="utf-8").replace(
                    "## Completion evidence", "## Completion proof"
                ),
                encoding="utf-8",
            )
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing skill contract section", result.stdout)

    def test_missing_required_release_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            (root / ".codexignore").unlink()
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required release file", result.stdout)

    def test_public_fixture_absolute_home_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            fixtures = root / "tests" / "fixtures"
            fixtures.mkdir(parents=True)
            (fixtures / "receipt.json").write_text(
                '{"cache": "/Users/example/.codex/cache"}', encoding="utf-8"
            )
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("absolute user-home path", result.stdout)

    def test_public_fixture_raw_task_identifier_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            fixtures = root / "tests" / "fixtures"
            fixtures.mkdir(parents=True)
            (fixtures / "receipt.json").write_text(
                '{"task": "019f7a5c-0d65-7053-a4db-fa66e20e289c"}',
                encoding="utf-8",
            )
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("raw task identifier", result.stdout)


if __name__ == "__main__":
    unittest.main()
