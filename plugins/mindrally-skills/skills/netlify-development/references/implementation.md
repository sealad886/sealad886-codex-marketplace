# Netlify Development Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Functions and configuration

- Standard Node functions and Edge runtimes have different APIs/import capabilities; inspect installed types and current platform limits rather than retaining a fixed timeout table.
- Use Request/Response handlers and exported config only where supported; netlify.toml remains canonical for applicable build and ordered routing configuration.
- Background functions return acceptance rather than final results; define durable job identity, idempotency and failure/status reporting.
- Scheduled invocation semantics and limits are platform-specific; local function invocation does not prove a production schedule ran.

## Storage, images and environment

- Choose Blobs, a database or another store from consistency, transaction, query and retention needs; Blobs is not mandatory for all persistent state.
- Use documented global/deploy store constructors and inspect current consistency/concurrency APIs; do not assume an arbitrary deployID option creates deploy-scoped storage.
- Validate upload type/size/content and derive safe unique keys; enforce owner access on status/result endpoints.
- Configure Image CDN remote sources narrowly and URL-encode inputs; framework remotePatterns alone does not prove CDN integration.
- Secret variables belong in approved scopes/destinations; runtime env mutation is not durable account configuration. Do not print plain environment lists.
- Keep .netlify tooling output and function source outside publish artifacts; inspect preview data isolation before publication.

## Primary documentation

- [Primary documentation](https://docs.netlify.com/build/functions/overview/) — Netlify distinguishes function execution types, configuration and current platform limits.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
