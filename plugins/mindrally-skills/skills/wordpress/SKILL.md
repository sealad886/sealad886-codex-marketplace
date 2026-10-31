---
name: wordpress
description: "Use when implementing WordPress hooks, admin/REST handlers, settings, data queries, scheduled work, or theme extensions."
---

# WordPress plugin and theme boundaries

## When to invoke

Use when implementing WordPress hooks, admin/REST handlers, settings, data queries, scheduled work, or theme extensions.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect WordPress/PHP/plugin versions, active theme type, hook lifecycle, capabilities/nonces, database ownership, and test environment.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Extend the existing plugin/theme through supported hooks and APIs.
2. Implement validated authorized handlers and context-correct output/data access.
3. Verify behavior, security failures, scheduled/resource lifetime, and update-safe templates.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run applicable WordPress/PHP checks and isolated handler/permission/template/cron tests; identify unavailable store or deployment checks.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
