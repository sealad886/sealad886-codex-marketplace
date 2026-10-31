# GSAP Animation Guidelines: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Animation design

- Use to, from, or fromTo according to the known initial state; timelines and labels coordinate dependent steps.
- Prefer transform/opacity where they reduce layout cost, but animate layout when the design actually requires it.
- Stagger, lag smoothing, will-change, and layer promotion are optional tools; excessive layers can increase memory and harm rendering.

## Framework and scroll lifecycle

- In React, use the installed @gsap/react useGSAP integration or an explicitly owned gsap.context; scope selectors to the component.
- useGSAP reverts context on teardown. With changing dependencies, select revertOnUpdate when resynchronization must revert prior work.
- Wrap delayed/event-created GSAP work in contextSafe and remove listeners/timers separately.
- Register ScrollTrigger/MotionPath only when used; refresh geometry after layout changes and test pinned content and reduced motion.

## Primary documentation

- [GSAP React guide](https://gsap.com/resources/React/) — useGSAP context cleanup, contextSafe, and revertOnUpdate lifecycle semantics.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
