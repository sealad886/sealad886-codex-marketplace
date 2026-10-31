---
name: vue-pinia
description: "Use when implementing Pinia stores, reactive selectors, async actions, SSR scope, persistence, or store/component tests."
---

# Pinia state ownership and lifecycle

## When to invoke

Use when implementing Pinia stores, reactive selectors, async actions, SSR scope, persistence, or store/component tests.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Vue/Pinia versions, state owner, active Pinia instance, SSR hydration, persisted fields, and test action stubbing.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Determine whether state belongs locally, in URL/server cache, or in a shared store.
2. Implement focused state/getters/actions with explicit async/resource ownership.
3. Verify reactive consumers, real action execution, persistence, and per-request isolation.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test real store actions and reactive components separately, including SSR instance isolation, persistence migration, and async failure.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
