# Kysely Development Guidelines: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Types and dialects

- Generated and ColumnType describe compile-time select/insert/update contracts; they do not convert driver values or validate live schema.
- Numeric aggregates, dates and large integers may return strings or driver-specific values; count<number> does not coerce runtime output.
- RETURNING, ON CONFLICT and serial column syntax vary by dialect; PostgreSQL examples are not portable to every database.

## Execution and migrations

- Kysely parameterizes values, but named/prepared-statement caching depends on the driver; do not claim every query automatically becomes a server-side prepared statement.
- Keep raw SQL identifiers allowlisted; parameterization of values does not make untrusted identifier fragments safe.
- Transactions must use the transaction object for all coupled queries; define rollback/retry behavior for the database isolation level.
- Check migration results/errors and verify applied schema before regenerating types; do not run destructive down migrations implicitly.

## Primary documentation

- [Primary documentation](https://kysely.dev/docs/recipes/data-types) — Kysely distinguishes TypeScript types from driver-provided runtime values and does not transform them automatically.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
