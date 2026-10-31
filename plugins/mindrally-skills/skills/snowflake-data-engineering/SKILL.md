---
name: snowflake-data-engineering
description: "Use when designing Snowflake SQL pipelines, semi-structured data, streams/tasks, dynamic tables, warehouse performance, or recovery."
---

# Snowflake ingestion and transformation

## When to invoke

Use when designing Snowflake SQL pipelines, semi-structured data, streams/tasks, dynamic tables, warehouse performance, or recovery.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect account edition/region, data contracts, source arrival, refresh/retention needs, role grants, warehouse limits, and measured query history.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Choose ingestion and transformation primitives from latency, change, and recovery requirements.
2. Implement typed, idempotent transformations with explicit access and operational boundaries.
3. Validate duplicate/late data, freshness, cost evidence, and recovery behavior in an approved environment.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run isolated transformation/duplicate/null tests and inspect query/refresh history when authorized; identify omitted account, cost, and recovery qualification.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
