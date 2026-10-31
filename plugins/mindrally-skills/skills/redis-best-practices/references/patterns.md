# Redis data and cache behavior: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use `SET key token NX EX 30` for conditional set with expiry; `SETNX key value EX 30` is invalid. Lock release must verify ownership atomically; expiry alone does not provide a general distributed correctness guarantee.

- Pipelines reduce round trips but are not automatically atomic. MULTI/EXEC queues commands atomically; WATCH detects optimistic conflicts and requires retry handling.

- Cache-aside updates must account for stale-reader races and failed invalidation; database write plus cache write is not one atomic transaction.

- Choose strings, hashes, sets, sorted sets, lists, or streams by access pattern. Bound large reads and consumer-group pending work.

- Redis Pub/Sub is ephemeral at-most-once delivery; use Streams or another durable queue when replay and acknowledgement are requirements.

- SCAN is incremental and may return duplicates during mutation; iterate the cursor to completion and scope deletions precisely. Cluster multi-key operations need compatible hash slots.

- Use ACL users, TLS, network restrictions, bounded connection pools, and secret storage; command renaming is not a replacement for access control.

- Persistence, replication, Sentinel, and Cluster solve different needs; measure recovery and failover against the application’s loss budget. CONFIG SET and persistence changes require operational authority.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [SET supports conditional NX and expiry options.](https://redis.io/docs/latest/commands/set/)
- [Redis Pub/Sub has at-most-once delivery semantics.](https://redis.io/docs/latest/develop/pubsub/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
