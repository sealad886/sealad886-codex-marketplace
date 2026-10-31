---
name: performance-optimization
description: "Use when measuring and improving web loading, rendering, runtime work, assets, caching, or query performance."
---

# Performance Optimization

## When to invoke

Use for measuring and improving web loading, rendering, runtime work, assets, caching, or query performance.

## Inputs and evidence

Inspect target user/device/network conditions, production traces, field/synthetic baseline, critical journeys and correctness constraints. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define the slow user-visible behavior and collect a reproducible baseline.
2. Identify the dominant bottleneck across server/network/browser/data boundaries.
3. Apply one coherent optimization and preserve usability/security semantics.
4. Compare equivalent before/after measurements and check regressions/resource tradeoffs.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Measured improvements hold under comparable conditions and critical interaction, rendering and data correctness checks pass.

## Must not

Do not claim performance gains from conventions alone or optimize away required content/accessibility. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
