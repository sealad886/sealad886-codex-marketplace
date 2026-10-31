---
name: styled-components-best-practices
description: "Use when implementing styled-components themes, dynamic styles, transient props, SSR, or React styling performance."
---

# Styled-components runtime and styling

## When to invoke

Use when implementing styled-components themes, dynamic styles, transient props, SSR, or React styling performance.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect styled-components/React/framework versions, theme typing, forwarded props, SSR pipeline, and style output.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Extend the existing token/theme and component boundary.
2. Implement valid CSS and deliberate prop forwarding without recreating component types during render.
3. Verify accessibility, hydration, responsive states, and measured style/render costs.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run type/build checks plus styled UI/hydration checks, confirming styling props are absent from unintended DOM output.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
