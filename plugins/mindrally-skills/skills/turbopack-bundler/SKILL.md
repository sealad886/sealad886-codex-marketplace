---
name: turbopack-bundler
description: "Use when configuring or debugging Next.js Turbopack resolution, loaders, caching, build compatibility, or measured build performance."
---

# Turbopack Next.js builds

## When to invoke

Use when configuring or debugging Next.js Turbopack resolution, loaders, caching, build compatibility, or measured build performance.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Next.js/Turbopack/Node versions, actual dev/build scripts, config, custom webpack behavior, loaders, and failure traces.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Reproduce the build issue at the installed Next version and identify supported bundler mode.
2. Translate only needed configuration to documented Turbopack options.
3. Run development and production checks separately and compare artifact/runtime behavior.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run installed-version dev/build/type checks and the affected route/asset behavior; measure comparable clean/warm builds for performance claims.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
