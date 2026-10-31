---
name: postgresql-best-practices
description: "Use when designing PostgreSQL schema/indexes, inspecting query plans, transactions, RLS, pooling, or maintenance plans."
---

# PostgreSQL Best Practices

## When to invoke

Use for designing PostgreSQL schema/indexes, inspecting query plans, transactions, RLS, pooling, or maintenance plans.

## Inputs and evidence

Inspect server/extensions, schema/query workload, migration ownership, role/RLS context, pool mode and operational authority. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define types/constraints and identity/partition choices from actual invariants.
2. Inspect safe plans and representative workload evidence before query/index changes.
3. Implement parameterized transactions and access policies with pool-safe identity context.
4. Validate SQL/migrations and cross-role behavior; plan operational maintenance and restore checks separately.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

SQL/migration and ordinary-role RLS tests pass; query improvements and operational recovery claims have direct evidence.

## Must not

Do not run write plans, maintenance, index deletion or privileged policy changes as read-only diagnostics. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
