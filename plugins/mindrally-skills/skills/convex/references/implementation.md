# Convex Development Guidelines: implementation guidance

## Functions and transactions

Use generated query/mutation/action constructors with runtime argument validators;
add return validation where needed. Authentication is not authorization: the
upstream getItems reads all users despite retrieving identity, and createItem
omits required schema status. Bind reads and writes to the caller's permitted
resources. Queries/mutations have transactional/deterministic restrictions; external
side effects belong in actions. Separate action runQuery/runMutation calls are
separate transactions and may observe different state. Use internal functions for
unexposed operations and idempotency for repeatable external actions.

## Data, files, scheduling, and UI

Choose indexes for access patterns without claiming every filter always needs one.
Use pagination for unbounded collections. first returns one matching record, not
proof of uniqueness; use the intended uniqueness invariant. Protect upload URL
issuance, file metadata reads/writes, and download access; storage IDs are not
permission checks. Validate webhook signatures on raw bodies before processing
and deduplicate events. Schedule internal jobs with the correct UTC/interval
semantics. React, Tailwind, Shadcn, and Server Components are optional client
choices, not Convex backend requirements. Validate subscription loading/errors.

## Primary documentation

- [Validators and access control on every public function](https://docs.convex.dev/understanding/best-practices).
- [Action and transaction boundaries](https://docs.convex.dev/functions/actions).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
