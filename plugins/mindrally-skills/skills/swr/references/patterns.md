# SWR cache and mutation behavior: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Keys may be strings, arrays, objects, or functions according to supported SWR versions; a URL alone may omit auth/tenant identity.

- A function key is conditional only if it returns falsy or throws while dependencies are unavailable; returning `/users/${undefined}` still starts a request.

- Fetch does not reject non-2xx responses automatically; mutation fetchers must check status for rollbackOnError to work.

- Use mutate from the relevant SWRConfig cache context; a global mutate may not target an isolated provider.

- Avoid optimistic spreading of undefined data with forced casts; define creation/update states and restore prior data on failure.

- Revalidation on mount depends on options and cached-data state; deduplication is not a universal no-duplicate-network guarantee.

- Infinite queries need deterministic keys, explicit next-cursor/end behavior, and proper URL encoding; avoid arbitrary short-page assumptions unless the API guarantees them.

- SSR/framework data APIs and SWR client caches have separate responsibilities; use current framework patterns and request-scoped authenticated data.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Function keys skip requests only on falsy values or thrown missing-dependency access.](https://swr.vercel.app/docs/conditional-fetching)
- [Mutation options support optimistic data, rollback, and cache population.](https://swr.vercel.app/docs/mutation)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
