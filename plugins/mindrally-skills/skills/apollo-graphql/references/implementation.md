# Apollo GraphQL Best Practices: implementation guidance

## Client and operation boundaries

Apollo Client 4 moves React integrations to `@apollo/client/react`; older major
versions have different exports. Use its current ErrorLink/error-class API rather
than mixing an older `onError` callback signature into a v4 setup. Prefer generated
operation document types and fragments; schema scalar types such as DateTime need
actual server definitions. A field called user is not less correct than getUserById.
Create isolated server-rendered client/cache instances per request where user data
is involved. Never share a server DataLoader across authorization scopes.

## Cache, pagination, and errors

Define stable cache identity with `keyFields` and field arguments with `keyArgs`.
Do not blindly concatenate all incoming lists: handle a new filter, first page,
refetch, repeated edges, ordering, and endCursor/pageInfo correctly. Use a suitable
pagination helper only when the server contract matches. Mutation update functions
must handle partial results and optimistic rollback. With partial-data policies,
check which fields exist before rendering. Expose a defined refetch function in
error UI; avoid the upstream example's undefined refetch and mismatched hook data.
HTTP batching requires server support; batching and retries need operation limits
and mutation side-effect semantics.

## Primary documentation

- [Apollo Client 4 migration and exports](https://www.apollographql.com/docs/react/migrating/apollo-client-4-migration).
- [ErrorLink current error interface](https://www.apollographql.com/docs/react/api/link/apollo-link-error).
- [Pagination merge and keyArgs contracts](https://www.apollographql.com/docs/react/pagination/core-api).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
