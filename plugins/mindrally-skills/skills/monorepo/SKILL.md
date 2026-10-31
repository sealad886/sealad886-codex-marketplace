---
name: monorepo
description: "Use when organizing JavaScript/TypeScript workspaces, shared packages, cross-platform application boundaries, or task caching."
---

# Monorepo Development

## When to invoke

Use for organizing JavaScript/TypeScript workspaces, shared packages, cross-platform application boundaries, or task caching.

## Inputs and evidence

Inspect package manager/lockfile, workspace graph, task runner, package exports, web/native targets and release/version ownership. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define package ownership and public interfaces within the existing workspace layout.
2. Declare direct dependencies and task/build graph edges accurately.
3. Share stable domain logic while isolating platform-specific code and secrets.
4. Run affected and integration checks using complete dependency/cache inputs.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Workspace resolution, public imports, platform builds and relevant task/cache checks succeed.

## Must not

Do not expand every shared package into a universal abstraction or force one application stack. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
