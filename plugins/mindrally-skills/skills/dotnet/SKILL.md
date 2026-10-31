---
name: dotnet
description: "Use when implementing .NET backend APIs, EF Core data access, DI, async operations, validation, or integration tests."
---

# .NET Development Guidelines

## When to invoke

Use when implementing .NET backend APIs, EF Core data access, DI, async operations, validation, or integration tests. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect target framework, ASP.NET/EF/provider versions, endpoint contracts, DI lifetimes, database schema, and auth/transaction boundaries. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define requested API/domain behavior and inspect the existing architecture and persistence path.
2. Implement typed validation, asynchronous/cancellable work, scoped EF operations, and explicit authorization/error handling.
3. Build and test API plus database contracts using the target provider where semantics matter.

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
