# MongoDB Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Data and queries

- Single-document operations are atomic; multi-document transactions have topology and read/write concern requirements.
- Choose embedding/references by update/read patterns and document growth; bound arrays and document sizes.
- Use explain and representative cardinality to assess compound/partial indexes and aggregation plans.

## Application integration

- Payload and Mongoose are separate/version-specific integrations; do not assume every current Payload MongoDB adapter is an Express/Mongoose stack.
- Use unknown plus narrowing for untrusted values rather than banning unknown and encouraging unsafe casts.
- Validate query objects and allowlisted operators; string sanitization alone does not prevent authorization or query injection defects.
- Bound pagination and transactions, and test migrations/data transformations with recovery evidence.

## Primary documentation

- [Primary documentation](https://www.mongodb.com/docs/manual/core/transactions/) — Single-document writes are atomic and multi-document transactions carry deployment/concern and performance considerations.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
