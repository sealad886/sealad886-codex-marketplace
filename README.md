# Agent plugins by sealad886

[![Validate plugins](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/validate.yml)
[![HOL Plugin Scanner](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/hol-plugin-scanner.yml/badge.svg)](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/hol-plugin-scanner.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Tools for planning and shipping software, reviewing and consolidating Git work, simplifying code, researching the web, managing releases and iCloud email, browsing the web with Camofox, working with visuals, and optimizing MLX on Apple Silicon. Install the plugins you need; each works independently.

Available as a plugin marketplace for **Codex** and **GitHub Copilot**. All
packages expose portable Agent Plugins 1.0 manifests, with Codex presentation
metadata retained separately.

## Plugins

### [Camofox Browser](plugins/camofox-mcp/README.md)

Give agents a full headless browser with 46 MCP tools, managed server and browser setup, isolated sessions, screenshots, structured extraction, uploads, and downloads. Runs locally on macOS and Linux, or connects to an existing Camofox service.

**Release:** `0.1.1` · [Setup and usage](plugins/camofox-mcp/README.md) · [Runtime source](https://github.com/sealad886/camofox-mcp)

### [Project Delivery](plugins/project-delivery/README.md)

Take work from requirements through implementation, testing, review, and release. Project Delivery adapts the workflow to the size and risk of the task, keeps decisions grounded in the repository, and tracks what has actually been verified.

**Stable release:** `1.5.0` · [Guide and usage](plugins/project-delivery/README.md)

### [Semantic Versioning](plugins/semantic-versioning/README.md)

Keep version decisions aligned with code changes. Assess release impact, respect the project's existing version owner, and configure or verify release automation. Includes guidance across ten ecosystem families, read-only inspection tools, and GitHub Actions examples for common packaging workflows.

**Release:** `0.1.1` · [Guide and examples](plugins/semantic-versioning/README.md)

### [MLX Optimizer](plugins/mlx-optimizer/README.md)

Audit, benchmark, and optimize Python MLX code on Apple Silicon. Find performance bottlenecks, compare changes against measured baselines, and check numerical accuracy alongside speed and memory use.

**Stable release:** `0.2.5` · [Guide and requirements](plugins/mlx-optimizer/README.md)

### [Conversation Visuals](plugins/conversation-visuals/README.md)

Bring useful images, diagrams, and generated visuals into supported Codex and ChatGPT conversations. Choose visuals that help explain the subject, with source attribution and clear disclosure of generated content.

**Version:** `0.1.2` · [Guide and supported capabilities](plugins/conversation-visuals/README.md)

### [iCloud Mail](plugins/icloud-mail/README.md)

Connect iCloud Mail through one temporary setup page on your Mac, with an Apple app-specific password stored in macOS Keychain. Search, read, organize, draft, and send mail directly on iCloud, including attachments, replies, and forwarding. No local email repository, cache, search index, or background sync.

**Release:** `0.4.0` (optional self-hosted read-only remote access; hosting required) · [Setup and usage](plugins/icloud-mail/README.md)

### [Build Multi-target Tauri Apps](plugins/build-multi-target-tauri-apps/README.md)

Build, debug, test and prepare Tauri 2 apps across Windows, Linux, macOS, iOS and Android. Eight skills cover architecture, frontend UX, native integration, IPC security, device QA, performance and distribution, grounded in dated primary-source research.

**Initial package:** `0.1.0` · [Guide and target requirements](plugins/build-multi-target-tauri-apps/README.md)

### [Iterating PR Bot Fixes](plugins/iterating-pr-bot-fixes/README.md)

Drive a GitHub pull request through bounded review and fix rounds, diagnose failed checks, and refresh evidence after head, base, or merge-queue changes. Retain explicit reviewer outcomes, current-revision merge gates, and resumable cleanup.

**Release:** `0.2.1` · [Guide and review workflow](plugins/iterating-pr-bot-fixes/README.md)

### [Repository Consolidation](plugins/repo-consolidation/README.md)

Reconcile useful outcomes from scattered branches, worktrees, stashes, and unfinished changes onto the verified default branch. Choose canonical implementations, adapt missing behavior, and prune verified obsolete code, artifacts and residue through focused PRs in series.

**Release:** `0.3.0` · [Guide and reconciliation rules](plugins/repo-consolidation/README.md)

### [Conventional Commit](plugins/conventional-commit/README.md)

Turn selected changes into coherent Conventional Commits whose types and scopes fit the behavior and repository automation. Includes a constrained staged-hunk procedure, excluded-work preservation, signing/hooks, and explicit cleanup controls.

**Release:** `0.2.0` · [Guide and commit safety](plugins/conventional-commit/README.md)

### [Simplify Code](plugins/simplify-code/README.md)

Remove unnecessary layers, simplify state and control flow, and migrate proven callers to their canonical owner. Preserve required behavior, resource lifetimes, evaluation order, and unresolved dynamic or external consumers.

**Release:** `0.2.0` · [Guide and refactoring examples](plugins/simplify-code/README.md)

### [Adversarial Audit](plugins/adversarial-audit/README.md)

Investigate system risks through reproducible evidence, bounded failure/recovery experiments, and independent or property-based comparisons. Keep finding validity separate from repair status and drive authorized fixes through verification.

**Release:** `0.2.0` · [Guide and evidence ledger](plugins/adversarial-audit/README.md)

### [Web Research](plugins/web-research/README.md)

Research decisions with cited evidence, comparable quantities, and explicit uncertainty. Compare options and sensitivity, refresh an existing brief claim by claim, and check quantitative claims while separating reported figures from calculations.

**Release:** `0.2.0` · [Guide and source evaluation](plugins/web-research/README.md)

### [Repository Guidance](plugins/repository-guidance/README.md)

Create or audit repository-specific agent instructions using evidence from the
target checkout. Adapt engineering conventions to its actual package boundaries,
state ownership, contracts, verification commands, and delivery policies.

**Release:** `0.1.0` · [Guide and adaptation method](plugins/repository-guidance/README.md)

### [Local Translation](plugins/local-translation/README.md)

Coordinate expert translation agents with queries, terminology decisions,
independent bilingual revision, correction rounds, and delivery evidence. The
bundled tool drafts text through a configured local Index-Translate runner.
Host agent models and final human acceptance are separate from local inference.

**Version:** `0.1.0` · [Setup and supported formats](plugins/local-translation/README.md)

## Install

### Codex

Add the marketplace once:

```bash
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
```

Marketplace releases use their own `marketplace-vX.Y.Z` tags and GitHub releases.
Plugin tags such as `icloud-mail-v0.2.0` are independent and do not identify a
marketplace release. To install a pinned marketplace version, use its
`marketplace-vX.Y.Z` tag as the `--ref`.

Then install any plugin:

```bash
codex plugin add project-delivery@sealad886-codex-marketplace
codex plugin add semantic-versioning@sealad886-codex-marketplace
codex plugin add mlx-optimizer@sealad886-codex-marketplace
codex plugin add conversation-visuals@sealad886-codex-marketplace
codex plugin add icloud-mail@sealad886-codex-marketplace
codex plugin add build-multi-target-tauri-apps@sealad886-codex-marketplace
codex plugin add iterating-pr-bot-fixes@sealad886-codex-marketplace
codex plugin add repo-consolidation@sealad886-codex-marketplace
codex plugin add conventional-commit@sealad886-codex-marketplace
codex plugin add simplify-code@sealad886-codex-marketplace
codex plugin add adversarial-audit@sealad886-codex-marketplace
codex plugin add web-research@sealad886-codex-marketplace
codex plugin add repository-guidance@sealad886-codex-marketplace
codex plugin add camofox-mcp@sealad886-codex-marketplace
```

To refresh an existing marketplace, run `codex plugin marketplace upgrade sealad886-codex-marketplace`. Start a fresh Codex task after installation. Each plugin's guide covers its requirements and usage.

The single-skill workflow plugins contain instructions without requiring a local
executor. Marketplace installation makes them available in the local client;
cloud use requires a separately available account copy. Each task still needs
the relevant tools, repository access, and authentication. Invoke each skill as
`$<plugin-name>:<skill-name>`; these plugins use the same name for both parts.

### GitHub Copilot

Register the marketplace, then install any plugin by its name from the list above:

```bash
copilot plugin marketplace add sealad886/sealad886-codex-marketplace
copilot plugin marketplace browse sealad886-codex-marketplace
copilot plugin install project-delivery@sealad886-codex-marketplace
```

Refresh the catalog with
`copilot plugin marketplace update sealad886-codex-marketplace`. For a pinned
marketplace snapshot, register
`sealad886/sealad886-codex-marketplace#marketplace-vX.Y.Z` instead. For local
development, run `copilot plugin marketplace add .` from this checkout.

The Copilot catalog uses repository-relative sources: each plugin comes from the
selected marketplace checkout. Codex retains its own catalog and release pins.
Copilot discovers skills under `skills/` and MCP servers through root `mcp.json`.
Client-specific features still require the relevant host tools; for example,
Conversation Visuals' Codex panels and image generation need a supported host,
and iCloud Mail's local setup requires macOS Keychain. See each plugin's guide
for its runtime and authentication requirements.

The catalog follows GitHub's
[marketplace format](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
and [plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference).

## Contributing and validation

See [CONTRIBUTING.md](CONTRIBUTING.md) for development, validation commands, and release requirements. Plugin source lives under `plugins/`; the catalogs are [Codex marketplace.json](.agents/plugins/marketplace.json) and [Copilot marketplace.json](.github/plugin/marketplace.json). CI checks catalog parity, package structure, distribution contents, regression tests, and security scans. Semantic Versioning also includes native example builds and workflow validation.

[Changelog](CHANGELOG.md) · [Report a security issue](SECURITY.md) · [Get support](SUPPORT.md)

## Support this work

[Sponsor on GitHub](https://github.com/sponsors/sealad886) or [buy me a coffee](https://www.buymeacoffee.com/sealad886).

Maintained by sealad886. [MIT licensed](LICENSE).
