# RabbitMQ Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Queue and version semantics

- Durable queues preserve metadata; message persistence, replication and publisher confirms are separate durability concerns.
- Current classic queues are not replicated; classic mirrored queues/ha-mode were removed in RabbitMQ4, so use quorum/streams when their semantics fit.
- Lazy queue options, priorities and storage behavior depend on queue type/version; avoid fixed throughput, memory or queues-equal-cores claims.
- A direct exchange routes to every matching binding/queue, so exact keys do not inherently mean unicast.

## Reliability and consumers

- Publisher confirms and mandatory returns establish different outcomes; handle both and make retry effects idempotent.
- Acknowledge after durable successful processing, not merely receipt; bound prefetch/concurrency and avoid infinite requeue loops.
- Dead lettering can have loss/overflow/retry policy implications; test the selected type’s guarantees rather than assuming a DLX is durable.
- Channels share connections but are not lightweight TCP connections; observe library thread-safety and recovery constraints.
- RabbitMQ queues/streams have ordering/redelivery semantics, not Kafka-style partitions for all event sourcing.

## Primary documentation

- [Primary documentation](https://www.rabbitmq.com/docs/classic-queues) — RabbitMQ4 classic queues are non-replicated; quorum queues/streams are recommended where replicated data safety is required.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
