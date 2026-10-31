# Nx Monorepo Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Project and task configuration

- Nx constructs projects from plugins, targetDefaults and package/project configuration; a project.json is not mandatory for every project.
- Use effective configuration views and the project graph before overriding inferred tasks.
- Module tags only enforce boundaries when matching lint/conformance rules run; a tag alone is documentation.

## Caching and CI

- Set accurate inputs/environment/dependency edges and outputs so cached tasks represent actual behavior.
- Use supported nx affected -t syntax with explicit base/head; older affected:test/build shortcuts may be removed by the installed generation.
- Remote caching/Nx Cloud exports artifacts and can incur service costs; use only configured authorized destinations.
- Changed-only tasks need a dependency-aware graph and valid comparison base; test cache misses and invalidation for changed configuration.

## Primary documentation

- [Primary documentation](https://nx.dev/docs/reference/project-configuration) — Nx combines inferred tasks, targetDefaults and package/project configuration into effective project settings.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
