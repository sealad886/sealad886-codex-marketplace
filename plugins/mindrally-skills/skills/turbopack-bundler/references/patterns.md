# Turbopack Next.js builds: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Current next.config turbopack settings differ from old experimental.turbo; default bundler/flags vary by Next version.

- Webpack plugins are not automatically supported. Turbopack’s loader support is a documented subset with constraints; inspect each custom loader.

- TypeScript/JSX transformation does not replace type checking; run the project’s TypeScript gate.

- TypeScript as const is erased and does not itself improve tree shaking; package side effects and actual module usage determine output.

- Cache persistence and diagnostics evolve by version. Do not invent environment flags or assume ANALYZE=true works without an analyzer integration.

- Capture logs and inspect supported cache tooling before deleting .next; preserve evidence and avoid concurrent build/dev disruption.

- Dynamic imports and ssr:false must obey Next component boundaries; disabling SSR is not a universal fix for a bundler error.

- Verify aliases, extensions, native/server-only modules, CSS, and public environment exposure in the final build.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Turbopack has versioned configuration and constrained webpack loader compatibility.](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
