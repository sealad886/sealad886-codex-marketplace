# Koa TypeScript Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Middleware and state

- Koa core supplies no router/body parser; select the installed maintained packages, such as @koa/router, rather than assuming bundled middleware.
- await next() enters downstream middleware; code after it unwinds upstream. Short-circuit intentionally when responding early.
- ctx.state is an intended per-request namespace; type it and avoid leaking per-request identity through shared global context.

## Validation and security

- Body parsing needs content-type/size limits and runtime schemas; TypeScript interfaces do not validate external input.
- Zod error fields and middleware imports vary by major version; use the installed public API rather than copying error.errors from another version.
- Constrain JWT algorithm/issuer/audience if tokens are used; CORS and headers do not authorize resources.
- Use app.callback() for HTTP integration tests and close created servers/connections; redact logs and unexpected error details.

## Primary documentation

- [Primary documentation](https://koajs.com/) — Koa uses async onion middleware, per-request context/state, and separately supplied middleware.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
