# Next.js React Redux TypeScript Cursor Rules: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Store and rendering

- Do not create a module-global Redux store shared across server requests; Server Components should not read/write Redux context.
- Use Redux for shared mutable client state where needed; Server Component data fetching need not be duplicated into a global store.
- Preserve hydration agreement and deliberately reset route/user-specific state; persisted caches must not cross identities.

## Framework and tests

- App Router metadata differs from Pages Router Head usage; choose the actual router APIs.
- Memoization, avoiding inline callbacks, and stable keys are contextual; index keys are unsafe for mutable/reordered identity, not universally forbidden.
- Use established forms/styling/i18n libraries, not every package in the source list.
- Test keyboard/error/loading states and server authorization; DOMPurify is needed for selected HTML boundaries, not ordinary escaped JSX.

## Primary documentation

- [Primary documentation](https://redux.js.org/usage/nextjs) — Redux’s Next.js guidance requires request-local stores, client providers and no RSC store reads/writes.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
