---
name: sequelize
description: "Use when changing Sequelize models, associations, migrations, transactional writes, hooks, or query behavior."
---

# Sequelize data integrity

## When to invoke

Use when changing Sequelize models, associations, migrations, transactional writes, hooks, or query behavior.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Sequelize major/dialect, models/migrations, association aliases, constraints, transaction propagation, and query plans.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define database constraints and the transaction boundary before changing model behavior.
2. Implement dialect/version-correct queries and pass transaction context consistently.
3. Test constraints, rollback, concurrent writes, associations, and migration behavior.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run isolated database tests for uniqueness races, rollback, hooks, relation pagination, and relevant up/down migrations.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
