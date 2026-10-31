---
name: less-best-practices
description: "Use when authoring Less variables, mixins, guards, imports, responsive styles, or stylesheet build configuration."
---

# Less CSS Best Practices

## When to invoke

Use for authoring Less variables, mixins, guards, imports, responsive styles, or stylesheet build configuration.

## Inputs and evidence

Inspect Less/compiler version, math mode, imports, bundler plugins, browser targets, and existing CSS architecture. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Organize tokens and reusable mixins around existing styling boundaries.
2. Implement variables, guards, interpolation and detached rulesets using supported syntax.
3. Inspect compiled CSS for selector specificity, duplication, responsive gaps, and accessibility.
4. Run the project compiler and relevant browser/style checks.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Less compiles and generated CSS meets intended selectors, responsive behavior, theme contrast and focus behavior.

## Must not

Do not assume mathematical expressions or vendor-prefix helpers behave identically across compiler versions. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
