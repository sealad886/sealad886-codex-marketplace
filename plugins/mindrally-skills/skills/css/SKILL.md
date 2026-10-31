---
name: css
description: "Use when implementing or debugging responsive CSS layout, cascade, themes, typography, or motion."
---

# CSS Development Guidelines

## When to invoke

Use when implementing or debugging responsive CSS layout, cascade, themes, typography, or motion. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect target browser matrix, computed styles, DOM semantics, design tokens, cascade layers, and visual/accessibility requirements. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inspect the actual cascade and layout constraints before adding overrides.
2. Implement the selected layout/theme with intentional sizing, responsive behavior, and accessible interaction states.
3. Check browser/viewport/zoom states, overflow, focus, contrast, reduced motion, and relevant computed styles.

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
