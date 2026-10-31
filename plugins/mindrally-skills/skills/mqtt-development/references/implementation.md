# MQTT Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Protocol and delivery

- QoS 0/1/2 describe delivery between protocol peers; QoS 2 does not guarantee exactly-once business effects across an entire application.
- MQTT 3.1.1 cleanSession differs from MQTT 5 Clean Start plus Session Expiry; user properties/message expiry are MQTT 5 features.
- Retained messages represent broker-held latest state, not a history; avoid retained destructive commands without deliberate staleness protection.
- Maximum topic levels and allowed QoS are broker/provider limits, not universal AWS-derived MQTT restrictions.

## Device security and resilience

- Authenticate clients and authorize publish/subscribe topics separately; TLS version negotiation is transport security, not a replacement for identity checks.
- Use stable unique client IDs according to session ownership; generic connection pooling can conflict with session identity.
- Bound reconnect backoff, offline memory and command expiry; account for duplicates and application acknowledgments.
- LWT depends on protocol disconnect/session conditions; test graceful disconnect, abrupt loss and broker behavior with a real isolated broker.

## Primary documentation

- [Primary documentation](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) — MQTT 5 defines QoS exchanges, Clean Start/Session Expiry, retained messages and protocol properties.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
