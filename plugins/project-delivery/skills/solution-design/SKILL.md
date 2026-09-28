---
name: solution-design
description: Design a production-ready solution from repository evidence and accepted requirements. Use for architecture, interfaces, data contracts, compatibility, migrations, rollback, observability, security, testability, release effects, or ADR decisions.
license: MIT
---

# Solution Design and Architecture

Read `../.shared/operating-model.md`; use the design/ADR template in `../.shared/artifact-templates.md`.

## When to invoke

Use for new systems, cross-module changes, public contracts, data/schema/infrastructure changes, high-risk fixes, refactors, or any material decision with multiple viable approaches. A small familiar change may need only a design delta.

## Inputs and evidence

Expect accepted requirements or clearly stated design-only scope. Inspect current architecture, dependency direction, entry points, data flow, interfaces/schemas, tests, deploy topology, observability, security guidance, historical decisions and Git history, and current authoritative docs for external APIs/frameworks.

## Workflow

1. Describe current state, constraints, pain points, and invariants with exact repository evidence.
2. Propose responsibilities, component boundaries, flows, interfaces, data/failure contracts, configuration, and lifecycle behavior. Reuse existing owners and extract a shared helper only for a stable process repeated across callers; preserve distinct domain behavior instead of forcing generic reuse.
3. Apply the shared simplicity test. Start with the least complex viable design that extends canonical paths. Analyze alternatives—including no change when meaningful—by correctness, complexity, compatibility, operability, cost, delivery risk, and reversibility. Choose added abstraction or infrastructure only when the simpler design has a concrete evidenced failure.
4. Address backward/forward compatibility, version negotiation, deprecation, data/config migration, coexistence windows, rollback, and failure recovery.
5. Design observability: user-visible errors, logs without secrets, metrics/traces, health, alerts, dashboards, ownership, and diagnostic paths.
6. Address authentication/authorization, trust boundaries, sensitive data, privacy/retention, dependency/supply-chain risk, abuse/failure modes, least privilege, and secrets.
7. Map design to test levels, test seams/data/environments, CI implications, feature flags, deployment sequencing, and release evidence.
8. Create/update an ADR when the decision is durable, cross-cutting, costly to reverse, contested, or establishes a standard. Follow the repository’s ADR convention; do not impose a new path.
9. Recheck every `REQ-*`/`AC-*` for design coverage and list decisions/questions.

## Outputs and handoff

Current/proposed design, alternatives/tradeoffs, contracts, compatibility/migration/rollback, observability/security/test/release implications, ADRs if warranted, and requirement coverage. Handoff to `security-operations` for high-risk design review and then `delivery-planning`.

## Completion evidence

The design is feasible against the actual repository; interfaces and failure behavior are explicit; compatibility, rollback, security, operations, tests, and release are addressed; tradeoffs and open questions are honest.

## Must not

- Implement, select technology from fashion, or force greenfield patterns onto an existing system.
- Invent external API behavior; retrieve current authoritative documentation.
- Create an ADR for routine reversible detail or omit consequences/alternatives for a material decision.
- Add abstraction, configurability, infrastructure, or future-proofing without a current requirement or demonstrated risk.
- Propose a rewrite without showing why bounded changes would retain or worsen entrenched complexity, duplication, incompatible paths, or an architecture that obstructs the accepted outcome.
- Duplicate one process across multiple code paths when a narrow, well-owned helper can express it without erasing domain differences.
