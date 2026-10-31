---
name: aspnet-core
description: "Use when implementing ASP.NET Core APIs, middleware, authentication, authorization, caching, or configuration."
---

# ASP.NET Core Development Guidelines

## When to invoke

Use when implementing ASP.NET Core APIs, middleware, authentication, authorization, caching, or configuration. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect target .NET framework, Program pipeline, endpoint/controller structure, options, authentication scheme, and deployment topology. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define endpoint semantics and inspect middleware/order, dependency lifetimes, and authorization policies.
2. Implement request validation, asynchronous domain calls, safe error responses, and the selected cache/configuration boundary.
3. Verify validation, denied access, middleware behavior, cancellation, cache isolation/invalidation, and production configuration.

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
