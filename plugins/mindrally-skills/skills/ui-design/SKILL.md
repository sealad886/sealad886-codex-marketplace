---
name: ui-design
description: "Use when designing or reviewing interface hierarchy, controls, visual states, responsive layout, or accessibility."
---

# Interface design and implementation review

## When to invoke

Use when designing or reviewing interface hierarchy, controls, visual states, responsive layout, or accessibility.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect the actual user task, existing brand/design system, content, supported devices, accessibility target, and interaction evidence.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify the primary task and visible states before selecting layout/styles.
2. Implement coherent hierarchy, semantic controls, and deliberate loading/error/recovery behavior.
3. Inspect rendered states and test keyboard, assistive technology, responsive content, and performance evidence.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Verify relevant states, widths, zoom/text enlargement, focus, contrast, and available assistive-technology checks; report untested scope.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
