#!/usr/bin/env python3
"""Validate executable example structure and the plugin's disclosure budget."""
from pathlib import Path
import argparse
import json
import re
import sys
import tomllib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / 'plugins' / 'semantic-versioning'

def validate(root):
    errors = []
    counts = {}
    for path in sorted((root / 'skills').glob('*/SKILL.md')):
        body = path.read_text().split('---', 2)[-1]
        counts[path.parent.name] = len(body.split())
        if counts[path.parent.name] >= 900:
            errors.append(f'{path}: skill body must be below 900 words')
    for path in sorted(root.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        try:
            if path.suffix == '.json':
                json.loads(path.read_text())
            elif path.suffix == '.toml':
                tomllib.loads(path.read_text())
            elif path.suffix in ('.xml', '.csproj', '.props', '.svg', '.plist'):
                ET.parse(path)
            elif path.name.endswith('.yml.template'):
                # Pin integrity is an intentional supply-chain contract; YAML/shell
                # semantics are checked separately with actionlint in CI.
                for action in re.findall(r'^\s*-?\s*uses:\s*(\S+)', path.read_text(), re.M):
                    if not action.startswith('./') and not re.fullmatch(r'[^@]+@[0-9a-f]{40}', action):
                        errors.append(f'{path}: external action must use an immutable SHA: {action}')
        except (ValueError, ET.ParseError) as error:
            errors.append(f'{path}: {error}')
    return errors, counts

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=ROOT)
    args = parser.parse_args()
    errors, counts = validate(args.root)
    for name, count in counts.items():
        print(f'{name}: {count} words')
    for error in errors:
        print(error, file=sys.stderr)
    return bool(errors)

if __name__ == '__main__':
    sys.exit(main())
