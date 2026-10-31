---
name: svelte
description: "Use when implementing Svelte components, runes, snippets, state sharing, effects, or a deliberate legacy-to-runes migration."
---

# Svelte component reactivity

## When to invoke

Use when implementing Svelte components, runes, snippets, state sharing, effects, or a deliberate legacy-to-runes migration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Svelte/compiler major, component mode, props/events, shared state ownership, SSR context, and existing component tests.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Select the component’s supported reactivity mode and preserve its public contract.
2. Model source state and derived values explicitly; reserve effects for external synchronization.
3. Verify updates, teardown, SSR/hydration, events, and accessibility.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run svelte-check/build and component tests for reactive updates and cleanup; verify SSR/hydration if the application uses them.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
