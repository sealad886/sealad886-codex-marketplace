---
name: bootstrap
description: "Use when implementing Bootstrap responsive layouts, interactive components, forms, or themes."
---

# Bootstrap Development

## When to invoke

Use when implementing Bootstrap responsive layouts, interactive components, forms, or themes. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Bootstrap major version, CSS/JS imports, existing tokens, component markup, and accessibility requirements. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Choose grid/utilities/components supported by the installed version and preserve semantic markup.
2. Implement responsive states and required JavaScript behavior with accessible labels and focus handling.
3. Test viewport changes, keyboard interaction, validation feedback, contrast, and component lifecycle.

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
