# Optimized Next.js TypeScript Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Rendering and data

- Server Components can reduce client payload for server-owned work; client state, effects and events remain appropriate where required.
- Dynamic imports help selected noncritical code but can add waterfalls; Suspense should correspond to actual asynchronous boundaries.
- Choose query/state/cache tools already used and verify user/tenant cache isolation and invalidation.

## Assets and measurements

- Optimize dimensions, formats and responsive delivery for actual images; do not lazy load critical LCP imagery by default.
- Measure LCP, CLS, INP, server latency and resource cost as relevant; synthetic scores alone may miss real user conditions.
- Keep error/loading/fallback UI usable on slow or failed networks and verify keyboard/screen-reader behavior after rendering changes.
- Avoid stylistic rewrites or adding Zustand/React Query/Tailwind solely as optimization claims.

## Primary documentation

- [Primary documentation](https://nextjs.org/docs/app/guides/production-checklist) — Next.js production checks cover rendering, caching, assets, security and measured performance.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
