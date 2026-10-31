# Cloudflare Development Best Practices: implementation guidance

## Storage and coordination

KV is eventually consistent and does not provide an atomic read-increment-write
counter. The upstream KV rate limiter races, resets its TTL per write, and is
unsuitable for strict rate enforcement. Choose a documented rate-limit binding
with understood locality or a Durable Object for required coordination. Generate
binding types from the actual Wrangler configuration. Use parameterized D1
statements and deliberate indexes; a unique email constraint already creates an
index, so avoid a redundant duplicate. Paginate KV/R2 listings and enforce object
ownership; prefixes alone are not access control.

## Runtime, background tasks, and tests

Durable Objects need correct class export/binding/migration names and storage
backend; hibernation requires its documented WebSocket APIs. waitUntil extends a
bounded invocation lifetime, not a durable job queue. Use Queues or another approved
primitive for work requiring durable retries. Cache only eligible responses with
correct user/headers/key variation; never publish authenticated data universally.
Avoid reusing consumed response streams, and pass the actual execution context
instead of the upstream undefined ctx. Use current Workers/Vitest testing APIs
rather than deprecated unstable_dev snippets. Deployment/secrets/config changes
need explicit task authority.

## Primary documentation

- [KV eventual consistency and per-key write limits](https://developers.cloudflare.com/kv/reference/faq/).
- [Rate-limit binding consistency scope](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/).
- [Bounded execution context lifetime](https://developers.cloudflare.com/workers/runtime-apis/context/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
