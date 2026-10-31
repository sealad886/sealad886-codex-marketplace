# Responsive design: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Set breakpoints from content and layout behavior rather than treating common device widths as universal requirements.

- Use flexbox for a primary axis and grid for coordinated tracks; account for minimum-content sizing and long unbroken strings.

- A fixed 300px minimum grid track can overflow a narrower container; use a bounded minimum such as `minmax(min(100%, 18rem), 1fr)` where appropriate.

- Use container queries for component-local adaptation when supported, with a deliberate fallback for required browsers.

- Use fluid typography with meaningful lower/upper bounds; retain user zoom and avoid scaling that makes enlarged text unreadable.

- Provide width/height or an aspect ratio for images; choose srcset/sizes for resolution and picture for art direction. Avoid lazy loading the primary visible image.

- Prefer native HTML semantics before adding ARIA; test focus order, reduced motion, contrast, and hover-independent controls.

- Touch-target criteria depend on the chosen accessibility standard and exceptions; 44 CSS pixels is an enhanced target, not a universal minimum for every conformance level.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Responsive layout combines flexible sizing, media queries, and viewport configuration.](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design)
- [WCAG target-size minimum and exceptions differ from the enhanced criterion.](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
