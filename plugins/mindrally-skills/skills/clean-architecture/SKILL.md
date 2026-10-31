---
name: clean-architecture
description: "Use when designing or refactoring dependency boundaries in Flutter or Go applications."
---

# Clean Architecture

## When to invoke

Use when designing or refactoring dependency boundaries in Flutter or Go applications. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect requested behavior, module imports, domain rules, I/O adapters, tests, and existing architectural decisions. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace dependencies and identify the concrete coupling or testing problem the change must solve.
2. Define the smallest boundary that keeps domain policy independent from transport/storage details.
3. Implement wiring in the composition root and verify domain behavior plus real adapter contracts.

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
