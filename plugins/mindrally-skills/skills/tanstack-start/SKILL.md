---
name: tanstack-start
description: "Use when implementing TanStack Start server functions, server routes, SSR/streaming, build configuration, or deployment adapters."
---

# TanStack Start full-stack boundaries

## When to invoke

Use when implementing TanStack Start server functions, server routes, SSR/streaming, build configuration, or deployment adapters.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Start/Router/Vite versions, current config/plugin, server function builder, route APIs, authentication, and target runtime.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify the installed Start generation before selecting imports/configuration.
2. Implement validated and authorized server-only operations with explicit HTTP/mutation semantics.
3. Verify client bundle boundaries, route behavior, SSR/streaming, and target build output.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Build server/client bundles and test invalid/unauthorized calls, mutation methods, raw-body handlers, and promised SSR/streaming behavior.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
