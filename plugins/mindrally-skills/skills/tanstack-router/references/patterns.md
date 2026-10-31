# TanStack Router route contracts: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- File-based and code-based routing are both supported; createFileRoute and a particular Vite plugin are not requirements for code-based trees.

- Runtime input still needs validation; TypeScript does not prove untrusted URLs, responses, or thrown errors match a type.

- Use validateSearch with the chosen supported schema/adapter or validator; Zod is optional and malformed input/default coercion needs explicit behavior.

- beforeLoad can guard route UI and redirects but is not server authorization. APIs/server functions must independently validate the caller.

- Update router context when auth state changes, and trigger supported invalidation so guards/loaders do not retain stale permissions.

- ensureQueryData may reuse stale cached data; choose fetchQuery, invalidation, or revalidateIfStale behavior from freshness requirements.

- Typed Links are useful for internal navigation; ordinary anchors remain valid for external/document navigation and intentional reloads.

- Keep generated route files under tool ownership and use current plugin packages; test deep links, preloading, redirect targets, and pending/error boundaries.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [beforeLoad guards UI; server data endpoints still require authorization.](https://tanstack.com/router/latest/docs/framework/react/guide/authenticated-routes)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
