---
name: websocket-development
description: "Use when implementing WebSocket authentication, message validation, reconnect/replay, fanout, or slow-consumer handling."
---

# WebSocket connection and message contracts

## When to invoke

Use when implementing WebSocket authentication, message validation, reconnect/replay, fanout, or slow-consumer handling.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect runtime/server/client versions, handshake/auth model, message schema, reconnect semantics, quotas, and connection ownership.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define connection authorization and per-message/channel permissions.
2. Implement bounded message handling, liveness, reconnect, and explicit delivery semantics.
3. Test disconnects, duplicates, expired access, malformed messages, and slow consumers.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run protocol/integration checks for handshake denial, expired auth, message limits, reconnect/replay, shutdown, and slow-consumer behavior.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
