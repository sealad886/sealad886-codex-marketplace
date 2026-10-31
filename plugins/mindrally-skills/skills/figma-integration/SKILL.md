---
name: figma-integration
description: "Use when implementing a Figma design, mapping design tokens/components, exporting assets, or comparing design and rendered UI."
---

# Figma Integration Guidelines

## When to invoke

Use when implementing a Figma design, mapping design tokens/components, exporting assets, or comparing design and rendered UI. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect authorized file/node identifiers and version, actual Figma/MCP/REST tool schemas, existing components/tokens, and responsive/interaction requirements. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Read the selected design nodes and identify layout, variants, assets, token references, and ambiguous behavior.
2. Map intent onto existing implementation components and export only required authorized assets.
3. Compare rendered states/viewports and accessibility against the design; report concrete deviations and unresolved interaction requirements.

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
