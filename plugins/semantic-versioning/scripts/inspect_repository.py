#!/usr/bin/env python3
"""Read-only release discovery; candidates require human/agent contract assessment."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib
import xml.etree.ElementTree as ET

SKIP = {'.git', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build', '.worktrees', '__pycache__', '.gradle', 'vendor'}
NAMES = {'package.json': 'javascript', 'pyproject.toml': 'python', 'Cargo.toml': 'rust', 'go.mod': 'go', 'pom.xml': 'jvm', 'build.gradle': 'jvm', 'build.gradle.kts': 'jvm', 'gradle.properties': 'jvm', 'Directory.Build.props': 'dotnet', 'Directory.Packages.props': 'dotnet', 'Package.swift': 'mobile', 'Info.plist': 'mobile', 'pubspec.yaml': 'mobile', 'CMakeLists.txt': 'native', 'conanfile.py': 'native', 'conanfile.txt': 'native', 'vcpkg.json': 'native', 'composer.json': 'ruby-php', 'Chart.yaml': 'artifacts', 'Dockerfile': 'artifacts', 'plugin.json': 'artifacts'}
CONFIGS = {'release-please-config.json': 'release-please', '.release-please-manifest.json': 'release-please', '.releaserc': 'semantic-release', '.releaserc.json': 'semantic-release', 'release.config.js': 'semantic-release', 'release.config.cjs': 'semantic-release', 'release.config.mjs': 'semantic-release', 'release.toml': 'cargo-release', 'release-plz.toml': 'release-plz', '.goreleaser.yaml': 'goreleaser', '.goreleaser.yml': 'goreleaser', 'lerna.json': 'lerna', 'GitVersion.yml': 'gitversion', 'version.json': 'git-derived-candidate'}


def git(root, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
    result = subprocess.run(['git', '-c', 'core.fsmonitor=false', '-C', str(root), '--no-pager', *args], capture_output=True, text=True, env=env, timeout=15)
    return result.stdout.strip() if result.returncode == 0 else None


def manifest(path, root, family):
    family = {'native': 'cpp', 'artifacts': 'containers-plugins'}.get(family, family)
    item = {'path': path.relative_to(root).as_posix(), 'ecosystem': family, 'versions': [], 'unresolved': []}
    try:
        if path.stat().st_size > 1_000_000:
            raise ValueError('Manifest exceeds 1 MB inspection limit')
        raw = path.read_text(encoding='utf-8')
        if path.suffix == '.json':
            data = json.loads(raw)
            for key in ('version', 'version-semver', 'version-string'):
                if key in data:
                    item['versions'].append({'field': key, 'value': data[key]})
            item['name'] = data.get('name')
            if 'private' in data:
                item['private'] = data['private']
            if 'workspaces' in data:
                item['workspaces'] = data['workspaces']
            if path.name == 'package.json':
                item['release_hints'] = [key for key in ('release',) if key in data]
                item['release_tools'] = sorted(set(data.get('devDependencies', {})) & {'semantic-release', '@changesets/cli', 'release-please'})
        elif path.suffix == '.toml':
            data = tomllib.loads(raw)
            fields = [('project', data.get('project', {})), ('package', data.get('package', {})), ('workspace.package', data.get('workspace', {}).get('package', {})), ('tool.poetry', data.get('tool', {}).get('poetry', {}))]
            for prefix, table in fields:
                if 'version' in table:
                    if isinstance(table['version'], str):
                        item['versions'].append({'field': prefix + '.version', 'value': table['version']})
                    else:
                        item['unresolved'].append(prefix + '.version is inherited or dynamic')
                if 'version' in table.get('dynamic', []):
                    item['unresolved'].append(prefix + '.version is dynamic; inspect build backend')
                if table.get('name'):
                    item['name'] = table['name']
            if data.get('workspace'):
                item['workspace_members'] = data['workspace'].get('members', [])
            item['build_backend'] = data.get('build-system', {}).get('build-backend')
        elif path.name == 'go.mod':
            match = re.search(r'^module\s+(\S+)', raw, re.M)
            item['name'] = match[1] if match else None
            item['unresolved'].append('Version is derived from module-specific Git tags')
        elif path.suffix in ('.xml', '.csproj', '.props', '.fsproj'):
            tree = ET.fromstring(raw)
            for child in tree.iter():
                name = child.tag.split('}')[-1]
                # Maven dependency versions are not project versions.
                if name in ('Version', 'VersionPrefix', 'PackageVersion', 'AssemblyVersion', 'FileVersion', 'revision') or (name == 'version' and child in list(tree)):
                    value = child.text or ''
                    if '$' in value or not value:
                        item['unresolved'].append(name + ' requires property resolution')
                    else:
                        item['versions'].append({'field': name, 'value': value})
        else:
            # Code/YAML definitions are deliberately not evaluated or guessed.
            item['unresolved'].append('Requires native metadata inspection; configuration is not executed')
        if len({str(v['value']) for v in item['versions']}) > 1:
            item['unresolved'].append('Multiple version values; determine distinct roles or drift')
        if not item['versions'] and not item['unresolved']:
            item['unresolved'].append('No static version found; resolve inherited/tag-derived owner')
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError, ET.ParseError) as error:
        item['unresolved'].append(str(error))
    return item


def inspect(root, scope):
    root = root.resolve(strict=True)
    target = (root / scope).resolve(strict=True) if scope else root
    if not root.is_dir() or not target.is_dir() or not target.is_relative_to(root):
        raise ValueError('Scope must be a directory within root')
    manifests, configs = [], []
    # Scan root so inherited owner configuration remains visible for a scoped package.
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not (Path(directory) / d).is_symlink())
        for name in sorted(files):
            path = Path(directory) / name
            if path.is_symlink():
                continue
            rel = path.relative_to(root).as_posix()
            owner = CONFIGS.get(name)
            if name == 'config.json' and path.parent.name == '.changeset':
                owner = 'changesets'
            if owner:
                configs.append({'path': rel, 'owner_candidate': owner})
            family = NAMES.get(name)
            if name.endswith(('.csproj', '.fsproj')):
                family = 'dotnet'
            if name.endswith('.gemspec'):
                family = 'ruby-php'
            if family and (path.is_relative_to(target) or path.parent in target.parents):
                manifests.append(manifest(path, root, family))
    head = git(root, 'rev-parse', 'HEAD')
    tags = git(root, 'for-each-ref', '--merged=HEAD', '--format=%(refname:short)%09%(*objectname)%09%(objectname)', 'refs/tags') if head else None
    candidates = []
    for row in (tags or '').splitlines():
        tag, peeled, direct = row.split('\t')
        candidates.append({'tag': tag, 'commit': peeled or direct, 'selected': False})
    shallow = git(root, 'rev-parse', '--is-shallow-repository')
    owners = sorted({c['owner_candidate'] for c in configs})
    return {'schema_version': 1, 'root': str(root), 'scope': target.relative_to(root).as_posix(),
            'manifests': manifests, 'release_configurations': configs,
            'owner_candidates': owners,
            'git': {'head': head, 'branch': git(root, 'symbolic-ref', '--short', '-q', 'HEAD'), 'status': git(root, 'status', '--porcelain=v1', '--untracked-files=all'), 'shallow': shallow == 'true', 'baseline_candidates': candidates},
            'references': sorted({m['ecosystem'] for m in manifests}),
            'unresolved': ['Baseline candidates are ancestry-filtered but not package-filtered or selected. Verify package tag convention and published release state.'] + (['Multiple owner candidates; scope their responsibilities before editing.'] if len(owners) > 1 else []) + (['History is shallow; release baseline evidence may be incomplete.'] if shallow == 'true' else []) + ([] if head else ['No Git HEAD; establish initial-release policy.'])}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--scope', default='')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        result, code = inspect(args.root, args.scope), 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        result, code = {'schema_version': 1, 'error': str(error)}, 2
    if args.json:
        print(json.dumps(result, indent=2))
    elif code:
        print(result['error'])
    else:
        print(f"{len(result['manifests'])} manifests; owners: {', '.join(result['owner_candidates']) or 'unresolved'}")
        for item in result['manifests']:
            values = ', '.join(f"{v['field']}={v['value']}" for v in item['versions'])
            print(f"{item['path']}: {values or 'version unresolved'}")
            for issue in item['unresolved']:
                print(f"  {issue}")
        print(f"{len(result['git']['baseline_candidates'])} reachable baseline candidates; none selected")
        for issue in result['unresolved']:
            print(issue)
    return code


if __name__ == '__main__':
    sys.exit(main())
