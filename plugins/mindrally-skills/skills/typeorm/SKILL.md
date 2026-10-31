---
name: typeorm
description: "Use when implementing TypeORM entities, relations, DataSource, migrations, transaction handling, or database query behavior."
---

# TypeORM persistence and transactions

## When to invoke

Use when implementing TypeORM entities, relations, DataSource, migrations, transaction handling, or database query behavior.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect TypeORM/driver/TypeScript versions, entity metadata, naming strategy, migrations, TLS configuration, constraints, and transaction managers.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define schema/relations and driver-correct types without implicit destructive synchronization.
2. Implement parameterized queries and transaction-scoped repositories/managers.
3. Test relation integrity, rollback, concurrent writes, and migration output in an isolated database.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run entity/type checks and isolated database tests for FK mapping, precision, transaction rollback, cascades, TLS, and relevant migrations.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
