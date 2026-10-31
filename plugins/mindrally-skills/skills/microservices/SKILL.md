---
name: microservices
description: "Use when designing service boundaries, inter-service contracts, retries, asynchronous jobs, observability, or graceful shutdown."
---

# Microservices Development

## When to invoke

Use for designing service boundaries, inter-service contracts, retries, asynchronous jobs, observability, or graceful shutdown.

## Inputs and evidence

Inspect domain ownership, existing service topology, API/event contracts, state consistency, failure budgets, and deployment authority. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Justify service boundaries and define data ownership and observable contracts.
2. Implement bounded synchronous/asynchronous communication with explicit timeouts and idempotency.
3. Propagate context, authenticate/authorize boundaries, and own workers/goroutines through shutdown.
4. Test partial failures, retries, duplicate events and cross-service user journeys.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Contract and integration/failure tests show user-visible behavior under partial failure and orderly shutdown.

## Must not

Do not split services or introduce infrastructure merely to match a preferred architecture. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
