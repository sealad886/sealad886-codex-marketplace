# Modern Web Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Rendering and interfaces

- Next.js App Router Server Components and client components have different capabilities; use client for state, events and browser APIs.
- Suspense is useful for actual suspension/streaming boundaries, not a requirement around every client component.
- Do not force TypeScript type/interface, semicolon, styling or component-order preferences over repository conventions.

## Data and runtime

- Choose existing Supabase/GraphQL/cache integrations based on need; a realtime database client is not a universal local-state manager.
- Enforce authorization/RLS at the server/database boundary and never expose privileged credentials through client imports.
- Verify current hosted storage offerings instead of prescribing retired Vercel KV products.
- Profile waterfalls, image behavior and code splitting; dynamic imports and caching need correct error and invalidation behavior.

## Primary documentation

- [Primary documentation](https://nextjs.org/docs/app/getting-started/server-and-client-components) — Server and Client Components are selected by data access and interactive/browser capabilities.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
