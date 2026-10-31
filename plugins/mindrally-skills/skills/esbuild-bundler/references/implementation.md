# esbuild Bundler: implementation guidance

## Build contracts

esbuild transpiles TypeScript but does not type-check; use tsc or the existing
checker. isolatedModules helps detect constructs needing cross-file type information,
not a runtime guarantee. Targets transform supported syntax, not all missing runtime
APIs/polyfills. Select actual supported browser/Node baselines instead of dated
Node 18/browser examples. ESM splitting needs outdir and supported loading; external
modules must exist for the consumer. File/copy/dataurl loaders have distinct asset
emission and URL behavior, which must be tested in packaged output.

## Plugins, optimization, and server

The upstream env plugin serializes all process.env into client output, exposing
credentials: allowlist only intentional public build constants. Validate define
values and do not include secrets in source maps or logs. drop:console can remove
argument side effects; use a more selective pure-call policy only if semantics
permit. Tree shaking depends on side-effect metadata and module semantics.
Use context.watch/serve and dispose owned contexts; bind dev servers deliberately
and never assume an unauthenticated dev server is production hosting. Incremental
reuse is scoped to the build context; avoid blanket speed/filesystem-cache promises.

## Primary documentation

- [Build targets, splitting, drop and context lifecycle](https://esbuild.github.io/api/).
- [TypeScript transpilation limits](https://esbuild.github.io/content-types/#typescript).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
