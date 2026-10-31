---
name: snowflake-snowpark-dbt
description: "Use when implementing Snowpark DataFrames/UDFs or dbt-snowflake models, incremental updates, tests, and environment isolation."
---

# Snowpark and dbt transformations

## When to invoke

Use when implementing Snowpark DataFrames/UDFs or dbt-snowflake models, incremental updates, tests, and environment isolation.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Snowpark/dbt/adapter versions, execution location, connection identity, schemas, model lineage, artifacts, and write authority.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Keep transformations at the appropriate execution boundary and define data/schema ownership.
2. Implement version-correct DataFrame/UDF or dbt materialization logic with explicit incremental semantics.
3. Compile/test on approved fixtures and check data movement, late data, schema drift, and environment isolation.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Compile models and run bounded dbt/Snowpark fixture tests when authorized; verify first/empty/incremental/late-data and schema-isolation scenarios.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
