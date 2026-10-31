---
name: remix
description: "Use when maintaining a Remix application\u2019s routes, loaders, actions, sessions, progressive forms, or migration decisions."
---

# Remix full-stack routes

## When to invoke

Use when maintaining a Remix application’s routes, loaders, actions, sessions, progressive forms, or migration decisions.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Remix major, runtime adapter, route conventions, Vite configuration, session storage, and deployment target.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify the project’s actual Remix generation and supported route/build APIs.
2. Implement validated loader/action boundaries and session-aware authorization.
3. Verify route nesting, form errors, redirects, and the supported progressive-enhancement path.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test authorized and unauthorized route data, invalid form submissions, cookie persistence, redirects, and any claimed JavaScript-disabled behavior.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
