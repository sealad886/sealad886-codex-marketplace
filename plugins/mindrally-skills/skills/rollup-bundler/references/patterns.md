# Rollup library bundling: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use output.file for a single output chunk and output.dir for multiple chunks; code-splitting output must support the selected module format.

- Configure ESM, CJS, UMD, or IIFE only when supported consumers require them; browser globals are required for relevant external UMD/IIFE dependencies.

- Externalize peer dependencies, including required subpaths, rather than blindly treating every dependency identically.

- Tree shaking depends on analyzable code and side-effect knowledge; named exports alone do not guarantee smaller output.

- Do not declare `sideEffects: false` for modules that intentionally register plugins, initialize globals, or import required CSS.

- Use maintained official resolve/CommonJS/TypeScript/replace/minification plugins matching the installed major.

- Node ESM loading of package.json depends on the installed Node version and import attributes; do not copy a bare JSON import unconditionally.

- Use documented CLI options and logging controls; an unsupported `--configDebug` flag is not a diagnostic method. Verify sourcemaps and declarations when promised.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Rollup CLI flags and config loading follow documented Node/module behavior.](https://rollupjs.org/command-line-interface/)
- [Output formats, externals, and tree-shaking options have explicit constraints.](https://rollupjs.org/configuration-options/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
