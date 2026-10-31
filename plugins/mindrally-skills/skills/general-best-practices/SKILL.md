---
name: general-best-practices
description: "Use when reviewing cross-stack engineering quality, testing, security, performance, observability, or maintainability."
---

# General Best Practices

## When to invoke

Use when reviewing cross-stack engineering quality, testing, security, performance, observability, or maintainability. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect requested behavior, repository policies, call paths/invariants, current tests/tooling, data trust and operational constraints. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Identify the concrete user-visible problem and existing contract before applying a general engineering pattern.
2. Implement the smallest coherent change with explicit validation, ownership, failure and resource boundaries.
3. Run risk-proportionate checks and review scope, evidence, documentation and remaining uncertainty.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
