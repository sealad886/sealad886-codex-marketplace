# Accessibility (a11y) Best Practices: implementation guidance

## Semantics, interaction, and content

Use native buttons for actions and links for navigation. Associate labels and errors
with fields; group related controls. Prefer visible text with `aria-labelledby`
over an unrelated accessible name. Announce status changes without moving focus.
For a custom widget, implement the applicable APG keyboard/focus pattern and state
attributes; adding a role alone does not supply behavior. Native buttons already
support keyboard activation: do not add duplicate key handlers or `onKeyPress`.

Use meaningful alternative text for informative images and empty alt text for
pure decoration. Provide captions/transcripts appropriate to the media and target
criteria. Maintain logical headings, landmarks, tab order, and visible focus.

## Visual checks

WCAG AA text contrast is normally 4.5:1, or 3:1 for qualifying large text. WCAG
2.2 AA target-size minimum is 24 by 24 CSS pixels with specified exceptions;
44 by 44 is the enhanced AAA criterion. Check the exact applicable exceptions.
Test 200% text resize and reflow separately. Honor reduced motion and avoid
color-only communication. Automated tools identify only part of conformance;
manual keyboard and assistive-technology checks remain necessary.

## Primary documentation

- [WCAG 2.2 AA target size and exceptions](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).
- [Widget semantics and keyboard interaction](https://www.w3.org/WAI/ARIA/apg/patterns/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
