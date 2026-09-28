#!/usr/bin/env python3
"""Materialize inactive release examples and check native workflow interfaces."""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actionlint', default='actionlint')
    args = parser.parse_args()
    executable = shutil.which(args.actionlint)
    if not executable:
        parser.error('actionlint is required; use the pinned CI tool or an existing installation')
    templates = ROOT / 'plugins/semantic-versioning/templates/workflows'
    failed = False
    for publisher in sorted(templates.glob('*.yml.template')):
        if publisher.name == 'release-please.yml.template':
            continue
        with tempfile.TemporaryDirectory(prefix='semver-workflow-') as temporary:
            root = Path(temporary)
            workflows = root / '.github/workflows'
            workflows.mkdir(parents=True)
            standalone = publisher.name in ('changesets.yml.template', 'semantic-release.yml.template')
            files = []
            if not standalone:
                coordinator = workflows / 'release.yml'
                shutil.copyfile(templates / 'release-please.yml.template', coordinator)
                files.append(coordinator)
            destination = workflows / ('release.yml' if standalone else 'release-publish.yml')
            shutil.copyfile(publisher, destination)
            files.append(destination)
            # actionlint discovers local reusable workflows from the repository root.
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            result = subprocess.run([executable, '-no-color', *map(str, files)], cwd=root, capture_output=True, text=True)
            print(f'{publisher.name}: {"PASS" if result.returncode == 0 else "FAIL"}')
            if result.returncode:
                print(result.stdout + result.stderr)
                failed = True
    return int(failed)

if __name__ == '__main__':
    raise SystemExit(main())
