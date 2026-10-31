# Prisma ORM Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Migrations and generated clients

- Do not modify already applied/shared migrations casually; an unapplied local draft may be edited through the repository workflow.
- Migration runners track ordered application; every SQL migration is not inherently or necessarily idempotent when rerun manually.
- PrismaClientValidationError reports invalid client query arguments and is not a general schema/input-validation API.
- Regenerate against the correct schema/runtime and review destructive data effects before migration execution.

## Boundaries and tests

- Use the installed generation’s query extension/middleware API, which changes across Prisma majors.
- Transactions require correct isolation/idempotency; retries can duplicate external effects.
- Soft deletion needs explicit semantics and authorization across direct, relation, aggregate and raw query paths.
- Mocked client or SQLite tests do not establish another provider’s migration/types/locking behavior; include relevant real-provider tests.

## Primary documentation

- [Primary documentation](https://www.prisma.io/docs/orm/v7/prisma-client/client-extensions) — Versioned Prisma docs distinguish supported Client extensions from other generations’ middleware.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
