---
name: shopify
description: "Use when changing Shopify Liquid, Online Store theme sections, JSON templates, cart interactions, images, or localization."
---

# Shopify theme implementation

## When to invoke

Use when changing Shopify Liquid, Online Store theme sections, JSON templates, cart interactions, images, or localization.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect theme architecture, Shopify CLI/Theme Check versions, Liquid objects, section settings, cart API behavior, and preview-store authority.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Locate the existing theme section/snippet/template owning the behavior.
2. Implement supported Liquid and locale-aware browser interactions with error states.
3. Validate Theme Check and test in an authorized unpublished preview theme.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run Theme Check and preview affected sections/cart states with valid and invalid inputs; report device, checkout, and store checks not run.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
