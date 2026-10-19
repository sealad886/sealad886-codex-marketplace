# Implementation plan: workflow plugin expansion

Approved design: [specification](../specs/2026-10-19-workflow-plugin-expansion-design.md).
Scope: six independent, instruction-only, one-skill plugins at 0.2.0.
Implementation, focused PR/merge, public/private publication and local refresh
were explicitly approved in chat. No new worktree or branch deletion is authorized.

## Execution rules

Use the existing task branch. Each package is a disjoint write scope; only the
primary agent edits root README/CHANGELOG and shared verification records.
Preserve plugin identity, current starter prompts and ordering, artwork,
license, scope, audience and unrelated metadata. Keep conditional detail in
references; do not add a runtime server, helper executable or sibling dependency.

Use the executing-plans control loop and bounded parallel package assignments.
Review specification compliance before quality/authority review. Fix material
findings before integration. For prose changes use meaningful scenarios and
existing schema/link/closure checks, not new prose-pinning tests. The new Git
recipe requires real disposable-fixture evidence before publication.

## Phase 1: Git workflow capabilities

1. PR evidence and recovery (low risk).
   - Files: `plugins/iterating-pr-bot-fixes/skills/iterating-pr-bot-fixes/references/ci-triage.md`,
     `references/revision-refresh.md`, existing `SKILL.md` and
     `templates/review-ledger.md` in that skill; package `README.md`,
     `plugin.json`, `.codex-plugin/plugin.json`.
   - Add CI diagnosis and revision/queue recovery, preserve review-source
     retirement/unavailability and integration gates, bump to 0.2.0.
   - Acceptance: provider failure, stale green check, H1/H2 review drift, and
     post-merge cleanup failure produce the correct bounded next action.
   - Dependencies: approved design only.
2. Consolidation dependencies and recoverability (medium risk).
   - Files: `plugins/repo-consolidation/skills/repo-consolidation/references/overlap-and-dependencies.md`,
     `references/preservation-and-restore.md`, existing `SKILL.md` and
     `templates/consolidation-ledger.md`; package README and both manifests.
   - Add serial overlap/prerequisite planning and recovery-content verification;
     update owning routes/templates and bump to 0.2.0.
   - Acceptance: shared prerequisite once, intentionally reverted behavior,
     incomplete dirty-work preservation and unavailable LFS content.
   - Dependencies: approved design only.
3. Commit semantics and constrained staged subset (medium risk).
   - Files: `plugins/conventional-commit/skills/conventional-commit/references/message-decisions.md`,
     `references/partial-staging.md`, existing `references/staging-and-hooks.md`,
     `SKILL.md`, `templates/commit-plan.md`; package README and both manifests.
   - Add automation-aware message decisions without release authority. Define
     exact applicability, preservation checks and failure handoff for a subset
     of already-staged work; do not promise arbitrary index reconciliation.
   - Before finalizing commands, create disposable fixtures and a behavioral
     checker for committed content, real index semantic entries and working bytes.
     Observe a naive whole-index commit violate the selection requirement, then
     verify the constrained procedure, empty selection, hook effects and a
     pre-commit signing failure. Do not add tests that inspect Markdown text.
   - Bump to 0.2.0 after the documented procedure has actual evidence.
   - Dependencies: approved design; fixture evidence precedes procedure acceptance.

## Phase 2: refactoring, auditing and research capabilities

4. Simplification workflows (low risk).
   - Files: `plugins/simplify-code/skills/simplify-code/references/state-and-control-flow.md`,
     `references/mechanical-migrations.md`, optional
     `templates/refactor-evidence.md`, existing `SKILL.md`; README and manifests.
   - Add state/control-flow and cohort migration guidance, route conditionally,
     and bump to 0.2.0.
   - Acceptance: cancellation/cleanup, lazy evaluation, dynamic callers and
     mixed dirty-file preservation scenarios.
   - Dependencies: approved design only; independent of tasks 1–3.
5. Adversarial verification workflows (medium risk).
   - Files: `plugins/adversarial-audit/skills/adversarial-audit/references/failure-experiments.md`,
     `references/oracles-and-properties.md`, existing `SKILL.md` and
     `templates/audit-ledger.md`; README, relevant SECURITY guidance and manifests.
   - Add bounded failure/recovery and differential/property experiments without
     live mutation authority, keep one ledger, bump to 0.2.0.
   - Acceptance: accepted delivery contract, defective oracle, round-trip versus
     ground truth, and audit-only boundaries.
   - Dependencies: approved design only; independent of tasks 1–4.
6. Research decisions, refresh and quantitative evidence (low risk).
   - Files: `plugins/web-research/skills/web-research/references/decision-comparisons.md`,
     `references/research-refresh.md`, `references/quantitative-evidence.md`,
     `templates/decision-matrix.md`, `templates/claim-ledger.md`, existing
     `SKILL.md`; README and manifests.
   - Add decision sensitivity, claim-scoped refresh and quantitative appraisal;
     preserve unknowns/citations, conditional templates and bump to 0.2.0.
   - Acceptance: missing price, unavailable old source, changed software version,
     absolute/relative rate calculation with applicable population/timeframe.
   - Dependencies: approved design only; independent of tasks 1–5.

## Phase 3: integration and publication

7. Root documentation and package verification (low risk).
   - Files: root `README.md`, `CHANGELOG.md`, and
     `docs/releases/2026-10-19-workflow-plugin-expansion.md`.
   - Explain user-visible additions/version0.2.0; record actual scenario and
     fixture results, limits, package counts and archive hashes.
   - Run source/distribution/catalog and pinned upstream validation for all six;
     existing regression suite/CI checks; no changes to validators solely to
     assert new prose. Review exact diff and each package independently.
   - Dependencies: tasks 1–6 accepted.
8. Delivery and installed proof (medium risk; explicitly authorized).
   - Create/attach the focused PR, obtain explicit review outcomes and hosted
     checks, merge with exact-head condition, then verify merged source.
   - Build/verify ZIPs against the committed source; guarded-update the six
     existing private account plugins preserving current scope/audience.
   - Create signed version tags and stable releases from the validated merge;
     wait for the canonical marketplace publication workflow and verify its
     exact source and asset digests. Do not move old tags or GitHub Latest back.
   - In an isolated home, verify pre-install discovery, install, namespaced skill
     loading and byte parity. Refresh the user's six local marketplace copies
     through supported commands; preserve unrelated configuration and verify
     originals stay absent. Cloud eligibility is separate from cloud execution.
   - Retain source/recovery/official verification receipts; remove only exact
     task-owned diagnostic debris. Leave branches without deletion authority.
   - Dependencies: task 7 and review/CI gates.

## Progress

- [x] Design approved; 0.1.1 release/local refresh verified.
- [ ] Phase 1: Git workflows and disposable-fixture proof.
- [ ] Phase 2: simplification, auditing and research workflows.
- [ ] Phase 3: integration, review, publication and native consumption proof.
