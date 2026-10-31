---
name: storybook
description: "Use when writing Storybook stories, controls, documentation, interaction checks, themes, or component accessibility examples."
---

# Storybook component evidence

## When to invoke

Use when writing Storybook stories, controls, documentation, interaction checks, themes, or component accessibility examples.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Storybook/framework version, story format, addons, test runner, providers, and component behavior contracts.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Choose meaningful states and fixtures for the component’s public behavior.
2. Write version-correct typed stories and only necessary decorators/controls.
3. Execute interactions and available accessibility/visual checks, keeping their evidence limits explicit.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Build Storybook and run changed interaction tests plus available a11y/visual checks; identify manual and application integration coverage omitted.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
