# Validation report

Validation date: 2026-07-21

Release: `v1.4.0`

Validated RC merge ancestor: `aec6a8b`

Canonical package: `plugins/project-delivery/`

## Decision

Project Delivery stable `1.4.0` is published and passes its post-publication hosted installation canary. The immutable release tag identifies artifact merge `db6aa16`; the later untagged catalog merge `950bdd3` points the Git-backed marketplace at `v1.4.0`. The 64-file stable package passes local and hosted validation, the current 157-test regression suite, Plugin Creator validation, exact tag/install parity, independent release review, and a fresh-process catalog/asset canary.

The stable promotion changes release identity only; it preserves the public capability surface already validated in `1.4.0-rc.1`. Hosted parity confirmed exactly one enabled Project Delivery `1.4.0` installation from the immutable GitHub ref; the temporary personal canary registration was removed after that check, preventing duplicate selector exposure. Provider connectors and domain-specific evidence plugins remain outside the replacement scope.

## Evidence

| Gate | Result |
|---|---|
| Plugin structure and references | Pass: 64 files, 13 skills, five shared runtime resources |
| Route profiles and contracts | Pass: 24/24 profiles; all 13 skills covered; ownership, authority, gates, evidence, and stop conditions aligned |
| Historical receipts | Pass: 17/17 records remain compatible |
| Regression suite | Pass: 157/157 with `GIT_CONFIG_GLOBAL=/dev/null` after adding immutable marketplace-ref coverage; the tagged artifact suite passed 155/155 before the catalog-only tests were added |
| Distribution boundary | Pass: no undeclared files, symlinks, executables, source-only paths, or unsupported types; stable source payload SHA-256 `f48258fe08d51de3a392cfdedbac1f326c516daeda3d6ca9c0879c6c417f48f1` |
| Marketplace and license | Pass: Git-backed `git-subdir` entry resolves `v1.4.0` at `plugins/project-delivery`; root/package MIT text is byte-identical |
| Plugin Creator | Pass on stable source and prepared source |
| Skill validation | Pass: 13/13 skills |
| Icons | Pass: 28/28 PNGs decode; 14 small assets are 128×128 and 14 large assets are 512×512 |
| Skill icon references | Pass: all 26 small/large paths in `agents/openai.yaml` resolve within the package |
| Duplicate selectors | Pass: none |
| Legacy dependencies | Pass: no hard dependency on Boss, Epic/Epic Harness, or Superpowers in the installable package |
| Hosted PR checks | Pass: validate, HOL scan, plugin-scanner, and GitGuardian on release PR #4 and marketplace PR #5 |
| Pre-release personal canary | Pass: `project-delivery@personal` version `1.4.0+codex.20260721203943`; registration removed after hosted parity passed |
| Hosted install | Pass: exactly one enabled Project Delivery entry, version `1.4.0`, sourced from GitHub ref `v1.4.0` |
| Tag/install parity | Pass: exact 64-file source/cache comparison; payload SHA-256 `f48258fe08d51de3a392cfdedbac1f326c516daeda3d6ca9c0879c6c417f48f1` |
| RC fresh-process smoke | Pass: exact `1.4.0-rc.1` marker, installed manifest/orchestrator match, and expected `small-bug-planning` route under planning-only authority |
| Stable hosted fresh-process smoke | Pass: orchestrator and all 13 selectors prompt-visible; 28/28 PNGs decode at expected dimensions; 26/26 YAML icon references resolve; no duplicate selector, stale version, or legacy dependency |

Reproduction commands:

```bash
.venv/bin/python scripts/check_plugin.py plugins/project-delivery --layout source
.venv/bin/python scripts/check_routes.py .
.venv/bin/python scripts/check_distribution_bundle.py plugins/project-delivery
.venv/bin/python scripts/check_marketplace.py .
GIT_CONFIG_GLOBAL=/dev/null .venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

## Canary findings incorporated

The release-candidate canaries found incomplete capability ownership, controller ordering, future-retrospective activation, stale installed identity, broad specialist-load claims, and weak gap linkage. Those findings drove the schema-v3 receipts, installed route profiles, exact package boundary, and regression coverage in the stable package.

The final pre-fix sealed 24-scenario task at `8cc215c` failed for four narrow reasons: a miscomputed semantic digest, uncited branch gaps, delivery-input gaps incorrectly marked route-blocking, and direct-retrospective intake requiring evidence that the prompt did not provide. Commit `81b50ba` corrected those semantics and added focused positive/negative tests. The heavyweight live matrix was not repeated for the stable identity-only promotion; it remains an optional confidence check rather than a file-installation gate.

The latest iOS Backup Viewer canary correctly refused a release-ready verdict because that separate repository revision moved, its worktree contained concurrent changes, and its full Swift suite stalled in an external macOS Address Book/CoreData service. It preserved that checkout and stopped only its own test process. That is expected evidence handling, not a Project Delivery failure.

## Bounded limitations

- Static inspection proves catalog metadata, icon assets, image decoding, dimensions, and reference reachability. It does not prove that protected Codex UI pixels rendered visually. A full Codex Desktop relaunch may be needed before existing tasks display refreshed cards.
- A delegated task created from a long-running parent can inherit an old skill-catalog snapshot. The final selector and asset canary therefore used a fresh ephemeral Codex CLI process. Ordinary smoke prompts require `PROJECT_DELIVERY_VERSION=<expected-version>` as the first line; sealed JSON uses `plugin_identity.installed_version`.
- Cisco's optional skill-scanner integration was unavailable under Python 3.14. The main scanner and hosted checks do not depend on it.
- The Project Delivery release does not prove release readiness of the unrelated iOS Backup Viewer repository.

## Release and adoption disposition

- Stable release `v1.4.0` is published at immutable artifact merge `db6aa16`.
- The untagged Git-backed marketplace pointer at catalog merge `950bdd3` resolves immutable ref `v1.4.0`; hosted install and fresh-process catalog/asset canary pass.
- Keep `project-delivery@sealad886-codex-marketplace` installed as the canonical generic PM/software-delivery workflow. The 2026-07-21 result above remains historical evidence for the unchanged `v1.4.0` package.
- Keep `v1.4.0-rc.1` available as a bounded rollback artifact; stable `v1.4.0` is the active source.
- Uninstall Boss, Epic/Epic Harness, Superpowers, or other superseded generic workflow plugins only after confirming the stable tagged package remains available and the desired rollback source is recorded.
- Keep provider connectors, platform tools, security scanners, and domain-specific plugins unless separately judged redundant.
