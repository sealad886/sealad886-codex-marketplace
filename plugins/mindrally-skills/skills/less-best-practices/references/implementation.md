# Less CSS Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Language and compilation

- Less variables and mixins are compile-time constructs; CSS custom properties provide different runtime behavior.
- Less 4 math behavior requires parentheses for division in many contexts; use percentage((1 / 3)) when arithmetic evaluation is intended.
- Less supports built-in functions and plugin-defined custom functions; mixin-return patterns are an alternative, not proof functions do not exist.
- Use imports, namespaces, guarded mixins, and bounded generated utilities deliberately; verify output size.

## Styles and accessibility

- Keep nesting/specifity manageable without imposing universal indentation/BEM/depth requirements over project conventions.
- Token colors and lighten/darken do not guarantee contrast; check text, focus and disabled states in rendered themes.
- Prefer targeted transitions and a reduced-motion path; avoid transition: all as an automatic default.
- Use an existing PostCSS/autoprefixer pipeline for browser support when present; do not recommend removed compression options.

## Primary documentation

- [Primary documentation](https://lesscss.org/usage/) — Less compiler math modes, plugins and command options are version-specific.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
