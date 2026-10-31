---
name: react-query
description: "Use when maintaining React Query or TanStack Query fetching, cache keys, invalidation, pagination, or optimistic mutations."
---

# React Query server state

## When to invoke

Use when maintaining React Query or TanStack Query fetching, cache keys, invalidation, pagination, or optimistic mutations.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect package major, QueryClient lifetime, query keys, authentication scopes, and server mutation behavior.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify installed React Query/TanStack major and the server-state owner.
2. Define complete query keys, fetching failures, conditional execution, and deliberate freshness policy.
3. Implement mutation invalidation or optimistic rollback, then verify observable cache transitions.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test loading, error, stale/refetch, invalidation, and failed optimistic mutation behavior against the installed major.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
