---
name: kafka-development
description: "Use when building Kafka producers, consumers, schemas, topic partitioning, stream processing, or CDC pipelines."
---

# Kafka Development

## When to invoke

Use for building Kafka producers, consumers, schemas, topic partitioning, stream processing, or CDC pipelines.

## Inputs and evidence

Inspect broker/client versions, topic configuration, partition keys, schema format/registry, delivery semantics, and external side effects. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define ordering, durability, retention, and duplicate-handling requirements.
2. Implement producers with supported reliability settings and bounded delivery error handling.
3. Process and commit consumer offsets with explicit failure/DLT and idempotency behavior.
4. Test retries, rebalances, crash recovery, schema evolution, and observed lag.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Integration tests bind produced events, durable effects, committed offsets, duplicates, and recovery outcomes.

## Must not

Do not silently discard timed-out messages or claim global ordering/exactly-once from client flags. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
