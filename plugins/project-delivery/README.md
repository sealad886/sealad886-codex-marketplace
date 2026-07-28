<p align="center">
  <img src="assets/project-delivery-logo.png" width="160" alt="Project Delivery compass and route logo">
</p>

# Project Delivery

[![Validate plugin](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/validate.yml)
[![HOL Plugin Scanner](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/hol-plugin-scanner.yml/badge.svg)](https://github.com/sealad886/sealad886-codex-marketplace/actions/workflows/hol-plugin-scanner.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Project Delivery is a self-contained Codex plugin that turns an incomplete idea or bounded request into a traceable, production-oriented change. It provides one repository-grounded, risk-scaled evidence spine from outcome through requirements, design, planning, implementation, verification, documentation, independent review, security and operational readiness, release, and learning.

It is published through the [sealad886 Codex Marketplace](https://github.com/sealad886/sealad886-codex-marketplace). The marketplace ID is `sealad886-codex-marketplace`; the plugin ID, display name, skill selectors, and package boundary remain `project-delivery`.

It is designed to become the sole generic project-management and software-delivery workflow after its adoption gates pass. It does not replace authenticated connectors, CI systems, platform tooling, security scanners, deployment providers, observability systems, or other specialist evidence sources.

## Why it is different

- **Repository first:** inspect instructions, code, tests, history, canonical documentation, CI/release configuration, and prior decisions before inventing new state.
- **Risk scaled:** preserve the same gates for a one-file fix and a multi-release initiative, but compress them when evidence supports low risk.
- **Evidence bound:** tie claims to exact revisions, environments, commands, artifacts, provider state, and actual results; record failures and checks not run.
- **Traceable:** connect outcomes, requirements, acceptance, decisions, risks, work, tests, findings, and release disposition.
- **Authority safe:** planning does not authorize edits; preparation does not authorize merge, publish, deploy, external writes, communication, or risk acceptance.
- **Provider neutral:** optional tools deepen evidence or perform authorized actions, while the core still produces useful plans, drafts, mappings, and receipts without them.
- **Independently implemented:** no runtime code, prompt, hook, manifest, app/MCP configuration, executable, or asset from another delivery plugin is required or re-exported.

## Canonical lifecycle

```text
Context → Requirements → Solution Design → Delivery Plan ↔ Coordination
        → Implementation → Quality → Documentation → Review / Security / Operations
        → Release → Retrospective
```

Start with `project-delivery:delivery-orchestrator` for end-to-end, incomplete, or mixed requests. Invoke a lifecycle skill directly when the target and authority are already bounded.

The lifecycle is a logical evidence and gate model, not a command that blindly invokes every skill in one total order. Required capability owners, conditional branches, valid existing evidence, safety precedence, and controller returns determine the actual route.

| Work shape | Default depth | Typical result |
|---|---|---|
| Small, low-risk change | Compact context and acceptance, design delta when needed, short plan, targeted verification, proportional review/release checks | One coherent PR with exact evidence and rollback notes |
| Medium feature or refactor | Full requirements, design, WBS, implementation, test strategy, docs, independent review, security/operations, release gate | One or a few traceable PRs |
| Large initiative | ADRs, RAID, milestones, critical path, bounded delegation, multi-PR/release slices, staged rollout, observation and learning | Incremental delivery with explicit integration and release gates |
| Review-only or release-only | Recover exact scope and missing evidence, apply only the relevant lenses | Findings or gate decision without unauthorized edits |
| Legacy-workflow migration | Instruction/state inventory, rollback capture, one-at-a-time disablement, fresh-task smoke receipts | Evidence-based replacement without deleting specialist access |

## Quick start prompts

Use the orchestrator for a full lifecycle:

```text
Use $project-delivery:delivery-orchestrator to deliver this request end to end. Inspect the current
repository, recover existing decisions and conventions, classify scale and risk,
use only the minimum sufficient lifecycle, keep facts/requirements/assumptions/
decisions/questions separate, and report actual evidence plus residual risk.

Request: <describe the outcome>
```

Use a bounded skill directly:

```text
Use $project-delivery:requirements-acceptance to turn this brief into testable requirements,
acceptance criteria, edge cases, non-functional requirements, and traceability.
```

```text
Use $project-delivery:review-audit to review this exact diff without modifying it. Pin the base and
head, report located evidence-backed findings, and state release blockers and
residual risk.
```

```text
Use $project-delivery:release-change to prepare this completed change for release. Recover missing
test, documentation, review, and security evidence; do not merge, tag, publish, or
deploy unless that action is separately authorized.
```

## Skills

| Skill | Canonical responsibility |
|---|---|
| `delivery-orchestrator` | Classify authority, scale, risk, lifecycle state, routing depth, delegation, and migration/decommission work |
| `project-context` | Refine the problem, outcome, value, scope, constraints, success, readiness, and repository context |
| `requirements-acceptance` | Produce testable requirements, acceptance criteria, edge cases, NFRs, and traceability |
| `solution-design` | Design current/proposed state, contracts, alternatives, compatibility, migration, rollback, and ADRs |
| `delivery-planning` | Build WBS, milestones, dependencies, critical path, ownership, estimates, RAID, and PR/release slices |
| `delivery-coordination` | Reconcile systems of record, meetings, status, exact external targets, authority, and readback receipts |
| `implementation-execution` | Implement an approved slice in canonical repository paths while preserving unrelated work |
| `testing-quality` | Select, run, and report risk-based tests, static checks, CI evidence, performance/security validation, and failure triage |
| `documentation-knowledge` | Maintain canonical user, developer, operator, architecture, migration, status, and release knowledge |
| `review-audit` | Independently review designs, plans, diffs, PRs, or releases with reproducible findings and governed closure |
| `security-operations` | Assess threat, privacy, dependency, reliability, observability, support, recovery, and operational readiness |
| `release-change` | Prepare and, only when authorized, execute integration, CI/CD, version, rollout, rollback, and post-release verification |
| `retrospective-improvement` | Capture outcomes, root causes, debt, decisions, bounded follow-up, and measurable process improvements |

Installable shared conventions, templates, the closed receipt schema, and canonical intent profiles live under [`skills/.shared/`](skills/.shared/). [`route-profiles-v1.json`](skills/.shared/route-profiles-v1.json) is the runtime semantic source for common routes; it gives the orchestrator profile ownership, evidence-resolved allowed taxonomy, gate, and stop-condition data without depending on repository-only tests. Keeping runtime references inside the manifest-declared skill tree makes the standalone plugin self-contained without exposing a fourteenth skill.

## Artifact and evidence model

Project Delivery updates the repository's canonical artifacts instead of creating a branded process tree. When the repository has no format, it offers proportional templates for:

- project briefs, requirements, acceptance criteria, solution designs, and ADRs;
- WBS, milestones, RAID, critical path, PR/release slices, status, and coordination receipts;
- risk-to-test strategies and revision/environment-bound results;
- review and security findings with severity, priority, evidence, closure, release treatment, and residual risk;
- release units, approvals, migrations, flags, rollout, rollback, observability, and post-release outcomes; and
- retrospectives, technical debt, follow-up work, and live route receipts.

Recommended traceability:

```text
Outcome → REQ → AC → DESIGN/ADR → WI/PR → TEST → FIND → RELEASE
REQ/AC → RISK → mitigation WI → TEST/FIND → RELEASE disposition
DEC/ADR → affected REQ/WI/TEST → RELEASE disposition
```

## Install from the hosted marketplace

Add the sealad886 marketplace and install the immutable stable package:

```bash
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add project-delivery@sealad886-codex-marketplace
```

Start a fresh Codex task, then invoke `$project-delivery:delivery-orchestrator` for an end-to-end request or a bounded Project Delivery skill directly. The marketplace currently resolves Project Delivery to the validated `v1.4.0` tag.

If Codex still has a former `project-delivery@project-delivery` or `project-delivery@andrew-cox-codex-marketplace` selector, follow the add-first migration in the [marketplace README](https://github.com/sealad886/sealad886-codex-marketplace#migrate-a-former-marketplace-name). Verify the new selector before removing former plugin and marketplace entries.

## Local development install

Project Delivery is a standalone plugin with a deliberately clean package boundary. Clone the development repository outside the personal plugin destination:

```bash
git clone https://github.com/sealad886/sealad886-codex-marketplace.git ~/src/sealad886-codex-marketplace
cd ~/src/sealad886-codex-marketplace
python3 scripts/check_distribution_bundle.py plugins/project-delivery \
  --output ~/plugins/project-delivery
```

For later iterations, rerun the materializer with `--replace`. It replaces only an exact clean Project Delivery distribution outside any Git checkout or Python environment, and refuses missing, extra, forbidden, executable, symlinked, or unsupported entries. A failed swap restores the prior clean distribution or retains its backup path for recovery. This separation is required because Codex recursively copies a local source directory and does not treat `.codexignore` as a packaging filter.

### Upgrade from the 1.3.x checkout layout

Version 1.3.x instructed users to clone the development repository directly into `~/plugins/project-delivery`. Preserve that checkout intact: record its plugin/source/revision/status identity, move it to a separate rollback location such as `~/src/project-delivery-1.3-backup`, verify the moved checkout, and materialize the new nested package into the now-vacant personal destination. Do not use `--replace` against the old checkout.

Then use Plugin Creator's supported cachebuster/reinstall flow, read back `project-delivery@personal`, compare the prepared source with the versioned installed cache, and verify selectors, icons, routing, and a bounded repository canary from a fresh task. Keep both sources until a forward-and-back recovery through the recorded control plane has passed; retained cache bytes alone are not rollback proof. The repository's [migration guide](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/references/migration-and-decommission.md) defines the full evidence record.

Then ask Codex's system Plugin Creator skill to validate and install the prepared package:

```text
Use $plugin-creator to validate, register, cachebust, and install the local plugin at
~/plugins/project-delivery. Follow the supported local-source registration and
cache-refresh workflow, do not hand-edit Codex configuration, and report the
installed plugin version and cache identity.
```

Start a new Codex task after installation and invoke `$project-delivery:delivery-orchestrator`. The installed bundle contains all 13 skills and their presentation metadata. Codex applies a global initial skill-metadata budget, so a crowded task may omit otherwise valid skills from its initial model-visible list. The orchestrator is instructed to resolve each selected Project Delivery specialist from its installed sibling path and block truthfully if the file is actually unavailable. Disabling superseded or unused workflow plugins after their canaries pass may improve initial-list visibility; do not rename skills to game ordering.

See OpenAI's [Build skills](https://learn.chatgpt.com/docs/build-skills.md) documentation for progressive disclosure, explicit invocation, and the initial-list budget.

For local development, edit the canonical package under `plugins/project-delivery/`, rerun the validated materializer, and ask `$plugin-creator` to run its supported cachebuster and reinstall workflow against the prepared personal-plugin folder. Do not point Codex at the development checkout root or edit product-managed installation state by hand.

Git-backed marketplaces should use `git-subdir` with the repository path `plugins/project-delivery` and pin an immutable release commit. This keeps repository `.git`, CI, tests, audit records, and development environments outside the installed payload.

See OpenAI's [Build plugins](https://learn.chatgpt.com/docs/build-plugins) guide for the current Codex manifest, component, and local testing contract.

## Validation

From a source checkout, the repository's dependency-free checks use only Python's standard library:

```bash
python3 scripts/check_plugin.py plugins/project-delivery --layout source
python3 scripts/check_routes.py .
python3 scripts/check_route_receipts.py tests/fixtures/blind-route-observations-v1.3.1.json --root . --allow-subset --allow-historical-annotations
python3 scripts/check_distribution_bundle.py plugins/project-delivery
python3 scripts/check_marketplace.py .
python3 scripts/check_installed_parity.py <prepared-plugin-source> <installed-cache-version-dir>
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

`tests/route-contracts.json` contains 24 schema-v3 machine-readable canary contracts: the original 17 prompts, four explicit platform-claim variants, a direct retrospective request, an authorized release-execution request, and a reversible workflow-decommission request. The installed [`route-profiles-v1.json`](skills/.shared/route-profiles-v1.json) contains the corresponding runtime semantics without the hidden canary prompts. Runtime `allowed_*` values permit truthful evidence-resolved classification, while maintainer contracts keep narrower `accepted_*` tolerances for projectless blind canaries. Validation requires semantic parity for ownership, gates, artifacts, evidence, stop conditions, and accepted-value subsets of the runtime policy. Passing those static checks proves that policy data is complete, references disjoint real capability owners, covers the taxonomy, declares substantive conditional triggers, acyclic entry precedence, two-sided occurrence-aware controller entry/return rules, and forbidden legacy runtime dependencies. It does **not** prove that a trigger applies, which skills a fresh agent selected, or that delivery work ran. The committed v1.3.1 fixture preserves genuinely blind route choices, but its schema-v2 taxonomy, rationales, and conditional dispositions are explicitly post-hoc and accepted only with the dedicated historical flag; it establishes historical route-shape compatibility, not current-policy conformance or candidate behavior. Fresh route-policy claims require the closed schema-v3 observation plus a coordinator-generated canonical task prompt, exact raw-byte and launch attestation, and independent digest-linked grade. The route task freezes taxonomy, trigger/outcome dispositions, route, effects, instruction closure, evidence, and structured gaps before comparison; loaded specialists equal only the present route union; delivery remains not run. Exact total-order equality is intentionally not a conformance rule.

The distribution check validates the exact 64-file canonical package boundary, including all five shared runtime resources, and can materialize that byte-defined payload into a separate personal-plugin folder. It rejects undeclared files, symlinks, unsupported file types, source-only paths, and broken runtime references. Installed-cache parity and fresh-task behavior remain separate release gates.

Release validation also includes Plugin Creator validation, Skill Creator validation for all 13 skills, exact prepared-source/cache comparison, an isolated install/rollback rehearsal, the pinned HOL scanner, fresh-task canaries, and independent review. Current evidence and limitations are recorded in the [validation report](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/references/validation-report.md).

## Trust, privacy, and dependencies

Project Delivery bundles no MCP server, app, hook, telemetry, network service, credential, binary, package dependency, or automatic external write. Its Python validation scripts use only the standard library. It never needs another workflow plugin to operate.

Repository instructions and user authority remain controlling. External issue trackers, source hosts, document stores, communication tools, calendars, CI systems, deployment platforms, security tools, and memory systems are optional adapters used only when available, relevant, and authorized. Secrets and personal data must not be copied into delivery artifacts or public evidence.

See [SECURITY.md](SECURITY.md) for private vulnerability reporting and the [support policy](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/SUPPORT.md) for support boundaries.

## Migration and replacement

Project Delivery is intended to replace generic project-management and software-delivery workflow authority, including fragmented planning, implementation, testing, documentation, review, security-gate, release, and retrospective entry points. Adoption is evidence-based:

1. neutralize active instructions that mandate a legacy workflow;
2. preserve historical provenance without leaving imperative legacy calls active;
3. inventory installed IDs, versions, configuration locations, and supported reinstall sources without secrets;
4. run representative small and medium canaries;
5. disable one superseded generic plugin at a time and start a fresh task;
6. confirm packaged files, explicit and orchestrated loading, semantic routing, artifacts, stable plugin state, and absence of legacy invocation/runtime requests; and
7. uninstall only after an observation period and explicit user confirmation.

Specialist platform, provider, security, CI, deployment, and observability tools may remain because they supply access or evidence rather than competing lifecycle authority. The [detailed migration map](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/references/migration-and-decommission.md) remains with the standalone plugin source.

## Project governance

- [Marketplace](https://github.com/sealad886/sealad886-codex-marketplace)
- [Contributing](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Support](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/SUPPORT.md)
- [Changelog](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/CHANGELOG.md)
- [Design brief](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/references/design-brief.md)
- [Environment and capability audit](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/references/environment-audit.md)
- [Research sources](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/references/research-sources.md)
- [Validation report](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/references/validation-report.md)

Project Delivery is maintained by Andrew Cox and licensed under the [MIT License](LICENSE). Copyright © 2026 Andrew Cox.
