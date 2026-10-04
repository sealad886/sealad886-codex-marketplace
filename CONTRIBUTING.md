# Contributing

Contributions that make the sealad886 Codex Marketplace or one of its contained plugins clearer, safer, more evidence-driven, or more adaptable are welcome.

## Choose the owning scope

- Marketplace-level changes own catalog metadata, repository policy, shared CI, issue templates, and cross-plugin documentation.
- Plugin changes belong under the canonical `plugins/<plugin-id>/` package and must follow that plugin's documented contracts and validation workflow.
- Do not create cross-plugin runtime dependencies merely to share prompts, assets, terminology, or implementation details.

Project Delivery, Conversation Visuals, MLX Optimizer, and iCloud Mail are marketplace plugins. Each package owns its contribution contract: use the [Project Delivery guide](plugins/project-delivery/README.md) for lifecycle and routing changes; the [Conversation Visuals guide](plugins/conversation-visuals/README.md) plus its [security policy](plugins/conversation-visuals/SECURITY.md) for visual-selection, MCP, provenance, privacy, and consent changes; the [MLX Optimizer guide](plugins/mlx-optimizer/README.md) for MLX skills, references, scripts, and measurement contracts; and the [iCloud Mail guide](plugins/icloud-mail/README.md) plus its [security policy](plugins/icloud-mail/SECURITY.md) for IMAP/SMTP, mailbox, credential, attachment, and mutation changes. The Project Delivery-specific guidance below does not override another package's contract.

Semantic Versioning follows the same release and validation requirements. Its [package guide](plugins/semantic-versioning/README.md) describes native examples, helper contracts, progressive disclosure, and release boundaries. Its catalog entry uses the package in this marketplace checkout so Codex can show its details before installation. Immutable Git tags still identify published releases; validate the package before publishing a new version.

Build Multi-target Tauri Apps follows the same package and release contracts. Its [guide](plugins/build-multi-target-tauri-apps/README.md) and [research ledger](plugins/build-multi-target-tauri-apps/skills/.shared/research.md) define original capability adaptation, target evidence and source freshness. Keep shared references inside its skill tree so the distribution remains self-contained.

## Before changing Project Delivery

1. Open or reference an issue when the change affects lifecycle semantics, artifact contracts, compatibility, or safety.
2. Inspect the shared operating model and the owning skill before adding a new concept.
3. Extend the canonical skill or shared reference instead of creating an overlapping skill.
4. Keep the core provider-neutral and independently useful. Integrations may be optional adapters, never hidden dependencies.

## Originality and provenance

Submit original work. Do not copy another plugin's skill text, prompts, code, icons, templates, manifests, or proprietary schemas. Capability-level research may inform a contribution, but the result must be an independently written synthesis that fits the owning plugin's terminology and operating model. Any incorporated third-party code or asset must have a compatible license, retain required notices, and be identified in the pull request.

Do not include credentials, private repository material, personal data, generated session transcripts, downloaded binaries, or another project's branded state.

## Skill contract

Every skill must retain clear answers to:

- when it is invoked;
- what inputs and repository evidence it inspects;
- what workflow and authority boundary it follows;
- what outputs and handoff it produces;
- what evidence completes it; and
- what it must not do.

Prefer a small number of substantial, non-overlapping skills. Update the operating model and templates only for conventions genuinely shared across the lifecycle.

## Codex display metadata

A plugin has two display surfaces. Keep both useful:

- `.codex-plugin/plugin.json` → `interface` describes the plugin detail page:
  display name, short and long descriptions, artwork, website, and starter prompts.
- `skills/<skill>/agents/openai.yaml` → `interface` describes an individual skill:
  `display_name`, `short_description`, `brand_color`, and `default_prompt`,
  plus skill-relative `icon_small` and `icon_large` assets.
  These fields use snake case; the plugin manifest uses camel case.
- `README.md` is the full package guide. Include a brief purpose, linked skill
  summaries, useful example requests, prerequisites, and validation instructions.

Display metadata does not replace `SKILL.md` or grant tool permissions. Keep
starter prompts within the skill's authority rules. See OpenAI's
[skill interface requirements](https://developers.openai.com/plugins/deploy/submission-errors).
For Semantic Versioning, retain the catalog-local source unless a replacement
passes native pre-install discovery. With `git-subdir`, the current Codex host
returns a cross-repository placeholder before installation; adding skill metadata
does not fix that listing. A local source in a Git-backed marketplace resolves
inside the downloaded marketplace checkout, not a developer-specific directory.
Catalog installs therefore follow the package on the marketplace branch; keep
that package at the intended published version.

Validate `plugin/read` in a fresh Codex home **before installing**: the plugin
should have a display name, descriptions, prompts, existing artwork paths, and
its three skills while `installed` is false. Verify installation and published
package identity separately.

Validate the packaged files and inspect Codex's `skills/list` response after an
isolated installation: the returned `interface` should include the intended
names, descriptions, and prompts. This checks what Codex loads; visual rendering
requires a separate app check.

## Validation

Run from the repository root:

```bash
python3 scripts/check_plugin.py plugins/project-delivery --layout source
python3 scripts/check_plugin.py plugins/conversation-visuals --layout source
python3 scripts/check_plugin.py plugins/icloud-mail --layout source
python3 scripts/check_plugin.py plugins/mlx-optimizer --layout source
python3 scripts/check_plugin.py plugins/semantic-versioning --layout source
python3 scripts/check_plugin.py plugins/build-multi-target-tauri-apps --layout source
python3 scripts/check_distribution_bundle.py plugins/build-multi-target-tauri-apps
python3 scripts/check_semantic_versioning.py
python3 scripts/check_routes.py .
python3 scripts/check_route_receipts.py \
  tests/fixtures/blind-route-observations-v1.3.1.json \
  --root . --allow-subset --allow-historical-annotations
python3 scripts/check_distribution_bundle.py plugins/project-delivery
python3 scripts/check_distribution_bundle.py plugins/conversation-visuals
python3 scripts/check_distribution_bundle.py plugins/icloud-mail
python3 scripts/check_distribution_bundle.py plugins/mlx-optimizer
python3 scripts/check_distribution_bundle.py plugins/semantic-versioning
python3 plugins/conversation-visuals/mcp/server.py --self-test
python3 plugins/icloud-mail/mcp/server.py --self-test
python3 scripts/check_marketplace.py .
python3 scripts/check_installed_parity.py <prepared-plugin-source> <installed-cache-version-dir>
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

When the Codex Plugin Creator skill is available, also run its manifest validator and validate every changed skill with Skill Creator. Release candidates must pass the pinned HOL scanner workflow with no high or critical finding.

Record exact commands, results, revision, and any checks not run. Static route-contract validation must never be described as proof of interactive agent behavior.

## Pull requests and releases

Use focused Conventional Commits. Explain the problem, user impact, design choice, validation evidence, compatibility, and residual risk in the pull request. Version plugin releases with Semantic Versioning based on the public plugin contract. The marketplace has an independent version and uses stable `marketplace-vX.Y.Z` tags; contained plugin tags and releases do not represent marketplace releases. Only maintainers publish tags and releases.

Follow the current Codex marketplace workflow for the selected source declaration. Keep the package manifest, catalog entry, displayed stable version, and validation expectations coherent in every plugin release. Create the annotated plugin version tag from the exact validated merge commit, and verify the installed plugin in a fresh task before closing the release. Publishing a stable plugin GitHub Release automatically validates that release's source commit, creates the next `marketplace-vX.Y.Z` snapshot tag at that commit, and publishes it as GitHub Latest. To publish a marketplace-only release, create and push an annotated `marketplace-vX.Y.Z` tag from the exact validated merge commit; the marketplace release workflow runs the full repository validation before publishing it as GitHub Latest.
