---
name: cpp
description: "Use when implementing or reviewing C++ ownership, concurrency, language features, error handling, or performance."
---

# C++ Development Guidelines

## When to invoke

Use when implementing or reviewing C++ ownership, concurrency, language features, error handling, or performance. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect compiler/standard/library versions, build targets, ownership/lifetime contracts, exception policy, and threading model. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace value/resource lifetimes and public invariants before choosing types or concurrency primitives.
2. Implement the simplest supported value/RAII design with explicit non-owning views, synchronization, and failure contracts.
3. Build with target compilers and run focused behavior tests, relevant sanitizers, and measured performance checks.

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
