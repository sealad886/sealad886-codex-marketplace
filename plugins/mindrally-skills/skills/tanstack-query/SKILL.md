---
name: tanstack-query
description: "Use when implementing TanStack Query v5 options, cache ownership, server-state transitions, mutations, infinite queries, or Suspense."
---

# TanStack Query v5 workflows

## When to invoke

Use when implementing TanStack Query v5 options, cache ownership, server-state transitions, mutations, infinite queries, or Suspense.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect v5 minor/adapter, query client lifecycle, key inputs, router/SSR integration, and error/response contracts.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define keys and freshness based on server-state identity.
2. Reuse queryOptions where useful and implement version-correct fetch/mutation behavior.
3. Verify cache invalidation, cancellation, optimistic rollback, and pending/error rendering.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test v5 pending/disabled/error states, key isolation, transformed data types, failed optimistic updates, retries, and pagination.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
