# Design Systems Best Practices: implementation guidance

## Tokens and components

Separate primitive tokens from semantic roles and component decisions; provide all
referenced values for every supported theme. The upstream button uses undefined
space-3, space-6, radius-md, secondary and danger colors, and its spread can replace
internal style: do not ship it as a complete component. Deliberately merge caller
props/styles and protect intended disabled/loading semantics. Native button type
must be explicit in reusable form contexts. State styling must include keyboard
focus, pressed, disabled, loading, invalid, and responsive behavior as applicable.

## Accessibility and governance

Choose the actual conformance target (current WCAG 2.2 AA when appropriate) and
verify semantics, keyboard/focus behavior, target size, contrast, motion, and
assistive technology. A component library or automated addon does not prove
accessibility. Storybook configuration/addon options are version-specific; use
existing tooling and avoid introducing paid visual services automatically.
Document purpose, API, states, usage boundaries, and consumer migration. Review
changes in real contexts as well as isolated stories, including token propagation,
RTL, themes, zoom and platform constraints. Version and publish only through the
user-authorized package workflow.

## Primary documentation

- [Current WCAG criteria and conformance](https://www.w3.org/TR/WCAG22/).
- [Component stories and states](https://storybook.js.org/docs/writing-stories).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
