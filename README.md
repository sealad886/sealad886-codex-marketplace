# sealad886 Codex Marketplace

[![Validate plugins](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/validate.yml)
[![HOL Plugin Scanner](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/hol-plugin-scanner.yml/badge.svg)](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/hol-plugin-scanner.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This repository is Andrew Cox's public marketplace for original Codex plugins. Each plugin is independently useful, versioned, documented, validated, and packaged beneath `plugins/<plugin-id>/`; the marketplace is the catalog and distribution boundary, not a shared runtime dependency.

The repository and marketplace are both named `sealad886-codex-marketplace`. Individual plugin IDs remain stable: Project Delivery uses `project-delivery@sealad886-codex-marketplace`, Conversation Visuals uses `conversation-visuals@sealad886-codex-marketplace`, and iCloud Mail uses `icloud-mail@sealad886-codex-marketplace`. Their skills retain the corresponding plugin prefix.

## Available plugins

| Plugin | Stable version | Purpose | Install selector |
|---|---:|---|---|
| [Project Delivery](plugins/project-delivery/README.md) | `1.4.1` | A repository-grounded, risk-scaled workflow from idea and requirements through implementation, evidence, review, release, and improvement | `project-delivery@sealad886-codex-marketplace` |
| [Conversation Visuals](plugins/conversation-visuals/README.md) | `0.1.1` | Enrich supported Codex and ChatGPT conversations with relevant sourced and generated visuals | `conversation-visuals@sealad886-codex-marketplace` |
| [iCloud Mail](plugins/icloud-mail/README.md) | `0.1.0` | Read, search, organize, draft, and send iCloud email through a local IMAP/SMTP integration | `icloud-mail@sealad886-codex-marketplace` |

Project Delivery is self-contained. It does not wrap, re-export, or require the generic workflow plugins it is designed to supersede. Provider connectors and specialist platform tools may still contribute authorized access or evidence without becoming lifecycle dependencies.

## Install from the marketplace

Add the hosted marketplace, then install the plugin you want:

```bash
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add project-delivery@sealad886-codex-marketplace
codex plugin add conversation-visuals@sealad886-codex-marketplace
codex plugin add icloud-mail@sealad886-codex-marketplace
```

Start a fresh Codex task after installation so the current plugin catalog and skill metadata are loaded.

### iCloud Mail setup

iCloud Mail stores the non-secret account address and optional outgoing aliases
through its `configure_account` tool; no persistent username shell export is
required. Apple requires two-factor authentication before an app-specific
password can be generated. Never give the plugin the primary Apple Account
password.

Apple documents the local part of the iCloud Mail address as the normal IMAP
username—for example `name` for `name@icloud.com`—with the full address as the
fallback. SMTP always authenticates with the full account address. An explicit
saved `imap_username` overrides automatic selection. Incoming mail for every
iCloud alias is already in the same mailbox; `allowed_from` is a comma-delimited
or array setting for outgoing identities only.

On macOS, the guided setup opens Keychain Access so the app-specific password
can be stored without entering it in chat or a tool argument. On other systems,
put `ICLOUD_MAIL_APP_PASSWORD` in the environment that launches Codex. An
`export` performed in another shell after Codex starts will not reach the MCP
process. See the [iCloud Mail guide](plugins/icloud-mail/README.md) for the full
setup and security boundary.

## Repository and package boundaries

```text
sealad886-codex-marketplace/
├── .agents/plugins/marketplace.json   hosted marketplace catalog
├── .github/                           repository CI and templates
├── references/                        research, audit, and release evidence
├── scripts/                           dependency-free validation and packaging tools
├── tests/                             semantic contracts and regression tests
└── plugins/
    ├── project-delivery/              canonical installable plugin
    ├── conversation-visuals/          installable visual conversation plugin
    └── icloud-mail/                   installable iCloud email plugin
        ├── .codex-plugin/plugin.json
        ├── .mcp.json
        ├── README.md
        ├── LICENSE
        ├── assets/
        ├── mcp/
        └── skills/
```

Only a plugin's own subtree is installable. Repository CI, tests, contributor tooling, audit evidence, Git metadata, and development environments stay outside installed payloads. Marketplace entries use supported, validated source declarations that resolve to the intended package rather than the repository root.

The marketplace itself is loaded from the hosted GitHub repository. A catalog
entry with `source: "local"` resolves a repository-relative plugin subtree
inside that GitHub-fetched marketplace checkout; it does not read from a
user's development checkout. Project Delivery instead uses an immutable
`git-subdir` release reference. Repository-relative packages retain their own
versioned release identity and immutable tag even though complete manifest and
branding metadata are served from the hosted marketplace checkout.

Every marketplace plugin must:

- have a unique lower-case hyphen-case plugin ID and contained `plugins/<plugin-id>/` path;
- include a valid `.codex-plugin/plugin.json` and package-local documentation;
- declare its own capabilities, trust boundary, dependencies, licensing, and release version;
- remain useful without another Andrew Cox plugin unless an explicit optional relationship is documented;
- carry a Semantic Versioning release identity and a resolvable immutable release tag;
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
python3 scripts/check_plugin.py plugins/conversation-visuals --layout source
python3 scripts/check_plugin.py plugins/icloud-mail --layout source
python3 scripts/check_routes.py .
python3 scripts/check_route_receipts.py \
  tests/fixtures/blind-route-observations-v1.3.1.json \
  --root . --allow-subset --allow-historical-annotations
python3 scripts/check_distribution_bundle.py plugins/project-delivery
python3 scripts/check_distribution_bundle.py plugins/conversation-visuals
python3 scripts/check_distribution_bundle.py plugins/icloud-mail
python3 plugins/conversation-visuals/mcp/server.py --self-test
python3 plugins/icloud-mail/mcp/server.py --self-test
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

This marketplace and its plugins are maintained by Andrew Cox and licensed under their included MIT licenses. Copyright © 2026 Andrew Cox.
