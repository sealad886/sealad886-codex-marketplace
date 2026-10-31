---
name: prisma
description: "Use when implementing Prisma schemas, typed queries, transactions, pagination, or version-aware query instrumentation."
---

# Prisma

## When to invoke

Use for implementing Prisma schemas, typed queries, transactions, pagination, or version-aware query instrumentation.

## Inputs and evidence

Inspect Prisma/client generator versions, database provider/driver, schema constraints, generated output, connection lifetime and access policies. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Model required data/relations/constraints with supported provider features.
2. Use generated queries and selected fields with explicit transaction/error behavior.
3. Integrate supported instrumentation/extensions/middleware for the installed major.
4. Run generation/type checks and actual-provider tests for persistence and authorization.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Generated client/type checks and selected-provider tests establish queries, transactions, constraints and row authorization.

## Must not

Do not infer runtime input validation or RLS/ownership from generated client types. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
