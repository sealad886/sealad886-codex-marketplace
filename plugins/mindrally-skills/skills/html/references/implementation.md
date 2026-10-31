# HTML Development Guidelines: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Semantics and forms

- Use buttons for actions and links with href for navigation; specify button type inside forms to avoid accidental submission.
- Maintain a useful heading hierarchy; one primary h1 is a common design convention, not a universal HTML validity constraint.
- HTML b and i remain valid semantic elements; use strong/em when importance or stress is intended, and CSS for purely visual styling.
- Associate labels, fieldsets, and error descriptions; client constraints do not replace server validation.

## Media and document behavior

- Use meaningful alt text or empty alt for decorative images; supply dimensions and responsive image selection where useful.
- Set html lang, encoding, viewport, and a descriptive title; use native landmarks without duplicate roles.
- Void elements such as img/input do not have end tags; XML-style self-closing syntax does not make ordinary HTML elements self-closing.
- Select async/defer/module behavior based on dependency and execution order; preload only measured critical resources.

## Primary documentation

- [HTML living standard](https://html.spec.whatwg.org/multipage/semantics.html) — Document semantics and metadata are defined by the current HTML standard.
- [HTML text-level semantics](https://html.spec.whatwg.org/multipage/text-level-semantics.html) — The b and i elements retain defined text-level semantics.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
