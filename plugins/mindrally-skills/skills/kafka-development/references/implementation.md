# Kafka Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Ordering and producer semantics

- Ordering is per partition; increasing partition count can remap keys and affect application ordering assumptions. Null-key partitioning is client/version-specific, often sticky rather than round robin.
- acks=all waits for the current in-sync replicas, with durability also governed by min.insync.replicas and failure configuration.
- Idempotent producers prevent certain retry duplicates; manual offset commits alone do not create exactly-once processing.
- Treat default linger, batching and retention values as version/configuration-dependent, and use a bounded delivery timeout.

## Processing and recovery

- Commit only offsets whose effects are durably completed; successfully publishing a failure record may require its own atomicity/confirmation design.
- External database/API effects need idempotency or coordinated transactions; Kafka transactions do not automatically make arbitrary external effects exactly once.
- Use schema compatibility rules for the selected registry and format; not every deployment needs Confluent.
- For Streams, choose windows/grace/state retention from event-time semantics; verify replay and late data instead of inventing fixed retry success percentages.

## Primary documentation

- [Primary documentation](https://kafka.apache.org/41/configuration/producer-configs/) — Producer acknowledgments, idempotence, partitioner behavior, delivery timeouts and batching are separately configured.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
