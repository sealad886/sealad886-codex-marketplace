---
name: pyspark-etl
description: "Use when building PySpark transformations, joins/windows, idempotent ETL, or Apache Iceberg writes and metadata checks."
---

# PySpark ETL

## When to invoke

Use for building PySpark transformations, joins/windows, idempotent ETL, or Apache Iceberg writes and metadata checks.

## Inputs and evidence

Inspect Spark/PySpark/Iceberg/catalog versions, source/sink schemas, key/time semantics, partitioning, SparkSession ownership and data-quality invariants. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define row/key/null/schema and rerun/backfill invariants before transformation.
2. Use explicit joins/windows and native expressions with a reviewed execution plan.
3. Write through supported catalog/V2 APIs with deliberate merge/overwrite and concurrency behavior.
4. Validate output and rerun/backfill semantics on synthetic data with actual Spark/Iceberg integration where claimed.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Spark transformations and catalog-specific write tests demonstrate schema/key preservation, idempotent reruns, backfill ordering and failure recovery.

## Must not

Do not overwrite tables, stop shared sessions or force driver materialization as an incidental diagnostic. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
