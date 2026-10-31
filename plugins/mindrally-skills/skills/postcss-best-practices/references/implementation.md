# PostCSS Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Transforms and compatibility

- PostCSS is the parser/plugin pipeline; it does not itself polyfill all future CSS or guarantee browser support.
- postcss-nested Sass-like concatenation differs from standards-based nesting; choose syntax intentionally.
- CSS feature proposal stage is not a browser-stability guarantee; use actual target support and plugin-version behavior.
- preset-env can include Autoprefixer, so adding another instance may duplicate work; inspect its configuration.

## Framework and production configuration

- Tailwindv4 uses @tailwindcss/postcss rather than the older tailwindcss/nesting plus tailwindcss plugin recipe.
- Vite config resolution and custom-media import APIs vary by version; use documented config paths/options, not obsolete importFrom assumptions.
- PurgeCSS needs complete dynamic-class sources/safelists; minifiers must preserve required license notices and animation semantics.
- Source maps can be useful in protected production debugging but can expose source; choose publication deliberately rather than a universal dev-only rule.

## Primary documentation

- [Primary documentation](https://tailwindcss.com/docs/installation/using-postcss) — Current Tailwind PostCSS setup uses @tailwindcss/postcss with major-version-specific configuration.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
