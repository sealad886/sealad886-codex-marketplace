---
name: sanity
description: "Use when changing Sanity Studio schemas, GROQ queries, typed content access, previews, or client configuration."
---

# Sanity content models and queries

## When to invoke

Use when changing Sanity Studio schemas, GROQ queries, typed content access, previews, or client configuration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Sanity/Studio/client versions, schema registration, dataset permissions, API date, query perspectives, and preview flow.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Model content and validation around editor and consumer needs.
2. Implement parameterized projections and explicit client/perspective settings.
3. Verify schema registration, query result shape, draft access, and editor behavior.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run schema/type generation and query checks against approved fixture content; verify published/draft access and editor validation when available.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
