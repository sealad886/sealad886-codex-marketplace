---
name: kysely
description: "Use when building typed Kysely SQL queries, dialect integration, transactions, migrations, or generated database types."
---

# Kysely Development Guidelines

## When to invoke

Use for building typed Kysely SQL queries, dialect integration, transactions, migrations, or generated database types.

## Inputs and evidence

Inspect Kysely/driver versions, dialect, schema types, actual returned driver types, pool ownership, and migration workflow. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Align schema interfaces and generated types with the real database/driver.
2. Build parameterized queries and inspect emitted SQL where semantics matter.
3. Use transactions for coupled effects and dialect-supported returning/upsert operations.
4. Validate types and run SQL/migration checks against the selected database.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Type checks and selected-dialect tests establish query results, transaction rollback, and schema/type agreement.

## Must not

Do not treat static types or raw SQL casts as runtime conversion/validation. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
