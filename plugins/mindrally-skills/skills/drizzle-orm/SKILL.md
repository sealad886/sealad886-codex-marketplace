---
name: drizzle-orm
description: "Use when implementing Drizzle schema, typed queries, relations, transactions, drivers, or migrations."
---

# Drizzle ORM Development Guidelines

## When to invoke

Use when implementing Drizzle schema, typed queries, relations, transactions, drivers, or migrations. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect installed Drizzle ORM/Kit versions, dialect/driver, live schema/migrations, query contract, transaction and ownership rules. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inspect dialect/driver capabilities and define database constraints plus query/result semantics.
2. Implement parameterized queries, explicit relations/keys, bounded stable pagination, and required transactions.
3. Type-check and test against the intended database/driver; review generated SQL and authorized migration plans.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
