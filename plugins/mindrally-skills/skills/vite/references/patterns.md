# Vite build and development behavior: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Vite transpiles TypeScript and does not itself type-check the application; run tsc/vue-tsc or the configured checker separately.

- Build internals and option names evolve; do not hardcode Rollup/esbuild-specific hooks into a different Vite generation without checking migration docs.

- Use ESM-safe config path resolution such as import.meta.url where appropriate; __dirname is not universally available in ESM.

- VITE_-prefixed variables are client-visible build configuration, not secret storage. Declaration files provide types, not runtime validation.

- Use current framework plugins; obsolete fastRefresh flags and old Tailwind PostCSS setup may no longer match installed versions.

- Vitest test configuration needs the supported Vitest config/types integration; a bare Vite defineConfig example does not guarantee test-key typing.

- Manual chunking requires output and runtime analysis; splitting every node_modules segment can mishandle scoped packages and create unnecessary requests.

- vite preview is a local production-build preview, not a hardened production server. Proxies/HMR server exposure require deliberate host and access settings.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Vite transforms TypeScript without performing type checking.](https://vite.dev/guide/features.html)
- [Official framework plugin capabilities and implementations are version-specific.](https://vite.dev/plugins/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
