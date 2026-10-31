# Framer Motion / Motion Animation Guidelines: implementation guidance

## Package, rendering and identity

Current Motion React uses motion/react when the motion package is installed;
framer-motion imports remain correct for projects using that supported package.
Do not silently upgrade or mix API generations. Variants coordinate states;
AnimatePresence tracks keyed children for exit, and layoutId needs an appropriate
shared-layout/identity scope. Motion values/useScroll/useTransform can update
animation without ordinary state-driven renders. Choose spring/tween behavior from
the design, not a universal spring preference.

## Performance and accessibility

Transform/opacity are often compositor-friendly, but properties such as backgroundColor,
filters or clipPath are not universally GPU-accelerated. Motion manages many
optimizations; do not add permanent will-change to every property/element, which
can increase memory and alter rendering. Memoization/hoisted style objects are
measured choices, not blanket requirements. Use MotionConfig reduced-motion policy
or useReducedMotion with usable non-motion final states and consider preference
changes. Native semantic buttons and focus behavior remain required for gesture
controls. Measure frame-time/long tasks on real target hardware rather than
promising 60/120fps from API selection alone.

## Primary documentation

- [Versioned Motion/Framer Motion migration](https://motion.dev/docs/react-upgrade-guide).
- [Animation backend and measured performance](https://motion.dev/docs/performance).
- [Reduced-motion behavior](https://motion.dev/docs/react-accessibility).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
