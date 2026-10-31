# Drizzle ORM Development Guidelines: implementation guidance

## Schema and API versioning

Drizzle relation APIs changed between stable generations and v1/RC documentation;
match relations/defineRelations and relational queries to the installed release.
Application relations do not create database foreign keys. defaultNow supplies
an insert default, not automatic updatedAt maintenance. Nullable columns and
returning-row absence need explicit handling; inferred TypeScript types are not
runtime input validation. Choose indexes from actual plans/cardinality, not every
WHERE/JOIN column, and avoid redundant unique/index definitions.

## Queries, transactions, and migrations

PostgreSQL, SQLite, MySQL, LibSQL and edge drivers differ in returning, upsert,
transactions, batching, connection lifetimes and async APIs. Do not copy PostgreSQL
syntax into every adapter. Pagination needs a total order/tiebreaker; consider
keyset behavior for mutable large datasets. Avoid shadowing a schema table with
a same-named query result as in the upstream const users examples. Review generated
migration SQL and data conversion; custom/manual migrations can be necessary,
while altering applied history is unsafe. drizzle-kit push can change/destructively
replace schema and requires target verification/authority, not merely a dev label.
No fixed bundle size or universal runtime claim replaces the actual driver evidence.

## Primary documentation

- [Relation API and foreign-key distinction](https://orm.drizzle.team/docs/relations).
- [Update and returning semantics](https://orm.drizzle.team/docs/update).
- [Version-specific migration and relation changes](https://orm.drizzle.team/docs/v0-v1-changes).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
