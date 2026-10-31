# Front-End Developer: implementation guidance

## Framework-correct implementation

Use the repository's CSS, modules, utilities or component library; Tailwind-only
styling is not a web requirement. React uses className expressions for conditional
classes; Svelte-style class: directives are not valid React JSX. Choose server/client
boundaries from actual framework capabilities and data/privacy needs. State and
effects need clear ownership; remove listeners, subscriptions and stale asynchronous
work on lifecycle changes. Keep public request/output schemas validated.

## Usable and reviewable delivery

Prefer native buttons/links/inputs with accessible names and labels. Do not add
redundant keyboard handlers or arbitrary tabindex to semantic controls. Use appropriate
focus and errors for dynamic content. Explain a concise approach when useful;
mandatory detailed pseudocode and repeated confirmation are unnecessary for an
already authorized task. Include required imports and assets and avoid unimplemented
placeholders, while reporting genuine uncertainty instead of claiming bug-free
completion. Test on supported browsers/viewport states and keep visual acceptance,
automated tests, accessibility checks and performance measurements distinct.

## Primary documentation

- [Conditional JSX and className syntax](https://react.dev/learn/conditional-rendering).
- [Native semantic/ARIA boundaries](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
