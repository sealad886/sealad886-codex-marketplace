---
name: scss-best-practices
description: "Use when changing .scss stylesheets, tokens, modules, mixins, selector output, or Dart Sass compilation."
---

# SCSS module architecture

## When to invoke

Use when changing .scss stylesheets, tokens, modules, mixins, selector output, or Dart Sass compilation.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect compiler version, SCSS entrypoints, module dependencies, existing tokens, CSS output, and component behavior.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Locate the owning stylesheet and reuse existing tokens or abstractions.
2. Implement current scoped modules and only necessary mixins/functions.
3. Compile and verify specificity, layout, focus, and generated output size.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Compile changed SCSS entrypoints and inspect CSS plus affected visual/interaction states; report unperformed browser checks.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
