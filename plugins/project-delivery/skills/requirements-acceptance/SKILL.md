---
name: requirements-acceptance
description: Convert an approved project brief or request into testable requirements, work items, acceptance criteria, edge cases, non-functional requirements, and traceability. Use before design or implementation when expected behavior is not fully verifiable.
license: MIT
---

# Requirements and Acceptance Criteria

Read `../.shared/operating-model.md` and use the requirements template in `../.shared/artifact-templates.md`.

## When to invoke

Use for features, bugs, refactors with behavioral constraints, platform/infrastructure changes, migrations, API/data changes, security/reliability work, and multi-PR initiatives. Compress to a few criteria for small low-risk changes.

## Inputs and evidence

Expect a project brief or clear request. Inspect current behavior, tests, schemas/contracts, public APIs, accessibility/security/privacy guidance, service objectives, deployment constraints, compatibility commitments, issue/PR history, and relevant authoritative third-party docs.

## Workflow

1. Create stable `REQ-*` IDs for functional, non-functional, constraint, migration, and operational requirements where traceability helps.
2. Express user stories, job stories, or technical work items only when they improve understanding; do not force persona syntax on infrastructure or documentation work.
3. Write `AC-*` as observable outcomes with a verification method. Include positive, negative, boundary, permission, failure, retry/idempotency, concurrency, empty/large/old-data, and recovery cases as relevant.
4. Elicit hidden requirements across accessibility, localization, security, privacy/data retention, performance/capacity, reliability/availability, observability/support, compatibility, migration/rollback, cost, and legal/compliance.
5. Detect ambiguity and conflicts. Record the competing interpretations, impact, and decision owner; do not silently choose when behavior materially changes.
6. Identify dependencies and requirement-to-requirement conflicts. Separate must/should/could or use the repository’s priority system.
7. Apply the shared simplicity test: include only requirements needed for the stated outcome, explicit constraints, or demonstrated risks. Mark speculative generality, optional future use, and adjacent improvements as out of scope unless the user asks for them.
8. Seed traceability from each requirement to anticipated design, tests, work/PR slices, and release evidence.
9. Update the Definition of Ready and Done.

## Outputs and handoff

Requirements set, acceptance criteria, edge-case inventory, non-functional requirements, dependency/conflict log, traceability matrix, and readiness decision. Handoff to `solution-design`, or to `delivery-planning` for an already-established low-risk design.

## Completion evidence

Every must-have requirement is unambiguous enough to test; each has source/rationale and acceptance; material NFR/migration/accessibility/security/operations concerns are addressed or explicitly not applicable; unresolved blockers are visible.

## Must not

- Prescribe architecture unless it is a confirmed constraint.
- Claim user validation, legal compliance, performance, or accessibility without evidence.
- Turn implementation tasks into acceptance criteria or accept untestable words such as “fast,” “secure,” or “user-friendly” without measures.
- Convert hypothetical future needs or unsolicited adjacent improvements into must-have requirements.
