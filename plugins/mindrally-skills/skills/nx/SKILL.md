---
name: nx
description: "Use when configuring Nx project graphs, inferred tasks, module boundaries, generators, affected checks, or computation caching."
---

# Nx Monorepo Development

## When to invoke

Use for configuring Nx project graphs, inferred tasks, module boundaries, generators, affected checks, or computation caching.

## Inputs and evidence

Inspect Nx/plugin/package-manager versions, inferred project configuration, graph tags, target inputs/outputs and CI comparison revisions. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Inspect effective project/task graph before changing configuration.
2. Declare necessary boundaries and target dependencies without duplicating inferred configuration.
3. Run generators with preview and choose complete affected/task scopes.
4. Validate task outputs/cache correctness and CI base/head selection.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Effective graph/configuration and selected tasks validate; cache behavior and CI revision mapping have direct evidence.

## Must not

Do not overwrite inferred config or enable external cache/services just to follow a template. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
