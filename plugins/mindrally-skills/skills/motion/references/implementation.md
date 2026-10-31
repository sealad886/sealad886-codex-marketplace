# Motion Animation Guidelines: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Current API selection

- Current hybrid animate accepts animation sequences; do not import old timeline APIs from modern motion without checking exports.
- Use ease with supported names such as easeOut and defaultTransition for sequence defaults; old easing/defaultOptions recipes are version-specific.
- inView callbacks receive element and entry; the first parameter is not an entry whose target should be read.
- Playback control properties/methods differ across generations; confirm time/speed/completion interfaces before copying Web Animations recipes.

## Performance and lifecycle

- Use scroll-linked animations or motion values directly instead of creating a new duration-zero animation every scroll event.
- Prefer transform/opacity when they help, but individual transform components do not guarantee compositor acceleration.
- Track observer, scroll, event-listener and animation cleanup separately; stopping an animation does not remove all subscriptions.
- Handle reduced motion and missing/browser-only APIs safely; will-change and layer promotion are measured options.

## Primary documentation

- [Primary documentation](https://motion.dev/docs/animate) — Current animate supports sequences, ease, defaultTransition and documented playback controls.
- [Motion inView](https://motion.dev/docs/inview) — inView callbacks receive an element and intersection entry and return lifecycle cleanup.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
