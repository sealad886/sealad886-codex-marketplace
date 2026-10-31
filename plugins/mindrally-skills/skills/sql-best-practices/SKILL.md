---
name: sql-best-practices
description: "Use when writing or reviewing SQL queries, schema constraints, indexes, transactions, pagination, or database performance."
---

# SQL correctness and query plans

## When to invoke

Use when writing or reviewing SQL queries, schema constraints, indexes, transactions, pagination, or database performance.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect database engine/version, schema and statistics, query parameters, result contract, concurrency requirements, and execution plans.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define required rows, null semantics, ordering, and data-integrity constraints.
2. Write dialect-correct parameterized queries and coherent transactions.
3. Compare results and plans using representative data and safe execution scope.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test row/null/duplicate/order cases and transactional failure; inspect representative plans and record engine-specific execution limits.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
