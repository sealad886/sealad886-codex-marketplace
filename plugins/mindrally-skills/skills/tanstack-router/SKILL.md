---
name: tanstack-router
description: "Use when implementing TanStack Router routes, search validation, context, beforeLoad guards, loaders, or query integration."
---

# TanStack Router route contracts

## When to invoke

Use when implementing TanStack Router routes, search validation, context, beforeLoad guards, loaders, or query integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect router/plugin versions, generated or code-based route tree, search parsing, auth context, loaders, and server data boundaries.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Register the route through the project’s supported route construction and generation.
2. Validate navigation/search inputs and load required data with deliberate freshness.
3. Verify route states and enforce authorization at every server data endpoint.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run route generation/type checks and tests for malformed search, auth changes, direct API access, reloads, and stale cache behavior.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
