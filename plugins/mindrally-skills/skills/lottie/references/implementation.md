# Lottie Animation Guidelines: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Player API and assets

- dotLottieReact renders through a canvas-based player; do not pass unsupported SVG renderer choices copied from another Lottie implementation.
- Use the actual installed prop names, such as playOnHover where supported, and obtain player control through dotLottieRefCallback.
- Listen to documented player load/loadError events; React DOM onLoad/onError are not interchangeable with player events.
- Compression savings depend on source assets and transport compression; do not promise a fixed 90 percent reduction.

## Accessibility and lifecycle

- Distinguish decorative animation from meaningful status; label meaningful state in accessible text instead of relying on canvas content.
- Read matchMedia only in browser-safe lifecycle code and respond to preference changes when needed.
- Clamp frame progress to the valid range and wait for the asset to load; track event/scroll subscriptions and remove them on teardown.
- The wrapper may own player destruction; follow its lifecycle contract and avoid double-destroying an instance still in use.

## Primary documentation

- [Primary documentation](https://github.com/LottieFiles/dotlottie-web/blob/main/packages/react/README.md) — DotLottieReact props extend canvas props and expose player references/events and supported playback options.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
