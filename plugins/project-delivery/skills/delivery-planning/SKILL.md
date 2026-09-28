---
name: delivery-planning
description: Turn accepted requirements and design into a risk-scaled delivery plan with WBS, milestones, dependencies, critical path, ownership, estimates, RAID, communication, change control, and multi-PR/release slicing.
license: MIT
---

# Project Planning and Delivery Management

Read `../.shared/operating-model.md`; use the plan/RAID/status templates in `../.shared/artifact-templates.md`.

## When to invoke

Use before implementation, for roadmap or multi-PR decomposition, for replanning after scope/risk change, and for status/escalation. A small change can use a short ordered checklist.

## Inputs and evidence

Expect approved requirements/design or explicitly record what is provisional. Inspect code ownership, module boundaries, tests/CI, release cadence, branch conventions, team/reviewer/deployment constraints when discoverable, existing roadmap/issues, and working-tree state. Never invent people, capacity, dates, or commitments.

## Workflow

1. Build outcome-oriented `WI-*` work breakdown items small enough to own, review, test, and rollback. Keep implementation/tests/docs for the same outcome together when practical.
2. Apply the shared simplicity test: keep only work that changes acceptance, mitigates a demonstrated risk, or supplies required evidence. Remove speculative phases, optional infrastructure, redundant artifacts, and coordination with no current dependency.
3. Map dependencies and identify the critical path, integration points, write-set conflicts, external lead times, and decision gates.
4. Define `MS-*` milestones by demonstrable outcomes, not activity completion.
5. Assign confirmed owners or mark `unassigned`; distinguish accountable decision owner, implementer, reviewer, release/operator roles where relevant.
6. Estimate using the repository/team convention. State range/unit and confidence plus uncertainty drivers; do not present agent guesses as commitments.
7. Create/update the RAID log with probability/impact, response, trigger, owner, due/review point, state, and trace links. Connect each material `RISK-*` to its originating requirement or decision, mitigation/contingency work, verification or finding, and release disposition. Connect each `DEC-*`/ADR to affected requirements, work, tests, and release effects.
8. Decompose PRs so each is coherent, independently reviewable, integration-safe, and either value-delivering or a clear enabling slice. Specify base dependencies, contract/compatibility strategy, feature flags, evidence gates, merge order, and rollback boundaries.
9. For multi-release work, define incremental value, migration/coexistence/deprecation phases, release train/cutover gates, and follow-up removal.
10. Define communication/status cadence, stakeholder decisions, escalation triggers, scope baseline, and change-control process proportional to risk. When external systems are involved, map internal IDs to provider IDs, retain native status mappings, name sync ownership/cadence and exact destinations, define update triggers/reconciliation checkpoints/write authority, and escalate stale state.
11. Check DoR/DoD, requirement coverage, resource/conflict constraints, and stop conditions.

## Outputs and handoff

Ordered WBS, dependency/critical-path view, milestones, ownership, estimates/confidence, RAID, PR/release map, evidence waves, communication/change-control plan, external mapping/sync plan when applicable, and readiness status. Handoff to `delivery-coordination` for synchronization and `implementation-execution` one ready slice at a time.

## Completion evidence

Every in-scope requirement maps to work and evidence; sequence is dependency-safe; critical path and risks are visible; slices are reviewable/releasable; assumptions and unassigned ownership are explicit.

## Must not

- Fabricate owners, deadlines, capacity, velocity, or certainty.
- Use heavyweight ceremony for a trivial change or split PRs solely by technical layer when that creates broken intermediate states.
- Begin implementation, hide contingency, or let plan detail duplicate code that will immediately go stale.
- Add speculative work, milestones, or coordination that do not support current acceptance, risk, or evidence needs.
