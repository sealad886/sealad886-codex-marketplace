# Anime.js Animation Guidelines: implementation guidance

## Version-correct animation

Anime.js v4 uses named APIs such as `animate(targets, parameters)`,
`createTimeline()`, `createAnimatable()`, and `waapi.animate()`. Do not combine
v3 `anime({ targets: ... })` or `anime.timeline()` examples with v4 imports.
The easing parameter and callback names also differ between major versions.
Use the installed version's documentation before copying an example.

## Composition and lifecycle

Compose sequencing with timelines and overlap positions, and stagger repeated
items. For continuous pointer-driven updates consider `createAnimatable()` and
its documented methods rather than assigning properties to a fabricated class.
Use documented SVG motion-path, drawable, or morph helpers for compatible shapes.
In React, scope animations to owned elements and revert the scope on cleanup;
pausing alone can leave styles and targets retained. Remove listeners as well.
Prefer transform/opacity when visually appropriate, but measure browser behavior
instead of promising GPU acceleration. Respect reduced-motion changes and expose
usable final states. Choose the WAAPI backend only for supported features.

## Primary documentation

- [v4 animate API](https://animejs.com/documentation/animation/).
- [createTimeline API](https://animejs.com/documentation/timeline/).
- [createAnimatable API](https://animejs.com/documentation/animatable/).
- [WAAPI API](https://animejs.com/documentation/waapi/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
