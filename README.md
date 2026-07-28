# sealad886 Codex Marketplace

[![Validate plugins](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/validate.yml)
[![HOL Plugin Scanner](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/hol-plugin-scanner.yml/badge.svg)](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/hol-plugin-scanner.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This repository is Andrew Cox's public marketplace for original Codex plugins. Each plugin is independently useful, versioned, documented, validated, and packaged beneath `plugins/<plugin-id>/`; the marketplace is the catalog and distribution boundary, not a shared runtime dependency.

The repository and marketplace are both named `sealad886-codex-marketplace`. Individual plugin IDs remain stable, so installing Project Delivery uses the selector `project-delivery@sealad886-codex-marketplace` and its skills remain `project-delivery:<skill>`.

## Available plugins

| Plugin | Stable version | Purpose | Install selector |
|---|---:|---|---|
| [Project Delivery](plugins/project-delivery/README.md) | `1.4.0` | A repository-grounded, risk-scaled workflow from idea and requirements through implementation, evidence, review, release, and improvement | `project-delivery@sealad886-codex-marketplace` |

Project Delivery is self-contained. It does not wrap, re-export, or require the generic workflow plugins it is designed to supersede. Provider connectors and specialist platform tools may still contribute authorized access or evidence without becoming lifecycle dependencies.

## Install from the marketplace

Add the hosted marketplace, then install the plugin you want:

```bash
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add project-delivery@sealad886-codex-marketplace
```

Start a fresh Codex task after installation so the current plugin catalog and skill metadata are loaded.

### Migrate a former marketplace name

The repository was formerly published as `sealad886/project-delivery`, with marketplace ID `project-delivery`, and briefly as `sealad886/andrew-cox-codex-marketplace`, with marketplace ID `andrew-cox-codex-marketplace`. Add and verify the canonical selector before removing any former control-plane entries:

```bash
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add project-delivery@sealad886-codex-marketplace
codex plugin list
codex plugin remove project-delivery@andrew-cox-codex-marketplace
codex plugin marketplace remove andrew-cox-codex-marketplace
codex plugin remove project-delivery@project-delivery
codex plugin marketplace remove project-delivery
```

Run only the removal pair or pairs that `codex plugin list` still reports. Do not remove a former selector until the canonical selector is installed, enabled, and verified.

The plugin ID, version, package contents, icons, and skill selectors do not change during this migration. The marketplace remains pinned to the immutable `v1.4.0` package; the rename changes repository and catalog identity, not the released plugin bytes.

## Repository and package boundaries

```text
sealad886-codex-marketplace/
├── .agents/plugins/marketplace.json   hosted marketplace catalog
├── .github/                           repository CI and templates
├── references/                        research, audit, and release evidence
├── scripts/                           dependency-free validation and packaging tools
├── tests/                             semantic contracts and regression tests
└── plugins/
    └── project-delivery/              canonical installable plugin
        ├── .codex-plugin/plugin.json
        ├── README.md
        ├── LICENSE
        ├── assets/
        └── skills/
```

Only a plugin's own subtree is installable. Repository CI, tests, contributor tooling, audit evidence, Git metadata, and development environments stay outside installed payloads. Marketplace entries use `git-subdir` and immutable release refs so Codex receives the intended package rather than the repository root.

Every marketplace plugin must:

- have a unique lower-case hyphen-case plugin ID and contained `plugins/<plugin-id>/` path;
- include a valid `.codex-plugin/plugin.json` and package-local documentation;
- declare its own capabilities, trust boundary, dependencies, licensing, and release version;
- remain useful without another Andrew Cox plugin unless an explicit optional relationship is documented;
- be pinned to a resolvable immutable tag or commit before the catalog advertises it;
- pass Plugin Creator validation and an evidence-proportional release review in the change that adds it; and
- add its package-specific validation to repository CI before becoming available.

## Local development

Clone the marketplace outside any personal plugin destination:

```bash
git clone https://github.com/sealad886/sealad886-codex-marketplace.git ~/src/sealad886-codex-marketplace
cd ~/src/sealad886-codex-marketplace
```

For Project Delivery, materialize the exact validated package into a separate local source:

```bash
python3 scripts/check_distribution_bundle.py plugins/project-delivery \
  --output ~/plugins/project-delivery
```

Use `--replace` only for a destination that the materializer proves is an exact, clean Project Delivery distribution. Then use Codex's system Plugin Creator workflow to validate, register, cachebust, and reinstall that prepared local source. Do not point a local marketplace at the development checkout root or hand-edit Codex-managed cache state.

The detailed product, lifecycle, installation, migration, and trust documentation lives in the [Project Delivery package guide](plugins/project-delivery/README.md).

## Validation

The current checks use only Python's standard library:

```bash
python3 scripts/check_plugin.py plugins/project-delivery --layout source
python3 scripts/check_routes.py .
python3 scripts/check_route_receipts.py \
  tests/fixtures/blind-route-observations-v1.3.1.json \
  --root . --allow-subset --allow-historical-annotations
python3 scripts/check_distribution_bundle.py plugins/project-delivery
python3 scripts/check_marketplace.py .
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Release validation also includes the system Plugin Creator validator, exact package/cache comparison, the pinned HOL scanner, fresh-task canaries where behavior is claimed, and independent review. Static package and icon checks are reported separately from live Codex UI evidence.

## Governance

- [Project Delivery guide](plugins/project-delivery/README.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Security policy](SECURITY.md)
- [Support](SUPPORT.md)
- [Design brief](references/design-brief.md)
- [Environment and capability audit](references/environment-audit.md)
- [Migration and decommission map](references/migration-and-decommission.md)
- [Validation report](references/validation-report.md)

This marketplace and its current Project Delivery plugin are maintained by Andrew Cox and licensed under the [MIT License](LICENSE). Copyright © 2026 Andrew Cox.
