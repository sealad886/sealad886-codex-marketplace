# GraphQL: implementation guidance

## Schema and execution

GraphQL types validate operation structure but not every domain rule; custom scalars
need actual coercion/serialization. Choose nullability carefully because non-null
errors propagate to the nearest nullable boundary. Top-level mutation fields execute
serially, but GraphQL does not create an atomic database transaction or roll back
previous successful fields. Enforce coherent write invariants in the resolver/data
layer. Return useful typed outcomes and safe errors without exposing internal data.

## Loading, clients and security

Scope DataLoader instances/caches to an appropriate request and authorization context;
return results in input-key order and handle missing records deliberately. Bound
page sizes and use stable cursor ordering. Generated clients/types are optional
choices and must track the actual schema. Gatsby useStaticQuery is build-time
functionality with its own static query constraints, not live user-private data
fetching; query filenames need no universal use prefix. Query depth/complexity,
timeouts, rate/resource limits and transport/CSRF controls work together. Persisted
query allowlists can limit operations, while automatic persisted-query hashing alone
is not authorization. Schema evolution often uses additive/deprecation workflows;
API versioning is a project contract choice.

## Primary documentation

- [Serial mutations versus database transactions](https://graphql.org/learn/mutations/).
- [Authorization and bounded query work](https://graphql.org/learn/security/).
- [Per-request cache and key-order contract](https://github.com/graphql/dataloader).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
