"""Distribution, disclosure, and inactive workflow security contracts."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/semantic-versioning'
sys.path.insert(0, str(ROOT / 'scripts'))
from check_distribution_bundle import select_paths
from check_semantic_versioning import validate
from check_marketplace import validate_entry

class PackageTests(unittest.TestCase):
    def test_package_closure_contains_runtime_references_and_examples(self):
        selected = select_paths(PLUGIN)
        for folder in ('scripts', 'references', 'examples', 'templates'):
            for path in (PLUGIN / folder).rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts:
                    self.assertIn(path.relative_to(PLUGIN), selected)

    def test_disclosure_and_example_validation(self):
        errors, counts = validate(PLUGIN)
        self.assertFalse(errors, errors)
        self.assertEqual(len(counts), 3)

    def test_mutable_actions_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / 'bad.yml.template').write_text('steps:\n  - uses: actions/checkout@main\n')
            self.assertTrue(validate(root)[0])

    def test_unavailable_entry_still_checks_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            plugin = root / 'plugins/semantic-versioning'
            shutil.copytree(PLUGIN, plugin, ignore=shutil.ignore_patterns('__pycache__'))
            entry = {'name': 'semantic-versioning', 'source': {'source': 'local', 'path': './plugins/semantic-versioning'}, 'policy': {'installation': 'NOT_AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Developer Tools'}
            self.assertFalse(validate_entry(root, entry, 0, set(), set()))
            manifest = plugin / '.codex-plugin/plugin.json'
            data = json.loads(manifest.read_text())
            data['name'] = 'wrong-name'
            manifest.write_text(json.dumps(data))
            self.assertTrue(validate_entry(root, entry, 0, set(), set()))

    def test_invalid_install_policy_is_rejected(self):
        entry = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())['plugins'][-1]
        entry['policy']['installation'] = 'AUTOMATIC'
        errors = validate_entry(ROOT, entry, 0, set(), set())
        self.assertTrue(any('policy.installation' in e for e in errors))

if __name__ == '__main__':
    unittest.main()
