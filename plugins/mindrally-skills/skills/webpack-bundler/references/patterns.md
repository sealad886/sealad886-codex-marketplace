# Webpack build configuration: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Webpack loaders generally run right-to-left; use MiniCssExtractPlugin.loader for production extraction instead of assuming adding the plugin replaces style-loader.

- Do not mark sideEffects:false unless all affected modules really lack required side effects; preserve CSS, polyfills, and registration modules.

- Asset modules cover common file handling in Webpack 5; avoid duplicate obsolete file-loader/url-loader rules unless a task requires them.

- Dev-server proxy and config syntax vary by version; use installed help/types rather than older object examples unconditionally.

- DefinePlugin substitutes build-time values into output. Only expose deliberate public values and quote literals correctly.

- output.clean deletes files in the output directory; ensure that directory contains only owned generated artifacts and no concurrent valuable output.

- Splitting every build is not mandatory; choose runtimeChunk/splitChunks from caching and loading evidence and test publicPath/deep links.

- Filesystem caches need complete build/config dependency invalidation; warm-build success does not prove a clean build works.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Required CSS and initialization side effects must be preserved during production tree shaking.](https://webpack.js.org/guides/tree-shaking/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
