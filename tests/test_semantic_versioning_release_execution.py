"""Run release validation and mutation-order scripts against disposable fixtures."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from test_semantic_versioning_publish_channels import run_block

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / 'plugins/semantic-versioning/templates/workflows'


class RustReleaseOrderTests(unittest.TestCase):
    def test_normalized_order_publishes_every_validated_member(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath('release-order.txt').write_text(' core \n\n api')
            packages = [{'id': 'core', 'name': 'core', 'version': '1.2.3', 'dependencies': []}, {'id': 'api', 'name': 'api', 'version': '1.2.3', 'dependencies': [{'name': 'core', 'path': '/fixture/core', 'kind': None}]}]
            temp = root / 'temp'
            temp.mkdir()
            (temp / 'cargo-metadata.json').write_text(json.dumps({'packages': packages, 'workspace_members': ['core', 'api']}))
            cargo = root / 'cargo'
            cargo.write_text('#!/bin/sh\nprintf "%s\\n" "$4" >> "$PUBLISHED"\n')
            cargo.chmod(0o755)
            env = dict(os.environ, RELEASE_VERSION='1.2.3', RUNNER_TEMP=str(temp), PUBLISHED=str(root / 'published'), PATH=str(root) + os.pathsep + os.environ['PATH'])
            check = run_block('Check fixed workspace versions and explicit publish order', WORKFLOWS / 'rust.yml.template')
            result = subprocess.run([sys.executable, '-c', check], cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            publish = run_block('Publish in dependency order', WORKFLOWS / 'rust.yml.template')
            result = subprocess.run(['bash', '-e', '-c', publish], cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((root / 'published').read_text().splitlines(), ['core', 'api'])
            root.joinpath('release-order.txt').write_text('api\ncore')
            result = subprocess.run([sys.executable, '-c', check], cwd=root, env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)


class GoDraftTests(unittest.TestCase):
    def fixture(self, draft=True, assets=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        def git(*args):
            return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True, text=True).stdout.strip()
        git('init', '-b', 'main')
        git('config', 'user.name', 'Fixture')
        git('config', 'user.email', 'fixture@example.invalid')
        git('commit', '--allow-empty', '-m', 'fixture')
        sha = git('rev-parse', 'HEAD')
        git('update-ref', 'refs/remotes/origin/main', sha)
        (root / 'response.json').write_text(json.dumps({'isDraft': draft, 'targetCommitish': sha, 'assets': assets or []}))
        gh = root / 'gh'
        gh.write_text('#!/bin/sh\nif [ "$1" = release ]; then cat "$RESPONSE"; else printf "%s\\n" "$RELEASE_SHA"; printf "%s\\n" mutation >> "$MUTATIONS"; fi\n')
        gh.chmod(0o755)
        env = dict(os.environ, RELEASE_SHA=sha, RELEASE_TAG='v1.2.3', RELEASE_VERSION='1.2.3', GITHUB_REPOSITORY='fixture/project', RUNNER_TEMP=str(root), RESPONSE=str(root / 'response.json'), MUTATIONS=str(root / 'mutations'), PATH=str(root) + os.pathsep + os.environ['PATH'])
        # GitHub's Ubuntu runner provides python. Bind it explicitly for hosts
        # that only provide python3, preserving the workflow's Python program.
        (root / 'python').symlink_to(sys.executable)
        return root, env, git

    def test_verified_empty_draft_materializes_exact_tag(self):
        root, env, git = self.fixture()
        script = run_block('Prepare verified draft and release tag', WORKFLOWS / 'go.yml.template')
        result = subprocess.run(['bash', '-e', '-c', script], cwd=root, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(git('rev-parse', 'refs/tags/v1.2.3'), env['RELEASE_SHA'])
        self.assertEqual((root / 'mutations').read_text().splitlines(), ['mutation'])

    def test_published_or_populated_release_blocks_before_tag_mutation(self):
        for draft, assets in [(False, []), (True, [{'name': 'partial.tar.gz'}])]:
            root, env, _ = self.fixture(draft, assets)
            script = run_block('Prepare verified draft and release tag', WORKFLOWS / 'go.yml.template')
            result = subprocess.run(['bash', '-e', '-c', script], cwd=root, env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / 'mutations').exists())

    def test_mismatched_existing_tag_blocks_source_verification(self):
        root, env, git = self.fixture()
        git('commit', '--allow-empty', '-m', 'different release')
        git('tag', 'v1.2.3')
        git('checkout', env['RELEASE_SHA'])
        prepare = run_block('Prepare verified draft and release tag', WORKFLOWS / 'go.yml.template')
        verify = run_block('Verify immutable release source', WORKFLOWS / 'go.yml.template')
        result = subprocess.run(['bash', '-e', '-c', prepare + '\n' + verify], cwd=root, env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((root / 'mutations').exists())

    def test_wrong_draft_target_blocks_before_tag_creation(self):
        root, env, _ = self.fixture()
        response = json.loads((root / 'response.json').read_text())
        response['targetCommitish'] = 'main'
        (root / 'response.json').write_text(json.dumps(response))
        script = run_block('Prepare verified draft and release tag', WORKFLOWS / 'go.yml.template')
        result = subprocess.run(['bash', '-e', '-c', script], cwd=root, env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((root / 'mutations').exists())


if __name__ == '__main__':
    unittest.main()
