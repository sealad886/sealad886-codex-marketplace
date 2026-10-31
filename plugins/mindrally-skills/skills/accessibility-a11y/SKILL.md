---
name: accessibility-a11y
description: "Use when implementing or auditing accessible web navigation, forms, dialogs, visual content, or keyboard interactions."
---

# Accessibility (a11y) Best Practices

## When to invoke

Use when implementing or auditing accessible web navigation, forms, dialogs, visual content, or keyboard interactions. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect the UI task, conformance target, rendered DOM, focus behavior, and assistive-technology coverage. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Establish the applicable WCAG level and inspect native semantics before adding ARIA.
2. Implement accessible names, keyboard behavior, focus management, and perceivable error and status feedback.
3. Check contrast, zoom/reflow, target size, reduced motion, keyboard operation, and representative screen-reader paths.

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
