# Validation report

Validation date: 2026-07-29

Release: `v1.4.1`

Canonical package: `plugins/project-delivery/`

Install selector: `project-delivery@sealad886-codex-marketplace`

## Decision

Project Delivery `1.4.1` is the canonical generic project-management and software-delivery workflow in this Codex environment. The published package, marketplace entry, installed cache, and fresh-task callbacks all identify the same release. Boss, Epic, and Superpowers are not installed; Project Delivery remains enabled and passed a fresh callback with each of those plugins absent.

The release provides a 13-skill lifecycle and 24 routing profiles. The marketplace uses the canonical repository and an explicit Git-backed release sequence. Validation binds semantic-version marketplace tags to the version declared by the pinned plugin manifest.

## Release identity

| Field | Verified value |
|---|---|
| Artifact merge | `a63079da03cfbcef721d5c829e8d1abfaa8c0838` |
| Annotated tag object | `6244dab9acae59b408f9f33d86ccb34783685060` |
| Tag peeled commit | `a63079da03cfbcef721d5c829e8d1abfaa8c0838` |
| Catalog merge | `ee762a06e543b856068e0d808ac471a367b88c3a` |
| Marketplace ref | `v1.4.1` |
| Installed version | `1.4.1` |
| Package files | 64 |
| Skills | 13 |
| Source/cache payload SHA-256 | `a7fd17d4423457937f5ecbabe3f0fe7211797efc63cb3ff85013faead7501945` |
| Root/package MIT SHA-256 | `486b9c74f1d5bf1a5be12a8fe070db7cfad5a4901f083d4810a677b32f2d4993` |

The local and remote `v1.4.1` tag identities agree. The GitHub release is published, non-draft, and non-prerelease. The marketplace snapshot resolves catalog merge `ee762a0` and the installed cache is an exact byte-for-byte copy of the tagged 64-file Project Delivery subtree.

## Validation evidence

| Gate | Result |
|---|---|
| Plugin structure and references | Pass: 64 files, 13 skills, five shared runtime resources |
| Route profiles and contracts | Pass: 24/24 profiles; all 13 skills covered |
| Route receipt compatibility | Pass: 17/17 |
| Regression suite | Pass: 163/163 |
| Focused marketplace suite | Pass: 11/11 |
| Distribution boundary | Pass: no undeclared files, symlinks, executables, source-only paths, or unsupported types |
| Marketplace and pinned identity | Pass: `git-subdir` ref `v1.4.1` resolves; pinned manifest reports `1.4.1`; category and package identity match |
| Plugin Creator | Pass on the `1.4.1` package |
| MIT license | Pass: root/package text is byte-identical and unchanged |
| Icons | Pass: 28/28 installed PNGs decode; 14 are 128×128 and 14 are 512×512 |
| Installed parity | Pass: 64 files and 13 skills, exact source/cache parity |
| Duplicate selector | Pass: exactly one enabled Project Delivery selector |
| Legacy dependency scan | Pass: the installable package has no hard dependency on Boss, Epic, or Superpowers |
| Artifact PR #10 | Pass: validation, HOL scan, plugin scanner, and GitGuardian |
| Catalog PR #11 | Pass: validation, HOL scan, plugin scanner, and GitGuardian |
| Independent artifact review | Pass: no release-blocking finding |
| Independent catalog review | Pass: no release-blocking finding |

Reproduction commands:

```bash
python3 scripts/check_plugin.py plugins/project-delivery --layout source
python3 scripts/check_routes.py .
python3 scripts/check_distribution_bundle.py plugins/project-delivery
python3 scripts/check_marketplace.py .
GIT_CONFIG_GLOBAL=/dev/null python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_installed_parity.py \
  plugins/project-delivery \
  ~/.codex/plugins/cache/sealad886-codex-marketplace/project-delivery/1.4.1
```

Use the repository's declared Python environment when the system interpreter does not provide the validation dependencies.

## Fresh-task evidence

Two post-installation tasks ran against the current iOS Backup Viewer checkout without modifying it:

- The orchestrator callback began with `PROJECT_DELIVERY_VERSION=1.4.1`, loaded the installed orchestrator and required specialists, selected the `small-bug-planning` route, and produced repository-grounded requirements, design, security, planning, and test-evidence boundaries.
- A direct `review-audit` callback began with `PROJECT_DELIVERY_VERSION=1.4.1`, loaded the installed specialist directly, and correctly blocked release readiness because the unrelated checkout was dirty and its available artifact evidence belonged to an older revision.

These callbacks prove installed-version pickup, direct and orchestrated skill loading, risk-scaled routing, repository grounding, and evidence-bounded conclusions. They do not establish release readiness for the unrelated iOS Backup Viewer repository.

## Installed workflow state

The supported Codex plugin control plane reports this generic workflow state:

| Plugin | Current state | Project Delivery callback evidence |
|---|---|---|
| `project-delivery@sealad886-codex-marketplace` | Installed and enabled at `1.4.1` | Pass: installed orchestrator loaded and routed |
| `boss@awesome-codex-plugins` | Not installed | Pass: Boss absent; Project Delivery `1.4.1` enabled and routed |
| `epic@awesome-codex-plugins` | Not installed | Pass: Boss and Epic absent; Project Delivery `1.4.1` enabled and routed |
| `superpowers@openai-curated` | Not installed | Pass: all three superseded plugins absent; Project Delivery `1.4.1` enabled and routed |

Readback confirms that the three superseded selectors are absent from the installed-plugin list and active plugin configuration. Residual marketplace cache content or inactive hook-state metadata is not treated as installed-plugin state. The configured `awesome-codex-plugins` and `openai-curated` marketplaces remain available as bounded recovery sources. Provider connectors, platform-specific builders, security scanners, review integrations, and other specialist plugins remain installed according to their independent use cases.

## Bounded limitations

- Static validation proves that installed icon files decode, have the expected dimensions, and are referenced by the package. It does not prove protected Codex Desktop pixels rendered. Existing tasks or cards can retain an earlier process snapshot until the app is relaunched.
- A long-running Codex process can expose an obsolete cache path in its initial skill metadata. Each canary therefore inspected the installed manifest and reported `PROJECT_DELIVERY_VERSION=1.4.1` explicitly before using the installed instruction files.
- The marketplace accepts immutable annotated tags but does not cryptographically enforce remote tag immutability. Current local and remote tag objects and peeled commits match exactly.
- The semantic-version tag grammar retains a low-severity edge case for numeric prerelease identifiers with leading zeroes. It does not affect stable tag `v1.4.1`.

## Current disposition

- Use `project-delivery@sealad886-codex-marketplace` as the canonical generic project-delivery workflow.
- Project Delivery `1.4.1` is installed and enabled from the canonical `v1.4.1` package.
- Boss, Epic, and Superpowers are not installed.
- Specialized plugins remain independently available for provider access, platform engineering, security analysis, review, and domain-specific evidence.
