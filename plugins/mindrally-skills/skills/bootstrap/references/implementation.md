# Bootstrap Development: implementation guidance

## Layout and components

Use container/row/column structure and breakpoint behavior deliberately. Include
only required CSS/JS through the current build system; a CDN is not universally
faster or allowed by CSP/offline requirements. Bootstrap 5 data-bs attributes differ
from older versions and interactive components need JavaScript initialization.
Modals require an accessible name, labeled close button, appropriate focus return,
and tested dismissal behavior. Utilities do not replace content semantics.

## Forms and themes

Validation styles do not implement validation. novalidate disables native browser
feedback; only use it with a complete accessible replacement. Bootstrap documents
accessibility limitations of custom client-side validation/tooltips, so prefer
native validation or an accessible server-side feedback path as appropriate.
Associate feedback with inputs and show invalid state accessibly. Customize via
supported Sass variables or CSS custom properties for the installed version.
Verify actual theme colors and states; Bootstrap defaults do not guarantee every
combination meets contrast requirements. Honor reduced motion.

## Primary documentation

- [Validation behavior and accessibility limitations](https://getbootstrap.com/docs/5.3/forms/validation/).
- [Modal markup, focus, and labels](https://getbootstrap.com/docs/5.3/components/modal/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
