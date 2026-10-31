---
name: zustand-state-management
description: "Use when implementing Zustand stores, selectors, middleware, persistence, SSR scope, or async client workflow state."
---

# Zustand shared state and hydration

## When to invoke

Use when implementing Zustand stores, selectors, middleware, persistence, SSR scope, or async client workflow state.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Zustand/React versions, store scope, selector output identity, middleware order, persisted schema, and SSR/hydration behavior.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Assign local/shared/server state ownership and choose store lifetime.
2. Implement typed actions, immutable updates, and stable selector outputs.
3. Verify transitions, persistence migration, subscriptions, and request/client hydration isolation.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test selector stability, nested updates, overlapping async flows, persistence migration, cleanup, and SSR/hydration where used.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
