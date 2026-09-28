import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'plugins/semantic-versioning/scripts'


def run(script, *args):
    result = subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args), '--json'], text=True, capture_output=True)
    return result.returncode, json.loads(result.stdout)


class VersionTests(unittest.TestCase):
    def test_strict_versions(self):
        for invalid in ('v1.2.3', '01.2.3', '1.2', '1.2.3-01', '1.2.3-', '1.2.3+é', '1.2.3\n'):
            with self.subTest(invalid=invalid):
                self.assertEqual(run('check_version.py', 'validate', invalid)[0], 2)
        self.assertEqual(run('check_version.py', 'validate', '1.2.3-alpha.1+001')[0], 0)

    def test_semver_precedence(self):
        ordered = ['1.0.0-alpha', '1.0.0-alpha.1', '1.0.0-alpha.beta', '1.0.0-beta', '1.0.0-beta.2', '1.0.0-beta.11', '1.0.0-rc.1', '1.0.0']
        for left, right in zip(ordered, ordered[1:]):
            self.assertEqual(run('check_version.py', 'compare', left, right)[1]['precedence'], -1)
        self.assertEqual(run('check_version.py', 'compare', '1.2.3+abc', '1.2.3+def')[1]['precedence'], 0)

    def test_cumulative_target_is_idempotent(self):
        for impact, target in [('none', '1.2.3'), ('patch', '1.2.4'), ('minor', '1.3.0'), ('major', '2.0.0')]:
            first = run('check_version.py', 'check', '1.2.3', target, '--impact', impact)
            self.assertEqual(first[0], 0)
            self.assertEqual(first, run('check_version.py', 'check', '1.2.3', target, '--impact', impact))
        self.assertEqual(run('check_version.py', 'check', '1.2.3', '1.2.5', '--impact', 'patch')[0], 1)

    def test_pre1_and_prerelease_promotion(self):
        self.assertEqual(run('check_version.py', 'check', '0.2.3', '0.3.0', '--impact', 'major')[0], 0)
        self.assertEqual(run('check_version.py', 'check', '0.2.3', '1.0.0', '--impact', 'major', '--pre1-policy', 'semver')[0], 0)
        self.assertEqual(run('check_version.py', 'check', '1.2.3', '1.3.0-rc.1', '--impact', 'minor')[0], 0)
        self.assertEqual(run('check_version.py', 'check', '1.3.0-rc.1', '1.3.0', '--impact', 'minor')[0], 0)
        self.assertEqual(run('check_version.py', 'check', '1.3.0-rc.2', '1.3.0-rc.1', '--impact', 'minor')[0], 1)


class InspectionTests(unittest.TestCase):
    def setUp(self):
        # Synthetic repositories must not inherit machine-specific LFS filters.
        config = patch.dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
        config.start()
        self.addCleanup(config.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True, text=True).stdout

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-m', 'fixture')

    def test_scope_inheritance_dynamic_owner_and_dirty_preservation(self):
        self.write('package.json', '{"private":true,"workspaces":["packages/*"]}')
        self.write('packages/a/pyproject.toml', '[project]\nname="a"\ndynamic=["version"]\n')
        self.write('packages/b/package.json', '{"name":"b","version":"9.0.0"}')
        self.write('release-please-config.json', '{}')
        self.write('.changeset/config.json', '{}')
        self.commit()
        self.git('tag', 'a-v0.1.0')
        self.write('packages/a/private.txt', 'leave me alone')
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        code, data = run('inspect_repository.py', self.root, '--scope', 'packages/a')
        self.assertEqual(code, 0)
        self.assertEqual({m['path'] for m in data['manifests']}, {'package.json', 'packages/a/pyproject.toml'})
        self.assertEqual(data['owner_candidates'], ['changesets', 'release-please'])
        self.assertTrue(data['manifests'][1]['unresolved'])
        self.assertIn('packages/a/private.txt', data['git']['status'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_baselines_follow_ancestry_not_highest_version(self):
        self.write('package.json', '{"version":"1.0.0"}')
        self.commit()
        self.git('tag', 'pkg-v1.0.0')
        self.git('checkout', '-b', 'other')
        self.write('package.json', '{"version":"9.0.0"}')
        self.commit()
        self.git('tag', 'pkg-v9.0.0')
        self.git('checkout', 'main')
        data = run('inspect_repository.py', self.root)[1]
        self.assertEqual([x['tag'] for x in data['git']['baseline_candidates']], ['pkg-v1.0.0'])
        self.assertFalse(data['git']['baseline_candidates'][0]['selected'])

    def test_malformed_dynamic_and_initial_state(self):
        self.write('package.json', '{')
        self.write('build.gradle', 'throw new RuntimeException("MUST NOT RUN")')
        data = run('inspect_repository.py', self.root)[1]
        self.assertTrue(all(m['unresolved'] for m in data['manifests']))
        self.assertIsNone(data['git']['head'])
        self.assertEqual(run('inspect_repository.py', self.root, '--scope', '..')[0], 2)

    def test_symlinks_do_not_leak_outside_scope(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside)
            (external / 'package.json').write_text('{"version":"7.8.9"}')
            (self.root / 'linked').symlink_to(external, target_is_directory=True)
            (self.root / 'package.json').symlink_to(external / 'package.json')
            data = run('inspect_repository.py', self.root)[1]
            self.assertEqual(data['manifests'], [])

    def test_does_not_execute_configured_fsmonitor(self):
        self.write('package.json', '{"version":"1.0.0"}')
        self.commit()
        marker = self.root / 'executed'
        hook = self.root / 'monitor.sh'
        hook.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\n')
        hook.chmod(0o755)
        self.git('config', 'core.fsmonitor', str(hook))
        self.assertEqual(run('inspect_repository.py', self.root)[0], 0)
        self.assertFalse(marker.exists())

    def test_configured_filters_leave_status_unresolved_without_execution(self):
        self.write('package.json', '{"version":"1.0.0"}')
        self.write('.gitattributes', 'package.json filter=demo\n')
        self.commit()
        marker = self.root / 'executed'
        hook = self.root / 'filter.sh'
        hook.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\ncat\n')
        hook.chmod(0o755)
        self.write('package.json', '{"version":"2.0.0"}')
        for kind in ('clean', 'process'):
            with self.subTest(kind=kind):
                self.git('config', 'filter.demo.' + kind, str(hook))
                self.git('config', 'filter.demo.required', 'true')
                before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
                code, data = run('inspect_repository.py', self.root)
                self.assertEqual(code, 0)
                self.assertFalse(marker.exists())
                self.assertIsNone(data['git']['status'])
                self.assertTrue(any('filter' in issue for issue in data['unresolved']))
                self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
                self.git('config', '--unset', 'filter.demo.' + kind)

    def test_status_does_not_enter_submodule_worktrees(self):
        nested = self.root / 'nested'
        nested.mkdir()
        subprocess.run(['git', '-C', str(nested), 'init', '-b', 'main'], check=True, capture_output=True)
        def nested_git(*args):
            return subprocess.run(['git', '-C', str(nested), *args], check=True, capture_output=True)
        nested_git('config', 'user.name', 'Fixture')
        nested_git('config', 'user.email', 'fixture@example.invalid')
        self.write('nested/package.json', '{"version":"1.0.0"}')
        self.write('nested/.gitattributes', 'package.json filter=demo\n')
        nested_git('add', '.')
        nested_git('commit', '-m', 'fixture')
        self.commit()
        marker = self.root / 'executed'
        hook = self.root / 'filter.sh'
        hook.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\ncat\n')
        hook.chmod(0o755)
        nested_git('config', 'filter.demo.clean', str(hook))
        self.write('nested/package.json', '{"version":"2.0.0"}')
        code, data = run('inspect_repository.py', self.root)
        self.assertEqual(code, 0)
        self.assertFalse(marker.exists())
        self.assertTrue(data['git']['status_excludes_submodules'])

    def test_inherited_rust_and_distinct_dotnet_roles(self):
        self.write('Cargo.toml', '[workspace.package]\nversion="0.4.0"\n[workspace]\nmembers=["lib"]\n')
        self.write('lib/Cargo.toml', '[package]\nname="lib"\nversion.workspace=true\n')
        self.write('Directory.Build.props', '<Project><PropertyGroup><Version>1.2.3</Version><AssemblyVersion>1.0.0.0</AssemblyVersion></PropertyGroup></Project>')
        data = run('inspect_repository.py', self.root)[1]
        items = {item['path']: item for item in data['manifests']}
        self.assertEqual(items['Cargo.toml']['versions'][0]['value'], '0.4.0')
        self.assertTrue(items['lib/Cargo.toml']['unresolved'])
        self.assertEqual(len(items['Directory.Build.props']['versions']), 2)
        self.assertTrue(items['Directory.Build.props']['unresolved'])

    def test_malformed_structure_is_reported_without_crashing(self):
        self.write('package.json', '[]')
        code, data = run('inspect_repository.py', self.root)
        self.assertEqual(code, 0)
        self.assertTrue(data['manifests'][0]['unresolved'])


if __name__ == '__main__':
    unittest.main()
