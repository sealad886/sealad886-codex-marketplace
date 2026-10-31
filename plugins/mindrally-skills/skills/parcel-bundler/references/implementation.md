# Parcel Bundler: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Entries and build semantics

- Parcel transpiles TypeScript but does not by default establish type correctness; run the configured type checker.
- Use documented new URL/import.meta.url or url: imports for URL assets; do not assume every image import returns the expected string.
- API proxy configuration uses supported .proxyrc formats, not a generic package devServer.proxy object copied from another bundler.
- Library types targets require the appropriate declaration transformer and coherent main/module/types paths.

## Dependencies and artifacts

- Automatic dependency installation can change manifests/lockfiles and execute install hooks; prefer declared locked dependencies and controlled installation.
- Environment references can be inlined into client output; never place secrets in browser-reachable code.
- Default transforms/optimization do not guarantee every asset is compressed or an application is performant; inspect emitted outputs.
- Use bounded no-cache diagnostics where appropriate instead of automatically deleting dist/cache or removing prior bundler configuration.

## Primary documentation

- [Primary documentation](https://parceljs.org/features/development/) — Parcel development documentation defines supported proxy configuration, dependency handling and development behavior.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
