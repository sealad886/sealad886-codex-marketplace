---
name: webpack-bundler
description: "Use when configuring Webpack entry/output, loaders/plugins, code splitting, side effects, caching, or build diagnostics."
---

# Webpack build configuration

## When to invoke

Use when configuring Webpack entry/output, loaders/plugins, code splitting, side effects, caching, or build diagnostics.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Webpack/CLI/dev-server/plugin versions, module target, entries, output ownership, package side effects, and runtime constraints.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Reproduce the build/runtime issue and define required output consumers.
2. Configure only necessary loaders/plugins and accurate side-effect/cache boundaries.
3. Build production output and test chunk/assets loading and required initialization.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run clean and incremental production builds where safe, type/lint checks separately, and smoke-test emitted assets/chunks and side effects.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
