---
name: react
description: "Use when implementing React components, hooks, state ownership, accessibility, or measured rendering improvements."
---

# React

## When to invoke

Use when implementing React components, hooks, state ownership, accessibility, or measured rendering improvements.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect component boundaries, state flow, JSX, renderer/framework, and performance evidence.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify the component contract and keep state with its owner; derive values during render when possible.
2. Implement semantic JSX and pure rendering; use effects for synchronization with external systems.
3. Profile expensive rendering before choosing memoization, lazy loading, or a framework-supported server/client boundary.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run the existing type/lint checks and behavior tests for the changed interaction; use a profiler capture for performance claims.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
