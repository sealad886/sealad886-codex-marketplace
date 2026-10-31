---
name: postcss-best-practices
description: "Use when configuring PostCSS transforms, browser targets, nesting, prefixing, minification, or CSS plugin pipelines."
---

# PostCSS Best Practices

## When to invoke

Use for configuring PostCSS transforms, browser targets, nesting, prefixing, minification, or CSS plugin pipelines.

## Inputs and evidence

Inspect PostCSS/plugin versions, ESM/CommonJS config loading, framework defaults, Browserslist targets and generated CSS contract. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Retain the existing build integration and select only required transforms.
2. Order plugins according to their input/output semantics and avoid duplicate transformations.
3. Configure target-specific prefixing/minification without removing required styles/notices.
4. Compile representative CSS and verify rendered output in supported browsers.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Pipeline builds and browser checks show correct nesting/prefixes, retained dynamic classes, notices and visual behavior.

## Must not

Do not add every plugin, strip legal comments, or purge runtime classes without proving the output remains correct. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
