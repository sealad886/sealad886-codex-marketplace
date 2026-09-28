"""Execute publisher channel checks without credentials or registry side effects."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'plugins/semantic-versioning/templates/workflows/npm.yml.template'


def run_block(name, template=TEMPLATE):
    lines = template.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == '- name: ' + name)
    body = []
    active = False
    for line in lines[start + 1:]:
        if line == '        run: |':
            active = True
        elif active and line.startswith('          '):
            body.append(line[10:])
        elif active:
            break
    return '\n'.join(body)


@unittest.skipUnless(shutil.which('node'), 'Node required for actual publisher channel guard')
class PublishChannelTests(unittest.TestCase):
    def guard(self, version, channel):
        return subprocess.run(['bash', '-e', '-c', run_block('Validate npm distribution channel')], env=dict(os.environ, RELEASE_VERSION=version, NPM_DIST_TAG=channel), capture_output=True, text=True)

    def test_stable_and_authorized_preview_channels(self):
        for version, channel in [('1.2.3', 'latest'), ('1.3.0-rc.1', 'next'), ('2.0.0-beta.1', 'beta'), ('1.2.3+build-12', 'latest')]:
            with self.subTest(version=version, channel=channel):
                self.assertEqual(self.guard(version, channel).returncode, 0)

    def test_prerelease_does_not_reach_latest(self):
        result = self.guard('1.3.0-rc.1+build.2', 'latest')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('preview', result.stderr)

    def test_invalid_channel_is_rejected(self):
        for tag in ('', '--force', 'next;exit 0', '1.2.3', 'next tag'):
            self.assertNotEqual(self.guard('1.3.0', tag).returncode, 0)

    def test_publish_forwards_explicit_channel_and_artifact(self):
        command = next(line.strip()[5:] for line in TEMPLATE.read_text().splitlines() if line.strip().startswith('run: npm publish '))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / 'artifact-name.txt').write_text('package artifact.tgz')
            npm = path / 'npm'
            npm.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
            npm.chmod(0o755)
            result = subprocess.run(['bash', '-e', '-c', command], cwd=path, env=dict(os.environ, PATH=str(path) + os.pathsep + os.environ['PATH'], NPM_DIST_TAG='next'), text=True, capture_output=True)
            self.assertEqual(result.returncode, 0)
            args = result.stdout.splitlines()
            self.assertEqual(args[1], 'package artifact.tgz')
            self.assertEqual(args[args.index('--tag') + 1], 'next')


if __name__ == '__main__':
    unittest.main()
