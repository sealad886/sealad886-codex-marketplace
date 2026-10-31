# TypeORM persistence and transactions: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Keep production TLS certificate verification enabled with the required trusted CA; rejectUnauthorized:false weakens identity verification and is not a production default.

- Use repositories/managers supplied by the active transaction, not an unrelated global custom repository; always release QueryRunner resources.

- Ensure explicit FK column names and JoinColumn names map to one intended column; authorId and author_id can diverge without a naming strategy.

- Decimal/bigint values may be returned as strings depending on the driver to preserve precision; do not assume a number annotation performs conversion.

- Relation cascade saves/removes, database ON DELETE actions, orphan handling, and soft deletes are distinct behaviors; broad cascade:true needs explicit justification.

- Initialize properties appropriately under strictPropertyInitialization and use module/decorator settings supported by the chosen build, not a universal CommonJS configuration.

- Use migrations, inspect generated SQL/dialect defaults, and avoid synchronize:true against valuable databases.

- Eager and lazy relation access differ; test actual query counts and join/null semantics rather than assuming logging a relation always triggers a query.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [TypeORM transactions require the provided transactional manager and scoped repositories.](https://dev.typeorm.io/docs/transactions/)
- [Driver/data-source options define TLS and database-specific behavior.](https://typeorm.io/docs/drivers/postgres/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
