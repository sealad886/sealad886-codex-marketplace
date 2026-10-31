# Firebase Development: implementation guidance

## Authorization and consistency

Client Firestore/Storage requests are governed by applicable Security Rules;
server/Admin libraries bypass Firestore Rules and use IAM, so enforce application
resource authorization too. Authentication alone does not grant ownership.
Queries must satisfy rule constraints; rules are not post-query filters. Design
indexes and cursor ordering for actual access patterns. Transactions can rerun:
keep callbacks free of external side effects. Batched writes and transactions
have different read/conflict semantics and platform limits.

## Files, functions, and offline state

Validate upload paths, sizes, content/metadata and allowed owners. Signed or tokenized
URLs grant bearer-like access for their lifetime; do not treat every download URL
as revocable per-request authorization. Functions may receive duplicate events and
need idempotency, time/resource limits and redacted logs. Offline persistence is
SDK/platform-specific and can retain sensitive data on shared devices; handle pending
writes, conflicts, logout/cache state and reconnection. Firebase web configuration
is generally public application identity, while service-account secrets remain private.
Angular or any particular service-layer architecture is optional.

## Primary documentation

- [Rules and server library boundaries](https://firebase.google.com/docs/firestore/security/rules-conditions).
- [Transaction retry and batch semantics](https://firebase.google.com/docs/firestore/manage-data/transactions).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
