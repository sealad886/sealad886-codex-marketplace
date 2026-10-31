# Indented Sass modules: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Indented .sass syntax uses indentation and omits braces/semicolons; do not mix SCSS examples into a .sass file.

- Use @use/@forward; symbols loaded by main.sass are not automatically visible inside separately loaded modules. Each consumer needs its own @use.

- Use namespaced built-ins such as map.get and math.div. Global built-ins and @import are deprecated in current Dart Sass.

- Replace removed/deprecated lighten/darken patterns with an appropriate color.adjust or color.scale call after choosing the desired color-space behavior.

- Keep arithmetic units explicit; division written with / is not the modern general-purpose arithmetic API.

- Use mixins for parameterized repeated declarations and @extend sparingly for intentional selector relationships.

- Limit nesting and generated utility loops by actual output needs, not a universal directory architecture or arbitrary nesting number.

- Keep focus indicators and reduced-motion behavior; avoid transition:all when only selected properties should animate. Source maps can remain a controlled debugging artifact.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Dart Sass deprecates @import and global built-in functions.](https://sass-lang.com/documentation/breaking-changes/import/)
- [@use members are scoped to the loading stylesheet.](https://sass-lang.com/documentation/at-rules/use/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
