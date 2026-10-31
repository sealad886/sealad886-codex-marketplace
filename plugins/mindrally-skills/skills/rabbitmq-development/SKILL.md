---
name: rabbitmq-development
description: "Use when designing RabbitMQ exchanges/queues, delivery acknowledgments, publisher confirms, retry/DLX handling, or broker integration."
---

# RabbitMQ Development

## When to invoke

Use for designing RabbitMQ exchanges/queues, delivery acknowledgments, publisher confirms, retry/DLX handling, or broker integration.

## Inputs and evidence

Inspect broker/client/protocol versions, queue type/durability, routing, publisher confirms, consumer ack/prefetch and failure requirements. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define routing and end-to-end delivery/idempotency semantics.
2. Declare supported queue/exchange topology and scoped permissions.
3. Implement confirmed publishing, bounded consumer work and explicit retry/dead-letter behavior.
4. Test unroutable messages, duplicate delivery, reconnect, crash and broker recovery.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Isolated broker tests demonstrate routing, confirms/returns, ack/retry behavior, duplicates and recovery under the required queue type.

## Must not

Do not infer durable business delivery from delivery_mode alone or requeue failing messages indefinitely. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
