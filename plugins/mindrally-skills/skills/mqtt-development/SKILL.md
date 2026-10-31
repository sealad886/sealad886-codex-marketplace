---
name: mqtt-development
description: "Use when implementing MQTT topics, QoS, persistent sessions, retained state, reconnect behavior, or device messaging security."
---

# MQTT Development

## When to invoke

Use for implementing MQTT topics, QoS, persistent sessions, retained state, reconnect behavior, or device messaging security.

## Inputs and evidence

Inspect MQTT 3.1.1 versus 5 support, broker/client versions, topic ACLs, QoS/session settings, offline queues and command idempotency. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define topic ownership, payload schema and end-to-end delivery requirements.
2. Configure supported QoS, sessions, retained/message-expiry and last-will behavior.
3. Implement authenticated TLS transport, scoped subscriptions and bounded reconnect/offline queues.
4. Test duplicate messages, disconnect/reconnect, session loss, stale commands and authorization.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Isolated-broker tests prove scoped access, expected session/QoS behavior and recovery without duplicate business effects.

## Must not

Do not treat QoS 2 as a financial transaction guarantee or silently drop offline messages. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
