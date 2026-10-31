# Interface design and implementation review: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use existing brand and component conventions when available; ask only for missing decisions that materially affect the task.

- Choose type, spacing, and contrast for hierarchy and readability, including long/localized content and text enlargement.

- Use native semantics first and add ARIA only where needed; decorative imagery has different text-alternative requirements.

- Target-size rules depend on WCAG version/level and exceptions; 44px is an enhanced/design target, not every AA minimum.

- Current Core Web Vitals include INP, LCP, and CLS; separate lab scores from real user evidence.

- Gestures need discoverable alternatives and must not conflict with platform accessibility/navigation.

- Analytics, heatmaps, recordings, and A/B tests require real research goals and privacy/authorization; do not add them by default.

- Use fixed or relative units according to the layout; animations and visual effects must support motion preferences and task clarity.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [WCAG 2.2 minimum target size is 24 CSS pixels with defined exceptions.](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [Current responsiveness metric is INP.](https://developers.google.com/search/docs/appearance/core-web-vitals)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
