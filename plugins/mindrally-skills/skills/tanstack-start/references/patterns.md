# TanStack Start full-stack boundaries: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Current React Start uses @tanstack/react-start and its Vite plugin; old @tanstack/start/config app.config.ts and server.preset examples are generation-specific.

- Server-function builder names changed across releases, including validator/inputValidator; inspect installed types and current migration docs rather than mechanically renaming.

- Server execution is not authorization. Validate caller identity, record access, and CSRF/session requirements within callable server functions.

- Use explicit POST semantics for mutations; a client-visible RPC wrapper must not turn a default read endpoint into an unauthenticated write.

- Use the current server route API for raw HTTP. Verify webhooks over the required raw body before parsing payloads.

- Streaming promise/defer/Await contracts and deployment adapters vary by generation; verify rejection and disconnect behavior in the actual build.

- Keep secrets in supported server-only modules/runtime bindings; a filename or process.env spelling alone does not prove exclusion from client output.

- Do not serialize raw internal error details to clients. Provider provisioning, secrets, and deployment remain separately authorized effects.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Current server functions use @tanstack/react-start with method, validation, and handler semantics.](https://tanstack.com/start/latest/docs/framework/react/guide/server-functions)
- [Current migration docs change builder methods including inputValidator back to validator.](https://tanstack.com/start/latest/docs/framework/react/migrate-from-release-candidate)
- [Current Start integrates through tanstackStart in vite.config.ts.](https://tanstack.com/start/latest/docs/framework/react/guide/static-prerendering)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
