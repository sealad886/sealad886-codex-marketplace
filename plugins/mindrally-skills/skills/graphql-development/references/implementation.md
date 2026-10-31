# GraphQL Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Schema and execution

- Choose nullable fields intentionally: non-null failures can propagate to a parent; document partial-data handling.
- Use cursor or offset pagination according to ordering and consistency requirements, with explicit bounds.
- Batch per request and identity; shared DataLoader caches can expose data across users.

## Clients and security

- Use the existing Apollo, urql, or Genql setup; generated operations must match the deployed schema.
- Keep authorization centralized in the business layer invoked by resolvers; authentication alone does not authorize a field.
- Limit expensive queries using measured cost/depth/pagination controls; sanitize error details and protect cache identities.
- Test loading, partial results, rejected mutations, optimistic rollback, and subscription teardown.

## Primary documentation

- [GraphQL authorization](https://graphql.org/learn/authorization/) — Authorization belongs in the business layer and remains necessary after authentication.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
