---
name: lerna
description: "Use when managing Lerna workspace tasks, versioning modes, changed-package selection, or authorized package publication."
---

# Lerna Monorepo Development

## When to invoke

Use for managing Lerna workspace tasks, versioning modes, changed-package selection, or authorized package publication.

## Inputs and evidence

Inspect Lerna/Nx/package-manager versions, workspaces, lerna.json, dependency graph, cache inputs and release scripts. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use package-manager workspaces for dependency installation/linking.
2. Configure task dependencies and select the required package scope and comparison base.
3. Validate builds/tests and release package contents without assuming changed-only coverage is sufficient.
4. Run version/publish operations only under explicit authority and verify resulting commits/tags/registry state.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Selected tasks and package graph validate; release claims include actual manifest/tag/registry readback.

## Must not

Do not execute version/publish to inspect a repository or bypass release gates with --yes. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
