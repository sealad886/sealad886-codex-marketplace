# Tailwind CSS styling: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Tailwind v4 uses CSS-first configuration and changed build/plugins compared with v3; do not assume a JavaScript config or JIT toggle remains the setup path.

- @apply is a supported directive with scope/reference constraints; never-use-in-production is a style preference, not a Tailwind rule.

- Build complete class names rather than concatenating dynamic fragments that source scanning cannot discover.

- Use existing semantic tokens and variants; do not mandate Tailwind for every style or add a UI component library automatically.

- Default breakpoints are minimum-width/mobile-first variants, but choose project breakpoints from content needs.

- Dark mode can follow media or configured selectors; ensure the app’s theme state matches the actual variant strategy.

- The container utility does not automatically center or pad itself; v4 customization differs from older container configuration.

- Use focus-visible, disabled, reduced-motion, logical spacing, and accessible markup; utility classes do not guarantee accessible components.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Tailwind v4 changes configuration, utilities, and integration from v3.](https://tailwindcss.com/docs/upgrade-guide)
- [@apply is a supported Tailwind directive.](https://tailwindcss.com/docs/functions-and-directives)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
