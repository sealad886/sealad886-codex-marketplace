# Contributing

Contributions that make the sealad886 Codex Marketplace or one of its contained plugins clearer, safer, more evidence-driven, or more adaptable are welcome.

All new and updated plugins must remain valid for both Codex and GitHub Copilot.
The repository's [agent instructions](AGENTS.md) define the required catalog,
manifest, MCP, packaging, and verification rules for both marketplaces.

## Choose the owning scope

- Marketplace-level changes own catalog metadata, repository policy, shared CI, issue templates, and cross-plugin documentation.
- Plugin changes belong under the canonical `plugins/<plugin-id>/` package and must follow that plugin's documented contracts and validation workflow.
- Do not create cross-plugin runtime dependencies merely to share prompts, assets, terminology, or implementation details.

Project Delivery, Conversation Visuals, MLX Optimizer, and iCloud Mail are marketplace plugins. Each package owns its contribution contract: use the [Project Delivery guide](plugins/project-delivery/README.md) for lifecycle and routing changes; the [Conversation Visuals guide](plugins/conversation-visuals/README.md) plus its [security policy](plugins/conversation-visuals/SECURITY.md) for visual-selection, MCP, provenance, privacy, and consent changes; the [MLX Optimizer guide](plugins/mlx-optimizer/README.md) for MLX skills, references, scripts, and measurement contracts; and the [iCloud Mail guide](plugins/icloud-mail/README.md) plus its [security policy](plugins/icloud-mail/SECURITY.md) for IMAP/SMTP, mailbox, credential, attachment, and mutation changes. The Project Delivery-specific guidance below does not override another package's contract.

Semantic Versioning follows the same release and validation requirements. Its [package guide](plugins/semantic-versioning/README.md) describes native examples, helper contracts, progressive disclosure, and release boundaries. Its catalog entry uses the package in this marketplace checkout so Codex can show its details before installation. Immutable Git tags still identify published releases; validate the package before publishing a new version.

Build Multi-target Tauri Apps follows the same package and release contracts. Its [guide](plugins/build-multi-target-tauri-apps/README.md) and [research ledger](plugins/build-multi-target-tauri-apps/skills/.shared/research.md) define original capability adaptation, target evidence and source freshness. Keep shared references inside its skill tree so the distribution remains self-contained.

The standalone workflow plugins each expose one skill: [Iterating PR Bot Fixes](plugins/iterating-pr-bot-fixes/README.md), [Repository Consolidation](plugins/repo-consolidation/README.md), [Conventional Commit](plugins/conventional-commit/README.md), [Simplify Code](plugins/simplify-code/README.md), [Adversarial Audit](plugins/adversarial-audit/README.md), [Web Research](plugins/web-research/README.md), and [Repository Guidance](plugins/repository-guidance/README.md). Their guides define invocation, prerequisites, authority, outputs, and verification. Keep supporting references and templates beneath the owning skill; another plugin or a sibling skill directory must not be a hidden runtime dependency.

## Camofox Browser source ownership

[Camofox Browser](plugins/camofox-mcp/README.md) is maintained in
[`sealad886/camofox-mcp`](https://github.com/sealad886/camofox-mcp). Make runtime,
setup, skill, asset and version changes there first. After its matching npm
version is published, copy that release's entire `plugin/` directory to
`plugins/camofox-mcp/`, including hidden files. Verify byte parity, package
validation and a clean consumer installation before publishing this marketplace.
The local catalog source keeps the full plugin details visible before install.
Do not create a second server implementation or follow npm latest implicitly.

Local Translation owns its [package guide](plugins/local-translation/README.md)
and [security policy](plugins/local-translation/SECURITY.md). Its stdlib MCP runtime
supports text and explicit segments through an operator-configured local
Index-Translate runner. Run
`python3 -m unittest discover -s tests -p 'test_local_translation.py' -v`
and `python3 -m unittest discover -s tests -p 'test_local_translation_settings.py' -v`
for behavioral checks. Include the no-environment settings form, persistent
configuration, synthetic model/tokenization checks and secret redaction when
changing setup. Never use real user settings or credentials for these tests.
The package has twenty separately discoverable skills:
one coordinator and nineteen specialists. Shared references and templates live
under `skills/.shared/`; role-specific methods stay in the owning skill. Keep the
role directory and packaged discovery count aligned, and verify role loading and
actual handoffs separately from metadata discovery. Agent role instructions,
deterministic tool validation, runner qualification, and human acceptance are
separate evidence; preserve those distinctions when extending the package.

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

## Copilot catalog and portable components

The Codex catalog at `.agents/plugins/marketplace.json` owns plugin membership
and package paths. Copilot's `.github/plugin/marketplace.json` is derived from
that membership and each current package's `.codex-plugin/plugin.json` identity,
description, and version. After adding, removing, or updating a plugin, regenerate
and check the Copilot catalog:

```bash
python3 scripts/check_copilot_marketplace.py --write
python3 scripts/check_copilot_marketplace.py
```

The write command updates only the Copilot catalog after validating all portable
components. Keep each root `plugin.json` synchronized with its Codex overlay.
Skills live in `skills/<skill>/SKILL.md`. Packages with MCP servers also ship a
root `mcp.json` using the Agent Plugins 1.0 MCP schema, `stdio` transport, and
`${PLUGIN_ROOT}` paths; keep the server names, commands, and entrypoints aligned
with the Codex `.mcp.json`. Codex's `tool_timeout_sec` is client-specific and is
not copied into the portable configuration. Distribution validation retains
both formats. Copilot sources track the selected marketplace checkout, while
Codex's existing `git-subdir` release pins remain independent.

## Codex display metadata

A plugin has two display surfaces. Keep both useful:

- All catalog packages use root `plugin.json` with the Agent Plugins 1.0 schema
  and OpenAI presentation under `extensions.com.openai.interface`. Keep identity,
  version, and presentation synchronized with the Codex overlay. Portable
  `shortDescription` must contain at most 30 characters.
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
For Semantic Versioning and the standalone workflow plugins, retain the catalog-local source unless a replacement
passes native pre-install discovery. With `git-subdir`, the current Codex host
returns a cross-repository placeholder before installation; adding skill metadata
does not fix that listing. A local source in a Git-backed marketplace resolves
inside the downloaded marketplace checkout, not a developer-specific directory.
Catalog installs therefore follow the package on the marketplace branch; keep
that package at the intended published version.

Validate `plugin/read` in a fresh Codex home **before installing**: the plugin
should have a display name, descriptions, prompts, existing artwork paths, and
the package's expected skills while `installed` is false: three for Semantic
Versioning and one per standalone workflow plugin. Verify installation and published
package identity separately.

Validate the packaged files and inspect Codex's `skills/list` response after an
isolated installation: the returned `interface` should include the intended
names, descriptions, and prompts. This checks what Codex loads; visual rendering
requires a separate app check.

## Validation

Run from the repository root:

```bash
python3 - <<'PY'
import json
import subprocess

with open(".agents/plugins/marketplace.json", encoding="utf-8") as stream:
    entries = json.load(stream)["plugins"]
for entry in entries:
    package = entry["source"]["path"]
    subprocess.run(["python3", "scripts/check_plugin.py", package, "--layout", "source"], check=True)
    subprocess.run(["python3", "scripts/check_distribution_bundle.py", package], check=True)
PY
python3 scripts/check_semantic_versioning.py
python3 scripts/check_routes.py .
python3 scripts/check_route_receipts.py \
  tests/fixtures/blind-route-observations-v1.3.1.json \
  --root . --allow-subset --allow-historical-annotations
python3 plugins/conversation-visuals/mcp/server.py --self-test
python3 plugins/icloud-mail/mcp/server.py --self-test
python3 scripts/check_marketplace.py .
python3 scripts/check_copilot_marketplace.py .
python3 scripts/check_installed_parity.py <prepared-plugin-source> <installed-cache-version-dir>
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

When the Codex Plugin Creator skill is available, also run its manifest validator and validate every changed skill with Skill Creator. Release candidates must pass the pinned HOL scanner workflow with no high or critical finding.

For a portable package, inspect the final archive to confirm root `plugin.json`,
the Codex overlay, the expected skill, and all referenced assets and supporting
files are present. Create one archive per plugin outside the directory being
packaged. Plugin Creator account saves are private account/workspace objects;
they do not publish a GitHub release or submit a public directory listing.

Record exact commands, results, revision, and any checks not run. Static route-contract validation must never be described as proof of interactive agent behavior.

## Pull requests and releases

Use focused Conventional Commits. Explain the problem, user impact, design choice, validation evidence, compatibility, and residual risk in the pull request. Version plugin releases with Semantic Versioning based on the public plugin contract. The marketplace has an independent version and uses stable `marketplace-vX.Y.Z` tags; contained plugin tags and releases do not represent marketplace releases. Only maintainers publish tags and releases.

Follow the current Codex marketplace workflow for the selected source declaration. Keep the package manifest, catalog entry, displayed stable version, and validation expectations coherent in every plugin release. Create the annotated plugin version tag from the exact validated merge commit, and verify the installed plugin in a fresh task before closing the release. Publishing a stable plugin GitHub Release automatically validates that release's source commit, creates the next `marketplace-vX.Y.Z` snapshot tag at that commit, and publishes it as GitHub Latest. If plugin releases overlap, only the newest stable release creates a new snapshot. A retry may finish an existing snapshot owned by its exact plugin release and source commit, while keeping that stale recovery from becoming GitHub Latest. Manual and automatic marketplace publishers share a publication queue. Automatic snapshots reserve versions from existing tags, reuse their own exact source tag on retry, and avoid moving GitHub Latest backward when recovering an older publication. To publish a marketplace-only release, create and push an annotated `marketplace-vX.Y.Z` tag from the exact validated merge commit; the marketplace release workflow runs the full repository validation before publishing it as GitHub Latest.
