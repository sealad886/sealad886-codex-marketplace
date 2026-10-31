# Lerna Monorepo Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Configuration and tasks

- Modern Lerna delegates dependency management to npm/yarn/pnpm workspaces; obsolete useWorkspaces/bootstrap/link options are not current configuration.
- Fixed and independent version modes have different release effects; inspect the existing mode.
- Use graph-aware task ordering and correct cache inputs/outputs; parallel execution is safe only for independent tasks.

## Versioning and publication

- lerna version can change manifests, commit, tag and push; inspect flags/configuration before execution.
- lerna publish, from-git and from-package select different candidates; none should be used as a harmless preview.
- Changed-package selection needs an explicit base and dependency impact assessment; it is not proof all affected tests ran.
- Keep registry auth outside tracked files and verify packlists/dependency ranges before publishing.

## Primary documentation

- [Primary documentation](https://lerna.js.org/docs/legacy-package-management) — Lerna removed legacy package-management commands/options and delegates to workspaces.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
