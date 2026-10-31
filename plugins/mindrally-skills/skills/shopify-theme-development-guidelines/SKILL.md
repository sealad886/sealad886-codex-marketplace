---
name: shopify-theme-development-guidelines
description: "Use when designing Shopify theme structure, merchant settings, section/block schemas, locale keys, or theme-editor behavior."
---

# Shopify theme architecture and editor UX

## When to invoke

Use when designing Shopify theme structure, merchant settings, section/block schemas, locale keys, or theme-editor behavior.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect theme generation, supported block features, schema/settings conventions, locale files, and target merchant workflows.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Map requested customization to the existing layout/template/section/block boundary.
2. Implement supported schemas and localized accessible controls with scoped assets.
3. Validate static theme rules and real editor lifecycle/published-page behavior in preview.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run Theme Check and verify section add/remove/reorder, translated settings, repeated IDs, keyboard flow, and preview rendering.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
