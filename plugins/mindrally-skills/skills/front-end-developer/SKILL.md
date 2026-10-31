---
name: front-end-developer
description: "Use when implementing or reviewing web UI in React, Next.js, JavaScript, TypeScript, HTML, or CSS."
---

# Front-End Developer

## When to invoke

Use when implementing or reviewing web UI in React, Next.js, JavaScript, TypeScript, HTML, or CSS. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect user flow and design, current framework/render boundary, component/state/data contracts, styling system, and browser/accessibility targets. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace user interaction and data flow, reuse existing components and resolve essential behavior/design ambiguity.
2. Implement complete loading/empty/error/success states with semantic controls and correct framework syntax.
3. Build/type-check and exercise the critical interaction, responsive states, keyboard access and relevant rendering/performance evidence.

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
