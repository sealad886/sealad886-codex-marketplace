---
name: swiftui-development
description: "Use when implementing SwiftUI views, Observation/state ownership, async UI flow, navigation, adaptive layout, or measured rendering performance."
---

# SwiftUI state, tasks, and rendering

## When to invoke

Use when implementing SwiftUI views, Observation/state ownership, async UI flow, navigation, adaptive layout, or measured rendering performance.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect deployment targets, Swift language mode, Observation support, view identity, data ownership, task keys, and runtime evidence.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Assign one owner for model state and stable identity for repeated views.
2. Implement target-compatible observation and cancellation-aware async flow.
3. Verify interaction, loading/error states, accessibility, and measured rendering behavior.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Build and test state/task transitions including changing selection, cancellation, error recovery, stable list identity, and supported accessibility settings.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
