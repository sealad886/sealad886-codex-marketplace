from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "check_marketplace.py"
MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_marketplace import version_from_tag  # noqa: E402


def run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def write_marketplace(root: Path, marketplace: dict[str, object]) -> None:
    (root / MARKETPLACE_PATH).write_text(
        json.dumps(marketplace, indent=2) + "\n", encoding="utf-8"
    )


def commit_fixture(root: Path, message: str) -> None:
    run_git(root, "add", ".")
    run_git(
        root,
        "-c",
        "user.name=Marketplace Tests",
        "-c",
        "user.email=marketplace-tests@example.invalid",
        "commit",
        "-q",
        "-m",
        message,
    )


def create_repository_fixture(root: Path) -> dict[str, object]:
    (root / MARKETPLACE_PATH.parent).mkdir(parents=True)
    shutil.copy2(REPOSITORY_ROOT / "LICENSE", root / "LICENSE")
    marketplace = json.loads(
        (REPOSITORY_ROOT / MARKETPLACE_PATH).read_text(encoding="utf-8")
    )
    for entry in marketplace["plugins"]:
        source_path = Path(entry["source"]["path"])
        while source_path.parts and source_path.parts[0] == ".":
            source_path = Path(*source_path.parts[1:])
        shutil.copytree(REPOSITORY_ROOT / source_path, root / source_path)
        pinned_version = version_from_tag(entry["source"].get("ref"))
        if pinned_version is not None:
            manifest_path = source_path / ".codex-plugin" / "plugin.json"
            manifest = json.loads(
                (root / manifest_path).read_text(encoding="utf-8")
            )
            manifest["version"] = pinned_version
            (root / manifest_path).write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
    write_marketplace(root, marketplace)
    run_git(root, "init", "-q")
    commit_fixture(root, "fixture: add catalog plugins")
    for entry in marketplace["plugins"]:
        source_ref = entry["source"].get("ref")
        if source_ref is not None:
            run_git(root, "tag", source_ref)
    return marketplace


def add_example_plugin(root: Path, manifest_name: str = "example-plugin") -> None:
    shutil.copytree(
        REPOSITORY_ROOT / "plugins" / "project-delivery",
        root / "plugins" / "example-plugin",
    )
    manifest_path = (
        root / "plugins" / "example-plugin" / ".codex-plugin" / "plugin.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["name"] = manifest_name
    manifest["version"] = "0.1.0"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")


def example_entry(source_ref: str) -> dict[str, object]:
    return {
        "name": "example-plugin",
        "source": {
            "source": "git-subdir",
            "url": "https://github.com/sealad886/sealad886-codex-marketplace.git",
            "ref": source_ref,
            "path": "./plugins/example-plugin",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Developer Tools",
    }


class MarketplaceTests(unittest.TestCase):
    def test_conversation_visuals_uses_manifest_visible_local_source(self) -> None:
        marketplace = json.loads(
            (REPOSITORY_ROOT / MARKETPLACE_PATH).read_text(encoding="utf-8")
        )
        entry = next(
            item
            for item in marketplace["plugins"]
            if item["name"] == "conversation-visuals"
        )

        self.assertEqual(
            entry["source"],
            {
                "source": "local",
                "path": "./plugins/conversation-visuals",
            },
        )

    def test_repository_marketplace_and_license_parity_pass(self) -> None:
        result = run_checker(REPOSITORY_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("license_parity=true", result.stdout)

    def test_local_marketplace_entry_requires_complete_interface(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            entry = next(
                item
                for item in marketplace["plugins"]
                if item["name"] == "conversation-visuals"
            )
            manifest_path = (
                root
                / entry["source"]["path"]
                / ".codex-plugin"
                / "plugin.json"
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["interface"]["longDescription"] = ""
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "local manifest interface.longDescription must be non-empty",
                result.stdout,
            )

    def test_marketplace_path_escape_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            marketplace["plugins"][0]["source"]["path"] = "../../outside"
            write_marketplace(root, marketplace)

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("escapes the repository", result.stdout)

    def test_mutable_marketplace_ref_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            marketplace["plugins"][0]["source"]["ref"] = "main"
            write_marketplace(root, marketplace)

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must be an immutable version tag", result.stdout)

    def test_nonexistent_immutable_looking_ref_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            marketplace["plugins"][0]["source"]["ref"] = "v9.9.9"
            write_marketplace(root, marketplace)

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("does not resolve to an exact local tag or commit", result.stdout)

    def test_tag_version_must_match_pinned_manifest_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            marketplace["plugins"][0]["source"]["ref"] = "v9.9.9"
            write_marketplace(root, marketplace)
            run_git(root, "tag", "v9.9.9")

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source.ref version '9.9.9' must match", result.stdout)

    def test_wrong_marketplace_repository_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            marketplace["plugins"][0]["source"]["url"] = (
                "https://github.com/example/project-delivery.git"
            )
            write_marketplace(root, marketplace)

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source.url must be", result.stdout)

    def test_additional_well_formed_marketplace_entry_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            add_example_plugin(root)
            marketplace["plugins"].append(
                example_entry("example-plugin-v0.1.0")
            )
            write_marketplace(root, marketplace)
            commit_fixture(root, "fixture: add example plugin")
            run_git(root, "tag", "example-plugin-v0.1.0")

            result = run_checker(root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("plugins=3", result.stdout)

    def test_duplicate_marketplace_plugin_name_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            marketplace["plugins"].append(
                json.loads(json.dumps(marketplace["plugins"][0]))
            )
            write_marketplace(root, marketplace)

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("plugin names must be unique", result.stdout)

    def test_duplicate_marketplace_source_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            duplicate = json.loads(json.dumps(marketplace["plugins"][0]))
            duplicate["name"] = "second-plugin"
            marketplace["plugins"].append(duplicate)
            write_marketplace(root, marketplace)

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source paths must be unique", result.stdout)

    def test_pinned_ref_without_plugin_subtree_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            add_example_plugin(root)
            marketplace["plugins"].append(
                example_entry(str(marketplace["plugins"][0]["source"]["ref"]))
            )
            write_marketplace(root, marketplace)

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("pinned source", result.stdout)
            self.assertIn("is missing required path", result.stdout)

    def test_pinned_manifest_identity_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            marketplace = create_repository_fixture(root)
            add_example_plugin(root, manifest_name="wrong-plugin")
            marketplace["plugins"].append(
                example_entry("example-plugin-v0.1.0")
            )
            write_marketplace(root, marketplace)
            commit_fixture(root, "fixture: add mismatched example plugin")
            run_git(root, "tag", "example-plugin-v0.1.0")

            manifest_path = (
                root
                / "plugins"
                / "example-plugin"
                / ".codex-plugin"
                / "plugin.json"
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["name"] = "example-plugin"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("pinned manifest name must match", result.stdout)


if __name__ == "__main__":
    unittest.main()
