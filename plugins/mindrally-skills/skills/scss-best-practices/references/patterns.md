# SCSS module architecture: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- SCSS uses CSS-like braces and semicolons; keep .sass indented syntax separate.

- @use is file-scoped, not a shared global import: each stylesheet that uses tokens needs the appropriate @use, and @forward exposes a module API.

- Prefer sass:map, sass:math, and sass:color APIs; replace map-get/map-has-key, slash division, and deprecated global color functions as supported by the compiler.

- Importing modules at the entrypoint does not make their variables available in components loaded later.

- Use color.adjust or color.scale according to the intended lightness change and color-space requirements; do not mechanically replace every color operation with one formula.

- Keep nesting and @extend deliberate; inspect emitted selector multiplication and avoid generating unused utility matrices.

- Preserve the project’s design architecture; a 7–1 directory layout, BEM naming, and fixed property order are options rather than compiler requirements.

- Ensure focus styles, logical layout, reduced motion, and controlled animation properties; source map distribution follows the project’s debugging/privacy policy.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [@use provides file-local namespaced members.](https://sass-lang.com/documentation/at-rules/use/)
- [Current Dart Sass deprecates @import and global built-ins.](https://sass-lang.com/documentation/breaking-changes/import/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
