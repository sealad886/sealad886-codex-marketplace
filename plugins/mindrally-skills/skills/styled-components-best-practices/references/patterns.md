# Styled-components runtime and styling: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Styled-components v6 includes TypeScript definitions; do not add the older @types package without checking the installed major.

- Define styled components outside ordinary render paths to preserve identity; constant interpolation alone does not create a new class on every render.

- Use transient $props or supported shouldForwardProp rules for styling-only values; source button variant/size props should not leak arbitrarily to DOM attributes.

- Type DefaultTheme against actual tokens and keep providers aligned across tests, client, and server.

- High-cardinality frequently changing values can be better expressed through CSS custom properties or inline values than generating many style rules.

- SSR integration differs by framework/router and streaming version; a compiler flag alone may not collect and hydrate server styles.

- Seal ServerStyleSheet in finally for manual server rendering; isolate each request’s style collection.

- Retain visible focus, semantic elements, appropriate names, and reduced-motion handling; removing outlines without an equivalent indicator is unsafe.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Styled-components v6 is written in TypeScript and has generation-specific migration behavior.](https://styled-components.com/docs/faqs)
- [Transient props and style collection have explicit APIs.](https://styled-components.com/docs/api)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
