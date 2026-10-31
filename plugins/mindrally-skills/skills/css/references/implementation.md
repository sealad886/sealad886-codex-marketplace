# CSS Development Guidelines: implementation guidance

## Layout and cascade

Use Flexbox for suitable one-axis relationships and Grid for suitable track-based
layouts; either can solve more than its simplest description. Use gap/logical
properties where supported. Container queries need an appropriate query container.
Min-width, intrinsic sizing, wrapping, and overflow often explain failures better
than adding breakpoints. Layer order is considered before specificity, and important
declarations reverse layer priority. Inline styles and !important are supported
features: use them deliberately where the application needs them instead of
blanket bans or a universal 0-1-0 specificity requirement.

## Tokens, units, and validation

Use semantic custom properties with defined fallbacks and theme scope. rem/em
support scalable typography, but unit choice alone does not guarantee accessibility;
verify browser zoom, text resize, and reflow. Consider dynamic viewport units on
mobile where supported. Fluid clamp sizing must still allow user scaling. Honor
focus-visible, contrast, reduced motion, and logical RTL layout; hidden content
has different visual/focus/accessibility effects depending on the technique.
Use feature detection/progressive enhancement for the actual browser baseline.
Measure style/layout cost before claiming class selectors are faster or adding
containment, which can change rendering and positioning behavior.

## Primary documentation

- [Cascade ordering, layers, inline and important precedence](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
