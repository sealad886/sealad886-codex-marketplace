# React Query server state: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- For TanStack Query v5 use `@tanstack/react-query` and object-form options, such as `useQuery({queryKey, queryFn})`; do not copy v3 positional examples.

- In v5 `gcTime` controls retention of inactive queries; `staleTime` controls freshness. Neither guarantees the server data remains unchanged.

- Use a stable QueryClient; create server-rendering clients per request rather than sharing authenticated caches across users.

- Include every input affecting fetched data in the query key, including tenant or account context where appropriate.

- Fetch functions must reject or throw on HTTP failures; native fetch resolves ordinary error statuses. Pass cancellation signals when supported.

- For v5 pagination use placeholder data intentionally; infinite queries require an initial page parameter and next-page logic.

- Cancel relevant reads before an optimistic update, retain rollback state, and reconcile with the server on settlement; handle overlapping mutations explicitly.

- V5 query-level onSuccess/onError/onSettled callbacks were removed; use appropriate cache-level handling or state-driven UI. Keep client UI state separate.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [V5 uses object signatures, gcTime, changed pagination, and removed query callbacks.](https://tanstack.com/query/latest/docs/framework/react/guides/migrating-to-v5)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
