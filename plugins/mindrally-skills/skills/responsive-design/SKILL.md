---
name: responsive-design
description: "Use when adapting web layouts, typography, imagery, and interactions across viewport sizes, zoom levels, and input modes."
---

# Responsive design

## When to invoke

Use when adapting web layouts, typography, imagery, and interactions across viewport sizes, zoom levels, and input modes.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect real content lengths, supported browsers, layout constraints, accessibility targets, images, and current responsive styles.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Find the width or input condition where content stops working.
2. Use intrinsic sizing, flexible layout, and justified media/container queries.
3. Verify reflow, zoom, keyboard/touch operation, and asset loading across representative conditions.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Check narrow and wide widths, long content, keyboard/touch, text enlargement and zoom; name tested browsers and devices.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
