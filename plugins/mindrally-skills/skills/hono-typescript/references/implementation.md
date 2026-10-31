# Hono TypeScript Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Routing and types

- Use Hono environment generics for Bindings and Variables where applicable; request validation complements static typing.
- Keep the route type returned by chained definitions when using RPC/testClient inference; separate declarations can lose inferred routes.
- Use app.route for subapps and verify middleware ordering and wildcard behavior for the installed major version.

## Runtime and security

- Cloudflare c.env bindings, Node adapters, Bun exports, and Deno.serve are different deployment entrypoints; select one supported target.
- Use HTTPException/onError deliberately; avoid returning stack traces or logging credentials.
- Validate input with the established validator, then enforce ownership and roles on the server. CORS is not authorization.
- Use request-level tests or typed testClient with supplied environment fixtures; exercise rejected inputs and missing bindings.

## Primary documentation

- [Hono getting started](https://hono.dev/docs/getting-started/basic) — Hono supports distinct runtime adapters and standard Request/Response routing.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
