# Adaptation lenses

Use only the rows relevant to the target. A missing concern is not a reason to
introduce a new subsystem. Record evidence and an adoption disposition before
turning a question into a rule.

| Concern | Inspect locally | Guidance to derive |
| --- | --- | --- |
| Instruction scope | Root/nested instruction files and client configuration | Reading order, canonical owner, scoped exceptions, supported clients |
| Code ownership | Package exports, imports, dependency rules and representative callers | Responsibility by module and allowed dependency direction |
| Cross-platform behavior | Platform entry points, shared logic and integration tests | Shared versus platform-owned code; feature wiring and platform checks |
| Development environment | Manifests, lockfiles, task runners and contribution guide | Managed environment, real commands, working directories and data effects |
| State ownership | Cache, persistence, stores and event handlers | Which layer owns each datum; durable versus temporary state; reconciliation |
| External contracts | Schemas, validators, client versions and contract tests | Validation at trust boundaries and locally required compatibility behavior |
| Data writes | Migrations, transactions, identifiers and access checks | Actual integrity, authorization, migration and recovery requirements |
| UI and copy | Design system, components, accessibility and translation contracts | Existing primitives, meaningful help text and supported-language checks |
| Tests | Existing test placement, fixtures, CI and side effects | Canonical test layer per behavior; meaningful regressions; isolated defaults |
| Delivery | Branch/commit policy, release configuration, templates and approvals | Scope control, verified completion, version owner and external-action authority |

## Decisions requiring local evidence

Do not infer that all repositories need web/mobile/desktop layers, server-state
caches, route adapters, or a relational database. If a similar boundary exists,
describe its actual owner and mechanism rather than importing a framework name.

Choose database integrity and index strategies from the target’s database engine,
operations constraints, and policies. A source project’s ban on foreign keys or
particular concurrent-index workflow cannot establish a rule elsewhere.

Preserve compatibility only where the target contract requires it. Do not add
shims or drop supported clients because of an external example. Verify unknown
values, response validation, and malformed-input behavior at the appropriate
boundary when those concerns apply.

Treat deterministic test fixtures and fakes as tools for isolating behavior.
Document real-account or installed-agent tests separately, including their actual
authorization and opt-in conditions. Do not run them to fill a checklist.

Derive release impact from the target’s versioning contract and actual change.
Do not apply a universal patch default, assume a tag publishes a package, or infer
release authority from permission to edit instructions.

## Worked example: this marketplace

This example illustrates evidence mapping for
`sealad886/sealad886-codex-marketplace`; recheck the files at invocation time.
It is not a set of paths to impose on other repositories.

| Candidate purpose | Local evidence | Disposition and resulting guidance |
| --- | --- | --- |
| Make ownership explicit | `CONTRIBUTING.md`, `plugins/<plugin-id>/README.md` | **Adapt:** each package owns its skills/resources; shared catalog and validation logic remains at marketplace level. |
| Keep generated outputs aligned | `AGENTS.md`, `scripts/check_copilot_marketplace.py` | **Adapt:** `.agents/plugins/marketplace.json` owns membership; regenerate `.github/plugin/marketplace.json` using the existing command. |
| Preserve public contracts | `AGENTS.md`, `scripts/check_plugin.py` | **Adapt:** retain paired portable `plugin.json` and `.codex-plugin/plugin.json` identities, versions and OpenAI presentation. |
| Use actual managed commands | `.venv/`, `CONTRIBUTING.md` | **Adapt:** run package, marketplace and distribution checks through the existing project Python environment; disable bytecode writes during validation. |
| Verify each supported surface | `AGENTS.md`, `CONTRIBUTING.md` | **Adapt:** validate both catalogs and isolated Codex/Copilot discovery/install when available; report versions and omitted runtime evidence. |
| Make delivery status honest | `CONTRIBUTING.md`, `.github/workflows/` | **Adopt:** tie release claims to verified artifacts and observed workflow results; preserve the user’s required publish authority. |
| Transfer app-specific architecture | No matching Multica app/server layers | **Not applicable:** omit its pnpm, Go, UUID, workspace-route, database and UI implementation details. |

A report-only adaptation can identify these mappings without editing `AGENTS.md`.
An instruction-edit request can patch the canonical file while keeping the
marketplace’s existing dual-client contracts and approval boundaries intact.
