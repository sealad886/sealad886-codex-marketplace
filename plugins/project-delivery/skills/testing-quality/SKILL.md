---
name: testing-quality
description: Select, execute, and report risk-based validation for a change or release candidate. Use for unit, integration, end-to-end, contract, regression, invariant, static, performance, security, CI-parity, and failure-triage evidence.
license: MIT
---

# Testing and Quality Engineering

Read `../.shared/operating-model.md`; use the test evidence template in `../.shared/artifact-templates.md`.

## When to invoke

Use after implementation, during planning/design to define strategy, when CI fails, for release gates, or for test-only/quality requests. Lead flaky-CI triage, performance-only claims, and combined platform performance/packaging/signing/distribution evidence recovery. Select depth from scale, blast radius, failure modes, and repository norms—not a universal coverage percentage.

## Inputs and evidence

Expect exact target revision/diff and requirements/acceptance when available. Inspect test layout, CI workflows, build/lint/type/format commands, coverage/performance/security thresholds, test data/fixtures, service dependencies, environments, flaky-test policy, and past related failures.

## Workflow

1. Build a risk-to-test matrix. Cover changed logic and the most consequential regressions, boundaries, permissions, failure/retry/recovery paths, data compatibility, concurrency/idempotency, and operational signals.
2. Select applicable levels: unit, component, integration, contract/API/schema, end-to-end/user journey, regression/characterization, property/invariant/fuzz, migration/rollback, static analysis, type/lint/format, dependency/security, performance/load/resource, accessibility, docs/link/example/build.
3. Prefer deterministic, isolated, maintainable tests; specify environment, versions, data provenance, seeds, credentials handling, external-service substitution, and cleanup.
4. Inspect unfamiliar test/build wrappers and delegated scripts before execution. Record consequential side effects and exact authorization for filesystem mutation, fixed temporary paths, signing/notarization, credentials, network/provider access, packaging, publication, deployment, or cleanup. A technically valid result produced outside authority remains non-compliant evidence and cannot pass the authority gate.
5. Run targeted checks early, then the broadest practical repository/CI-parity gates. Bind evidence as `question → focused scenario → matching method → fresh identified artifact → observable/quantitative result → limitations`. Capture command, exit status, revision, device/browser/runtime/build variant, environment, data/run count, counts/duration, artifact/log locations, and material side effects. Compare before/after only under comparable conditions; one noisy sample is a lead, not a conclusion.
6. Triage the first causal failing job/step and dependency fanout. Classify configuration, environment/toolchain, dependency/cache, product/test regression, flaky/timing, external/transient infrastructure, downstream cascade, pre-existing, or setup/proof gap. Reproduce on the same revision when useful; distinguish counterevidence from inability to test. Evaluate affected requirements and gates, then propose viable corrective or proof-recovery responses with material tradeoffs, a recommendation, and next owner/action; do not stop at naming the failure category. Retry only the smallest evidence-confirmed transient unit, never a deterministic failure, and retain JUnit/result artifacts and retry metadata.
7. Compare each `AC-*`/risk to actual evidence. Mark verified, failed, not run with reason, or not applicable.
8. For performance/security claims, use representative measurements/tools and state limitations. Prove artifact freshness and identity; for leaks or ownership defects validate the offending path/invariant, not merely a smaller capture. A lack of findings is not proof of absence.
9. Assess CI quality when relevant: reproducible lock/cache inputs, retained result artifacts, slow/flaky baseline, before/after duration and pass/retry metrics, and approval gates paired with restricted credentials. Select optional domain-specialist tools from the actual platform, but keep the evidence contract provider-neutral.
10. Produce separate technical and authority gate decisions with residual gaps and release impact.
11. For combined platform claims, establish the focused scenario and fresh artifact before handing security/signing concerns to `security-operations` and package/distribution decisions to `release-change`. Do not let a downstream release controller pre-judge missing quality evidence.

## Outputs and handoff

Test strategy/evidence matrix, actual commands/results, solution-oriented failure triage, requirement coverage, CI parity, gaps, and quality gate decision. Handoff bounded corrections to `implementation-execution`, material design choices to `solution-design`, and successful evidence to `documentation-knowledge`, `review-audit`, and `release-change`.

## Completion evidence

Relevant tests actually ran; results are tied to the target revision/environment; failures and not-run checks are explicit; acceptance and risk coverage are traceable; residual confidence is calibrated.

## Must not

- Say “should pass,” use fixed coverage/E2E mandates unrelated to repository/risk, or confuse selected tests with complete system assurance.
- Alter tests merely to accept incorrect behavior, expose secrets/test personal data, or claim CI parity without comparing workflows.
- Treat successful execution as authority-compliant when the command performed an unauthorized side effect.
