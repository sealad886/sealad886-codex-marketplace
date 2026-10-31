---
name: redux-toolkit
description: "Use when implementing Redux Toolkit stores, slices, selectors, thunks, RTK Query, or typed React integration."
---

# Redux Toolkit state ownership

## When to invoke

Use when implementing Redux Toolkit stores, slices, selectors, thunks, RTK Query, or typed React integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect existing state ownership, installed Redux Toolkit/React Redux versions, store lifetime, serialization, and async contracts.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Decide which shared client state belongs in Redux and which server data belongs in the existing query layer.
2. Extend configureStore, createSlice, typed hooks, and selectors around the feature boundary.
3. Implement async error/cancellation and cache behavior, then test user-observable transitions.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run typed store checks and tests for pending/success/rejected flows, selectors, and any invalidation or hydration behavior.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
