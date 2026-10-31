---
name: alpine-js
description: "Use when building or repairing lightweight Alpine.js reactive components and backend-rendered interactions."
---

# Alpine.js Development

## When to invoke

Use when building or repairing lightweight Alpine.js reactive components and backend-rendered interactions. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Alpine version and startup, rendered markup, component state, and any Livewire integration. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Map each interaction to local x-data state, bindings, and events.
2. Implement state changes with native accessible controls and select x-show or x-if based on lifecycle needs.
3. Check initialization, focus, repeated rendering, outside clicks, and form failures.

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
