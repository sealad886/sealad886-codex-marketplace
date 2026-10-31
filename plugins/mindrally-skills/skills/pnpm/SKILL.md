---
name: pnpm
description: "Use when managing pnpm workspaces, dependency protocols, filters, lockfiles, install policy, or package release preparation."
---

# pnpm Development

## When to invoke

Use for managing pnpm workspaces, dependency protocols, filters, lockfiles, install policy, or package release preparation.

## Inputs and evidence

Inspect repository packageManager/engines, pnpm major version, workspace manifest, lockfile and lifecycle-script policy. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Reuse the declared pnpm version and workspace layout.
2. Update direct dependencies/workspace protocols with explicit package scope.
3. Run reproducible install and filtered tasks with correct dependency/dependent graph.
4. Inspect lockfile/packlist and run relevant tests before any authorized publication.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Selected-version install, graph/task checks and focused dependency tests pass with reviewed manifest/lockfile changes.

## Must not

Do not disable peer/engine/script protections or publish packages to resolve an install issue. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
