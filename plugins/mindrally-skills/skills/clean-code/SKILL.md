---
name: clean-code
description: "Use when writing, reviewing, or simplifying code for readability, maintainability, and justified abstraction."
---

# Clean Code

## When to invoke

Use when writing, reviewing, or simplifying code for readability, maintainability, and justified abstraction. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect the requested behavior, existing call sites, invariants, test evidence, conventions, and change ownership. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define the smallest coherent change and trace what callers rely on before refactoring.
2. Use intent-revealing names and direct control flow; extract shared logic only when it represents the same responsibility.
3. Compare behavior before/after and run proportionate checks while reviewing the full diff for scope and complexity.

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
