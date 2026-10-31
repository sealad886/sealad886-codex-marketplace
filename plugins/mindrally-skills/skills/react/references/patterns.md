# React: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use `className` in React JSX. A Svelte-style `class:` directive is not React syntax; select conditional classes with ordinary JavaScript or the existing class helper.

- Keep Hooks at component or custom-Hook top level. Declare dependencies honestly; remove an unnecessary effect instead of suppressing dependency checking.

- Treat `useMemo`, `useCallback`, and `memo` as measured optimizations. Correctness must not depend on retained memo caches.

- Use the project’s CSS system; Tailwind, inline dynamic values, and ordinary CSS are choices rather than React requirements.

- React Server Components require a supporting framework/build pipeline. Do not introduce `use client` into an ordinary client-only application.

- Suspense handles supported suspending resources and lazy components; wrapping arbitrary effect-driven fetching does not make it suspend.

- Use semantic controls, labels, focus handling, stable list identity, and explicit loading/error/empty states.

- Follow the project’s TypeScript and export conventions; function declarations, arrow functions, interfaces, and aliases each remain valid.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Memoization is a performance optimization without semantic guarantees.](https://react.dev/reference/react/useMemo)
- [React JSX uses className and JavaScript expressions.](https://react.dev/learn/writing-markup-with-jsx)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
