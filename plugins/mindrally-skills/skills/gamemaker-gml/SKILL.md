---
name: gamemaker-gml
description: "Use when implementing GML scripts, object events, gameplay state machines, collision, save data, or performance."
---

# GameMaker Language (GML) Development

## When to invoke

Use when implementing GML scripts, object events, gameplay state machines, collision, save data, or performance. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect GameMaker/runtime version, room/object/event order, movement model, resource ownership, input and save contracts. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define initialization, simulation, drawing and cleanup responsibilities with explicit state/instance ownership.
2. Implement the feature with a single movement/collision authority, valid instance references, and owned dynamic resources.
3. Test gameplay, falling/landing, pause, room transitions, destruction/removal, save migration, and target-runner behavior.

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
