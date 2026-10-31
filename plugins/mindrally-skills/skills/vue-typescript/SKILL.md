---
name: vue-typescript
description: "Use when implementing typed Vue components, props/emits, refs, composables, or build/type integration."
---

# Vue and TypeScript integration

## When to invoke

Use when implementing typed Vue components, props/emits, refs, composables, or build/type integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Vue/TypeScript/compiler versions, component style, vue-tsc config, typed props/events, and framework plugins.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Model the component’s public inputs/events and actual reactive state.
2. Implement supported typed Vue syntax while retaining the project’s component conventions.
3. Run SFC-aware type checks and behavior tests for updates, emits, and failures.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run vue-tsc/build and focused component tests for prop/event types, reactive updates, async failures, and keyboard operation.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
