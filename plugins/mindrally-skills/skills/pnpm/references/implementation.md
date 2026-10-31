# pnpm Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Workspace and dependencies

- Use pnpm when the project selects it; do not replace npm/yarn or install global/latest tooling merely because this skill is invoked.
- workspace protocols require a matching local package and are rewritten on packing/publication; range selection should follow release intent.
- Filter prefix/suffix ellipses select dependents/dependencies differently; verify the chosen package set before large operations.

## Version and execution policy

- Configuration locations, hoisting defaults, peers and dependency build approval differ by pnpm major; inspect supported settings instead of copying a fixed v9 .npmrc.
- Frozen lockfiles provide reproducibility only with compatible runtime/configuration and available packages; offline installs need the complete fetched store.
- Install, dedupe, overrides and audit fixes can change resolved dependencies or run scripts; inspect changes and use repository policy.
- Remote stores/caches and publication credentials need approved destinations; package publishing is externally visible.

## Primary documentation

- [Primary documentation](https://pnpm.io/workspaces) — pnpm workspaces and workspace protocols govern local dependency resolution and package publication rewriting.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
