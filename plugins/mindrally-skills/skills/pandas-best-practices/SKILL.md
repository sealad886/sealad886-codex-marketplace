---
name: pandas-best-practices
description: "Use when processing pandas DataFrames, joins, missing data, time series, dtype conversion, or memory-sensitive analysis."
---

# Pandas Best Practices

## When to invoke

Use for processing pandas DataFrames, joins, missing data, time series, dtype conversion, or memory-sensitive analysis.

## Inputs and evidence

Inspect pandas version, schema/dtypes, null policy, index/join cardinality, time-zone semantics, provenance and memory budget. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Validate inputs and record intended row/key preservation and rejected-data handling.
2. Apply explicit typed transformations and single-step indexed assignments.
3. Use checked joins/aggregations and deliberate date/null/conversion policies.
4. Test row counts, invariants and representative edge data; profile allocations/time where relevant.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Data invariants, conversion/rejection counts, joins and time-series boundary tests pass without silent row/value loss.

## Must not

Do not drop/impute/coerce data silently or treat a successful DataFrame operation as verified analysis. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
