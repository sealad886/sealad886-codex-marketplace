# TanStack Query v5 workflows: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- V5 uses object-form query APIs, gcTime for inactive retention, and dedicated Suspense query hooks; choose options from the installed minor.

- A QueryClient can be created with stable component state or a factory; it must not be recreated every render, and SSR clients should not leak user data across requests.

- Inline options objects are supported. queryOptions improves shared type inference and co-location, but is not mandatory for every single use.

- isPending and isLoading differ for queries: a disabled uncached query may be pending without an active fetch. Render a spinner from actual fetch semantics.

- Mutation retries can duplicate writes unless idempotent; do not enable a default retry merely because the API permits it.

- Use generic hook types that preserve select transformations; a wrapper fixed to User data cannot correctly accept every transformed result.

- Keys should include all variables influencing fetched data; weakening identity to improve reuse can leak or return wrong tenant/filter data.

- Suspense/error boundaries and ensureQueryData have freshness semantics; preloading cannot guarantee navigation has no pending state.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [queryOptions co-locates reusable typed keys/functions/options.](https://tanstack.com/query/latest/docs/framework/react/guides/query-options)
- [Freshness, retry, garbage collection, and structural sharing have configurable defaults.](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
