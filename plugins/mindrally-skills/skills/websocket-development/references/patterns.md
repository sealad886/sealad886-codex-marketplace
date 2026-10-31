# WebSocket connection and message contracts: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use TLS for production and validate origins where browser ambient credentials are used; CORS rules alone do not govern WebSocket authorization.

- Browser WebSocket cannot set arbitrary handshake headers or send protocol ping frames through the standard JS API; choose supported cookie/subprotocol/application-heartbeat patterns.

- Recheck authorization for sensitive messages and channel subscriptions and account for session expiry/revocation.

- The browser WebSocket API provides no automatic receive backpressure; bound server/client queues, inspect bufferedAmount where useful, and disconnect or shed work deliberately.

- Reconnect with jitter/backoff and a cap; buffering offline writes requires IDs, ordering, deduplication, expiry, and idempotent acknowledgement semantics.

- Native Node client availability/stability differs by version and is distinct from a server implementation; use installed runtime docs.

- Cross-server brokers, sticky sessions, binary formats, and dead-letter queues are optional and do not automatically make delivery durable or exactly once.

- Release timers/listeners/subscriptions on close and test rolling deploy/shutdown; logs must not contain tokens or sensitive payloads.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [The browser WebSocket API lacks automatic backpressure.](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
