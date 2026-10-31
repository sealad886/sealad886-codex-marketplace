---
name: game-development
description: "Use when implementing Unity C# gameplay or Lua game logic, assets, state, physics, or performance."
---

# Game Development

## When to invoke

Use when implementing Unity C# gameplay or Lua game logic, assets, state, physics, or performance. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect engine/Lua/runtime versions, gameplay invariants, frame/physics lifecycle, asset pipeline, platforms, and profiling evidence. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define gameplay/state ownership and choose the correct update, physics, input, and rendering boundaries.
2. Implement engine-appropriate components or Lua modules with explicit resource/lifecycle and deterministic state handling.
3. Test gameplay, pause/load/scene transitions, collision/input, memory cleanup and measured target-device frame behavior.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
