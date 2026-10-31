# Next.js React TypeScript: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Components and state

- Client Components are appropriate for state management, events and browser APIs; minimizing boundaries must not prevent required interactivity.
- A use client entry marks its imported client graph; keep secrets/server-only modules outside that graph.
- Suspense handles suspension boundaries, not every client component; nuqs is optional and must match router/version needs.

## Data and performance

- Next.js data caching, request APIs and async route params changed across releases; verify installed contracts.
- Core Web Vitals currently uses INP rather than retired FID; measure actual LCP/CLS/INP for relevant pages.
- Choose image formats/sizes and lazy loading according to criticality; do not lazy load the LCP image indiscriminately.
- Use accessible native semantics and existing styling primitives; verify keyboard/focus and meaningful loading/error states.

## Primary documentation

- [Primary documentation](https://nextjs.org/docs/app/getting-started/server-and-client-components) — Client Components support state/events/browser APIs while server capabilities stay in Server Components.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
