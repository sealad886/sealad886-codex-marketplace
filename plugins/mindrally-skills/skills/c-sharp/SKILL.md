---
name: c-sharp
description: "Use when implementing or reviewing C#/.NET logic, asynchronous APIs, resource lifetimes, Blazor, or Unity code."
---

# C# Development Guidelines

## When to invoke

Use when implementing or reviewing C#/.NET logic, asynchronous APIs, resource lifetimes, Blazor, or Unity code. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect target framework and language version, nullable settings, project conventions, threading/lifetimes, and host restrictions. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Identify the public behavior and target runtime/language constraints before choosing syntax or abstractions.
2. Implement explicit nullability, resource ownership, async/cancellation, and error contracts using existing patterns.
3. Build and verify success/failure behavior, disposal, concurrency, serialization, and host-specific integration.

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
