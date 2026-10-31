---
name: sass-best-practices
description: "Use when implementing .sass stylesheets, modules, mixins, maps, calculations, or compilation fixes."
---

# Indented Sass modules

## When to invoke

Use when implementing .sass stylesheets, modules, mixins, maps, calculations, or compilation fixes.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Dart Sass version, .sass entrypoints, module imports, token ownership, compiled selectors, and browser targets.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Follow the project’s indented syntax and identify the owning stylesheet/module.
2. Use scoped modules and current built-in APIs for the needed abstraction.
3. Compile and inspect CSS behavior, specificity, bundle size, and accessibility.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Compile all affected entrypoints with the pinned compiler and check rendered responsive/focus behavior plus CSS-size changes where relevant.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
