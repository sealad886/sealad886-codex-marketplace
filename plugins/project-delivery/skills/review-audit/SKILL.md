---
name: review-audit
description: Independently review a design, plan, diff, PR, repository slice, or release candidate against requirements, architecture, conventions, tests, security, operations, and release criteria with exact evidence-backed findings.
license: MIT
---

# Code Review and Audit

Read `../.shared/operating-model.md`; use the review template in `../.shared/artifact-templates.md`.

## When to invoke

Use for design review, normal code review, security-aware review, adversarial audit, review feedback adjudication, or release-readiness audit. Preserve reviewer independence: use a fresh context or subagent when available and proportionate, but remain useful without one.

## Inputs and evidence

Resolve exact scope/base/head/revision and review mode. Inspect requirements/AC, design/ADRs, plan, diff plus supporting code, applicable instructions, tests/results, docs, CI/release config, Git history, security/operational guidance, and existing findings. Do not review only the patch when unchanged context controls behavior.

## Workflow

1. Select lenses:
   - Design: requirements coverage, alternatives, interfaces, compatibility, migration/rollback, security/operations/test/release feasibility.
   - Code: correctness, invariants, errors, data/concurrency, maintainability, conventions, duplication, compatibility, tests/docs.
   - Security: trust boundaries, attacker inputs, authn/authz, secrets, sensitive data/privacy, dependencies, abuse paths, severity/exploitability.
   - Release readiness: requirement/test evidence, CI, approvals, migrations, flags, observability, rollback, support, residual risk.
2. Trace `REQ/AC → design → diff/work → test/docs/release evidence`; identify omissions and unsupported claims.
3. Define assessment mode, target revision/snapshot, reviewed surfaces, exclusions, deferred/not-applicable surfaces, and coverage completeness. Validate each candidate against source and reachable behavior; for security paths record source, control, sink, reachable boundary, preconditions/outcome, counterevidence, proof gaps, and static/dynamic validation rationale.
4. Deduplicate by stable root-cause identity/fingerprint while retaining every affected location and its role. Report decision-ready `FIND-*` with severity, priority, exact location, evidence, impact, response constraints and invariant, viable solution options and material tradeoffs, recommended response and next action, owner or authority need, release-blocking state, confidence, uncertainty, and residual risk. A localized obvious defect may have one precise fix; a material design choice should compare multiple credible options. If evidence cannot yet support a remedy, specify the smallest next proof action instead of stopping at the defect.
5. Distinguish confirmed defect, design concern, test/evidence gap, question, and accepted residual risk. Do not inflate style preference into correctness.
6. Technically adjudicate incoming review comments; verify before accepting or rejecting them.
7. Re-review fixes and rerun relevant evidence before closing findings. Apply the shared finding lifecycle. Suppression is limited to evidence-backed false-positive, duplicate, or invalidation closure and records category, rationale, counterevidence, sibling/variant checks, qualified reviewer/date, revalidation trigger, release treatment, and residual uncertainty; a duplicate links its canonical finding. If material reachability/exploitability/impact remains uncertain, keep the candidate open or mark it deferred/blocked with owner and next proof action. Residual risk requires acceptance by the identified risk owner. Verify remediation invariant and regression evidence before `fixed`.

## Outputs and handoff

Review decision, scope/revision, decision-ready finding ledger, requirement coverage, positive evidence (brief), residual risks, blockers, and re-review needs. Handoff bounded fixes to `implementation-execution`, material solution choices to `solution-design`, evidence gaps to `testing-quality`, security/operations depth to `security-operations`, and cleared work to `release-change`.

## Completion evidence

Exact scope is pinned; all material lenses were applied or marked not applicable; findings are reproducible, located, impact-assessed, and paired with a viable recommended response or explicit next proof action; blockers/residual risk are explicit; reviewer did not self-approve unverified work.

## Must not

- Implement fixes in a review-only request, fabricate findings for volume, or approve because tests merely exist.
- Require a particular hosting platform/plugin, expose secrets, or claim exhaustive security assurance from a normal review.
