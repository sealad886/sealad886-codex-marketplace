---
name: graphql
description: "Use when designing GraphQL schemas, resolvers, mutations, generated clients, pagination, or query limits."
---

# GraphQL

## When to invoke

Use when designing GraphQL schemas, resolvers, mutations, generated clients, pagination, or query limits. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect schema/server/client versions, resolver/data ownership, nullability/error contract, auth rules, loader scope, and query workload. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define domain fields, input constraints, nullability and caller/resource authorization before resolver changes.
2. Implement bounded typed operations and request-scoped loading/caching with explicit mutation transaction semantics.
3. Validate schema/operations and test access, null/error propagation, pagination, N+1 behavior and query-cost limits.

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
