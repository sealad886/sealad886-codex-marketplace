# FastAPI Microservices Serverless: implementation guidance

## Runtime and service boundaries

FastAPI is ASGI; serverless support requires a compatible hosting/runtime adapter
and verified lifespan behavior. Async handlers should await actual asynchronous
I/O, while blocking libraries need an appropriate thread/process boundary. CPU
work does not become nonblocking by adding async. Reused instances can retain
pools/clients but per-request private state must not leak. Scale pool/concurrency
limits across all instances and provider quotas.

## Gateways, state, and operations

Redis, an API gateway, Prometheus and Grafana are optional choices, not required
for statelessness. OpenTelemetry is observability, not security middleware or an
OAuth2 mechanism. Gateway authentication does not remove application resource/
permission checks. Verify trusted forwarded headers/path prefixes and CORS.
In-process background tasks are not durable after serverless response/lifetime
termination; use an approved durable queue for required work. Bound retries and
use idempotency keys where effects can repeat. Redact traces/logs, isolate cache
keys by authorization scope, and separate local emulation from authorized hosted
load/failure/deployment validation.

## Primary documentation

- [Sync versus async execution](https://fastapi.tiangolo.com/async/).
- [Deployment/runtime concerns](https://fastapi.tiangolo.com/deployment/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
