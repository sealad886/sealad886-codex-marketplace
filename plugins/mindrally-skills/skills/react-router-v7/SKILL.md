---
name: react-router-v7
description: "Use when implementing React Router v7 framework routes, loaders, actions, forms, pending UI, or route error boundaries."
---

# React Router v7 framework mode

## When to invoke

Use when implementing React Router v7 framework routes, loaders, actions, forms, pending UI, or route error boundaries.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect the v7 package version, framework/data/declarative mode, routes.ts, rendering strategy, and server/client module boundaries.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Register a route through the configured route system rather than assuming a filename is sufficient.
2. Validate loader/action inputs and enforce server-side authorization at each protected boundary.
3. Implement navigation or fetcher state, error responses, and focused route/form checks.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run route type generation/type checks and integration checks for successful and failed loader/action flows, including any promised no-JavaScript path.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
