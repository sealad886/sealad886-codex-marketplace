---
name: ghost
description: "Use when implementing Ghost CMS Handlebars themes, assets, membership UI, metadata, or performance."
---

# Ghost CMS Theme Development

## When to invoke

Use when implementing Ghost CMS Handlebars themes, assets, membership UI, metadata, or performance. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Ghost/theme version, templates/helpers, package config/image sizes, memberships/tier access, assets and rendered content states. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inspect theme routes, helper contexts, content types, design tokens and membership access requirements.
2. Implement supported Handlebars/helper composition with accessible responsive assets and explicit member/guest behavior.
3. Run the supported theme validator and check rendered posts/pages, paid/free/guest states, pagination, metadata and assets.

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
