# User experience evidence and flows: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Choose interviews, task observation, card sorting, or analytics from the question; personas and journeys should reflect evidence rather than invented demographics.

- Progressive disclosure hides optional detail while keeping required decisions, prerequisites, and critical errors visible.

- Use familiar labels and navigation where they support the domain; search or a hamburger menu is not mandatory for every information architecture.

- Provide meaningful loading, empty, error, completion, and undo/recovery states; explain irreversible consequences when relevant.

- Reduce cognitive load through grouping and sensible defaults without concealing important choices or manipulating consent.

- Accessibility includes keyboard, assistive technology, reflow, focus, and understandable content; select the applicable WCAG target and verify it.

- Animations/celebration/gestures must serve the task and support reduced motion and alternative operation.

- A/B tests require adequate design/sample and authorization; heatmaps/session recordings are optional and can capture sensitive data. Current Web Vitals use INP.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [WCAG versions and conformance targets must be chosen explicitly and verified.](https://www.w3.org/WAI/standards-guidelines/wcag/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
