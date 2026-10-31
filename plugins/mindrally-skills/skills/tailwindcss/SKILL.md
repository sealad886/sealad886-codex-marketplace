---
name: tailwindcss
description: "Use when implementing Tailwind utilities, responsive states, themes, content detection, or version-specific configuration."
---

# Tailwind CSS styling

## When to invoke

Use when implementing Tailwind utilities, responsive states, themes, content detection, or version-specific configuration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Tailwind major/build integration, CSS entrypoints, source detection, design tokens, supported browsers, and existing class helpers.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Use the installed major’s configuration and token model.
2. Implement complete detectable utility classes and semantic responsive/interaction states.
3. Build production CSS and verify rendered layout, focus, contrast, and theme behavior.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run the production CSS build and check dynamic/conditional classes, responsive widths, keyboard focus, dark mode, and required browser support.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
