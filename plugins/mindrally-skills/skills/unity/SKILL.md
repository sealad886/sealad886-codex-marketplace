---
name: unity
description: "Use when implementing Unity C# components, game state, input/UI, resource lifetime, physics, or measured performance."
---

# Unity game and application behavior

## When to invoke

Use when implementing Unity C# components, game state, input/UI, resource lifetime, physics, or measured performance.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Unity version, render pipeline, target platforms, Input/UI systems, scene/prefab ownership, and profiler evidence.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Locate the component/system owning the state and frame/physics behavior.
2. Implement lifecycle-correct references, input, resources, and failure handling.
3. Run focused play/edit-mode checks and profile representative target builds.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run relevant Unity edit/play-mode tests and representative platform build/interaction checks; report target, editor, and profiling limits.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
