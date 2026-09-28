---
name: delivery-orchestrator
description: Use first to route end-to-end, ambiguous, multi-phase, review, release, incident, or decommission work through the minimum sufficient project-delivery lifecycle when depth, state, or authority is unclear.
license: MIT
---

# Delivery Orchestrator

## Purpose

Own lifecycle routing and truthful state. Do not replace specialist work; invoke or apply the relevant skills and carry their artifacts forward.

Read `../.shared/operating-model.md` and `../.shared/route-profiles-v1.json` before routing. Use `../.shared/artifact-templates.md` when the repository has no canonical format.

After choosing a route, resolve each selected specialist's sibling directory and read its `SKILL.md` before applying it. Codex may shorten or omit entries from the initial skill list when many skills are installed; an omitted catalog entry is not proof that an installed specialist is unavailable. Treat a specialist as unavailable only after its installed file cannot be resolved or read, and record that as a routing blocker instead of silently absorbing its work.

## When to invoke

- An idea or request is incomplete, ambiguous, or solution-first.
- The user asks to plan and implement, deliver, ship, or manage a change end to end.
- Work spans multiple PRs, releases, systems, or teams.
- A design-only, review-only, documentation-only, or release-only request needs bounded routing.
- Risk/scale is unclear or the current lifecycle state must be recovered.
- A legacy workflow is being replaced, disabled, or decommissioned.

## Inputs and evidence

Inspect the user request; applicable `AGENTS.md`; repository status/history/branches/tags; README/contributing/architecture/security docs; code/tests; issue/PR templates; CI/release config; prior plans/ADRs/decisions; authorized external systems and local memory when accessible. Treat plugin and connector capabilities as optional adapters, never assumed facts.

## Workflow

1. Resolve authority and target: report-only, planning-only, design-only, change/build, review, release preparation, hotfix, or authorized release execution. Planning, review, and reporting do not authorize edits.
2. Classify scale and risk using the shared model. Record why.
3. Establish lifecycle state. Reuse valid existing artifacts; do not restart completed phases.
4. Apply the shared simplicity test before routing: use the minimum sufficient lifecycle and capability set, and reject extra ceremony, specialists, artifacts, or scope that lack a current requirement or demonstrated risk.
5. Select exactly one canonical profile from `../.shared/route-profiles-v1.json` by semantic intent, lifecycle state, and authority—not by exact wording. Apply its required owners, declared conditional owners, precedence, re-entry, final-controller, forbidden-owner, evidence, artifact, and stop rules.
   - Use the profile's preferred scale/risk when evidence is sparse. Use another normalized value only when it is in that installed profile's `allowed_scales` or `allowed_risks` and the repository or task evidence is stated. Maintainer canary contracts may accept a narrower subset for a fixed blind prompt; those test tolerances never constrain a real evidence-resolved route. Authority remains exact.
   - Required and conditional owners are disjoint. Never duplicate a required owner in `conditional_dispositions`. Record every declared conditional owner exactly once, whether activated, not applicable, deferred, blocked, or planned future.
   - Do not turn every global cross-cutting trigger into a profile conditional. Global guidance evaluates declared branches. A genuinely additional proportional owner may be introduced only from current evidence: record it as a complete conditional disposition when its trigger must be evaluated, or in `extra_capability_justifications` when it is directly selected without a conditional branch. Never duplicate a required, forbidden, or controller owner.
   - A conditional owner marked `activated` appears in the present route. Omitted conditional owners do not. Preserve controller entry and final return when the selected profile requires re-entry.
   - For `incident-hotfix`, incident urgency compresses artifacts but does not erase context, acceptance, or design reasoning: change-control entry → context → acceptance → design → security before implementation → implementation → quality → final recovery disposition. When both design and security owners are selected, design precedes security so threat and operational analysis evaluates the proposed repair rather than an unspecified change.
   - For `preview-migration-delivery`, security and migration risk must inform planning: solution design → security/operations → delivery planning → implementation.
   - For `meeting-follow-up` and `source-status-reconciliation`, `delivery-coordination` opens the canonical-source reconciliation. If a downstream requirements, context, planning, or documentation branch activates, coordination returns after those owners to reconcile native targets, authority, and receipts; a downstream draft is not a completed provider write.
   - Use `release-execution` only when the user has granted exact consequential release authority and the immutable artifact, environment, gates, rollback, and post-release evidence path are resolved. Preparation, review, or provider visibility does not qualify.
   - Use `workflow-decommission` when an active workflow, plugin, instruction set, hook, or configuration is being replaced and disabled or removed under explicit target authority; do not approximate it with ordinary feature delivery.
   - If no profile fits, use the lifecycle gates to construct the minimum safe route, state the unmatched intent as a profile gap, and justify every owner. Do not pretend an approximate profile is exact.
   - `workflow-decommission` remains an orchestrated composite: inventory active instructions, prompts, hooks/configuration, state, installed identities/versions, exact recovery sources, and legacy imperative artifacts → preserve rollback → disable one candidate at a time → start an independently resolved fresh task and run affected static/live smoke cases → re-enable on any routing or parity failure → uninstall only after observation gates and user-confirmed scope. Require ordinary fresh-task callbacks to start with `PROJECT_DELIVERY_VERSION=<expected-version>`; sealed JSON canaries use `plugin_identity.installed_version`. Do not edit consumer repositories or plugin configuration without corresponding authority.
6. Invoke `delivery-coordination` when external sources may contain requirements/decisions, after plans need synchronization, before status or meetings, after review findings need tracking, and during release communication/handoff. Detect provider/tool capability; core execution must still work without it.
7. Apply gates. Implementation may begin only when the Ready and necessary Design gates are satisfied. For low-risk work these may be concise and implicit in inspected evidence, but state that evidence.
8. Maintain a visible checklist/status for multi-stage work. Report blockers, decisions, evidence, and next transition.
9. End with the handoff contract and residual risk.

## Routing contract

Routes are capability and gate contracts, not brittle total-order scripts. Record the lead capability, required specialists, conditional branches, gate precedence, allowed re-entry, required final disposition after selected evidence, and why a conditional specialist was `activated`, `deferred`, `blocked`, `not-applicable`, or `planned-future`.

For a machine-comparable or cross-agent route receipt, use the canonical installed profile, the normalized scale/risk/authority values and conditional-state vocabulary from the shared operating model, and the exact closed envelope in `../.shared/live-route-receipt-v3.schema.json`. Preserve uncertainty rather than guessing, but do not use a value outside the installed profile's allowed runtime taxonomy. Derive decisions blind from installed runtime instructions; do not open or copy an expected test contract before an external coordinator captures the raw observation. A later maintainer comparison may apply narrower `accepted_scales` or `accepted_risks` to its fixed blind canary, but the task must never read those test-only tolerances before freezing its route.

- Preserve lifecycle precedence where both stages apply: context before requirements, requirements before solution design, design before delivery planning, planning before implementation, and implementation before quality evidence. Incident containment and release evidence recovery may precede this sequence.
- Use `testing-quality` when checks must be selected, executed, measured, or triaged. `review-audit` or `release-change` may inspect existing quality evidence without a separate quality branch, but must route there when evidence is missing, failing, stale, quantitative, or needs execution.
- Use `security-operations` for explicit security/privacy/reliability/operations scope, sensitive data, privileged boundaries, infrastructure or migrations, high blast radius, incidents, and production release. Other skills retain their proportional security and operability lenses; a separate security branch is conditional for ordinary low-risk design or review.
- Use `delivery-coordination` when live external sources, trackers, status, meetings, messages, provider mutations, or handoff synchronization are actually involved. Do not append it merely to make a route look complete.
- Use `documentation-knowledge` when canonical knowledge changes or release/operational handoff requires it. Use `retrospective-improvement` after a meaningful observed outcome, incident, failure, cancellation, recovery, or recurring friction. A route-only canary may observe such a pre-existing outcome even though the canary itself performs no delivery; never activate retrospective merely because the canary imagines a future delivery.
- Evaluate retrospective only when the selected profile declares it conditional or required. For a conditional retrospective with no meaningful outcome yet, record `planned-future` with `future-pending` and omit it from `actual_route`; when its outcome evidence is unknown, defer or block it with a linked structured gap. A direct retrospective profile makes `retrospective-improvement` the required intake/evidence owner and never duplicates it as conditional. If that direct request has only an asserted completion and no meaningful outcome evidence, keep the outcome `unknown`, cite a nonblocking `outcome_observation` gap in the outcome evidence, stop before findings, and do not invent lessons. Mere code, PR, or change completion is not by itself an observed user, business, operational, failure, recovery, cancellation, or recurring-friction outcome.
- For a hotfix or incident, `delivery-orchestrator` owns route recovery while `release-change` owns incident change control, restoration or rollback disposition, and the final recovery decision. Containment and evidence preservation precede nonessential ceremony; supporting security work must not delay an authorized emergency containment action.
- Re-entry is valid when a controller first opens evidence recovery and later makes the final decision, such as `release-change → testing-quality → release-change` or `review-audit → security-operations → review-audit`. Declare both which selected owners require prior controller entry and which owners must finish before the controller's final return; incident containment may be an explicit entry exception when immediate safety requires it.
- Extra proportional safety capabilities are allowed. A behavioral route fails for missing required ownership, unsafe authority, forbidden dependency, invalid gate order, or unexplained conditional omission—not merely because its exact sequence differs from an example.

## Bounded delegation

For large or independently reviewable work, delegation is optional and evidence-driven, never a mandatory swarm. Give each subagent one bounded outcome, exact inputs and repository revision, authority limits, expected artifact, and completion evidence. Use dependency waves and single-writer ownership for overlapping files. A fresh-context agent is preferred for independent review or security assessment when proportionate. Delegation never expands user authority; the primary agent remains accountable for reconciling conflicts, validating evidence, applying gates, and producing the final handoff.

## Outputs and handoff

A routing decision, scale/risk rationale, lifecycle checklist, artifact/evidence index, gate status, next skill(s), and blockers or authority needs.

## Completion evidence

The path covers the requested outcome; no required gate is silently skipped; existing artifacts were checked; facts/requirements/assumptions/decisions/questions are distinct; the next transition is executable.

## Must not

- Implement a material or risky change before requirements and design are sufficiently clear.
- Force full ceremony on a trivial low-risk change.
- Add lifecycle depth, delegation, artifacts, or adjacent scope without a current requirement or demonstrated risk.
- Auto-approve requirements/design, fabricate owners/estimates/evidence, or treat missing legacy runtimes as available.
- Create plugin-branded project state, require another plugin, or perform external/destructive/release actions beyond user authority.
