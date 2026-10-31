---
name: mysql-best-practices
description: "Use when designing MySQL schemas, indexes, transactions, queries, replication diagnostics, or safe maintenance plans."
---

# MySQL Best Practices

## When to invoke

Use for designing MySQL schemas, indexes, transactions, queries, replication diagnostics, or safe maintenance plans.

## Inputs and evidence

Inspect actual MySQL version/engine, schema and workload, query plans, data growth, isolation, replication and maintenance authority. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Model constraints, precision, encoding and keys from data requirements.
2. Use parameterized queries and measure representative plans/index choices.
3. Define transaction failure/deadlock behavior and replica consistency requirements.
4. Validate migrations and performance locally; execute maintenance only under explicit operational authority.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Selected-version SQL and migration tests pass; plan/latency measurements support tuning and transaction failure behavior is checked.

## Must not

Do not copy fixed server settings or run live maintenance/destructive migrations from generic advice. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
