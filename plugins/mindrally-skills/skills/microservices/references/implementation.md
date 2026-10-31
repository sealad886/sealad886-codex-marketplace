# Microservices Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Boundaries and resilience

- Choose services only where ownership/scale/deployment needs justify distributed complexity; Redis, gateways and serverless are optional.
- OAuth is an authorization framework; authentication may use OIDC or another explicit identity mechanism.
- Set end-to-end deadlines and retry budgets; use idempotency for effects and avoid retry amplification across layers.

## Python, Go and operations

- In FastAPI, async handlers must not call blocking I/O directly; durable work needs an appropriate queue rather than unowned background tasks.
- In Go, propagate context where operations need cancellation/deadlines and bound goroutine/connection lifetimes.
- Use trace context and structured logs across boundaries, while separating user data from telemetry.
- Test graceful shutdown, backpressure, worker redelivery and eventual consistency; dashboards are not proof of resilience.

## Primary documentation

- [Primary documentation](https://opentelemetry.io/docs/concepts/signals/traces/) — Distributed traces propagate causal context across service boundaries for end-to-end observation.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
