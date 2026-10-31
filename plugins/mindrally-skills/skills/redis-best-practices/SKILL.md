---
name: redis-best-practices
description: "Use when implementing Redis caching, structures, expiration, streams, transactions, connection handling, or operational diagnostics."
---

# Redis data and cache behavior

## When to invoke

Use when implementing Redis caching, structures, expiration, streams, transactions, connection handling, or operational diagnostics.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Redis/client versions, topology, consistency and durability needs, key ownership, TTLs, and authorized diagnostic access.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Choose structures and expiry policy from the data and failure contract.
2. Implement atomic boundaries, bounded operations, and deliberate cache/messaging semantics.
3. Verify contention, reconnect, expiration, and failure behavior without changing live configuration unexpectedly.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Use isolated Redis tests for expiry, concurrent updates, invalidation failure, and reconnects; report topology/failover tests not performed.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
