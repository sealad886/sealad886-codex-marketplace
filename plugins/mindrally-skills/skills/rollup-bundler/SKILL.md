---
name: rollup-bundler
description: "Use when configuring Rollup outputs, plugins, externals, code splitting, tree shaking, or package exports."
---

# Rollup library bundling

## When to invoke

Use when configuring Rollup outputs, plugins, externals, code splitting, tree shaking, or package exports.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Rollup/plugin versions, module type, entrypoints, consumers, package exports, and artifact size baseline.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define supported consumers and output formats before choosing bundle configuration.
2. Configure only needed plugins, external boundaries, and intentional side-effect handling.
3. Build and exercise the published artifact through its supported import paths.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run the configured build and smoke-test each supported package export/format, including external imports and required side effects.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
