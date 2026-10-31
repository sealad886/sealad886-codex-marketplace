---
name: vuejs-typescript-best-practices
description: "Use when reviewing Vue/TypeScript component architecture, composables, reactive boundaries, accessibility, or measured performance."
---

# Vue TypeScript implementation review

## When to invoke

Use when reviewing Vue/TypeScript component architecture, composables, reactive boundaries, accessibility, or measured performance.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect existing Vue patterns, typed public APIs, reactivity/SSR state, UI dependencies, and profiling or error evidence.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Trace the requested behavior through component, composable, and store ownership.
2. Improve types and reactive flow without replacing the existing UI/build stack.
3. Verify observable behavior and benchmark only the identified performance path.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run SFC type/build checks and focused reactivity/interaction tests; compare measured traces for any performance claim.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
