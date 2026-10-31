# Prisma: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Types and generation

- Prisma schema @id/@unique/@relation are schema attributes, not TypeScript decorators.
- Generated types describe the generated schema/client; validate external input and keep migration/schema/client versions coherent.
- Soft deletes and Repository layers are optional policies; if used, account for relations, uniqueness and all access paths.

## Execution and safety

- Instrumentation changed across major versions: older $use, v7 Client extensions and v8 middleware are different APIs. Confirm the installed surface rather than copying a generic middleware recipe.
- Typed client calls do not authorize rows or protect unsafe raw SQL interpolation; parameterize values and enforce ownership separately.
- Use the actual database provider for semantic integration tests; in-memory SQLite does not prove PostgreSQL/MySQL behavior.
- Transactions, batch operations, selects/includes and pooling have provider/runtime limits; inspect generated queries and errors.

## Primary documentation

- [Primary documentation](https://www.prisma.io/docs/orm/v7/prisma-client/client-extensions) — Prisma extension/middleware APIs are generation-specific; current docs distinguish v7 Client extensions and v8 middleware.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
