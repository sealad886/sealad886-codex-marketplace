---
name: sveltekit
description: "Use when implementing SvelteKit routes, load functions, actions, endpoints, rendering options, or server/client state."
---

# SvelteKit route and server boundaries

## When to invoke

Use when implementing SvelteKit routes, load functions, actions, endpoints, rendering options, or server/client state.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Svelte/SvelteKit versions, adapters, route files, generated types, auth locals/cookies, and rendering settings.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Choose the correct page/layout/server endpoint boundary for the requested behavior.
2. Validate and authorize server loads/actions while keeping secrets out of shared/client modules.
3. Verify navigation, invalid actions, errors, hydration, and the selected rendering strategy.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run svelte-check/build and route/action tests for unauthorized data, invalid forms, deep links, and the promised SSR/prerender path.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
