# Monorepo Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Workspace and graph

- Package managers own workspace installation/linking; a task runner such as Turborepo schedules/caches tasks.
- apps/packages is a useful convention, not a requirement to relocate an existing valid repository.
- Declare every imported dependency and public export; avoid relying on accidental root hoisting.

## Cross-platform and caching

- Share React/domain code only where platform semantics match; verify .native and web resolution through each bundler.
- expo-localization detects locales and still needs a message layer; do not assume one state/query/navigation library is required.
- Cache keys must include relevant source, environment and dependency inputs; generated outputs need explicit ownership.
- Keep backend/payment credentials server-side; shared packages must not cause client bundles to import privileged SDKs.

## Primary documentation

- [Primary documentation](https://turborepo.dev/docs/crafting-your-repository/structuring-a-repository) — Workspace boundaries, package declarations and task graph structure govern Turborepo repositories.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
