---
name: turborepo
description: "Use when configuring Turborepo task graphs, workspace dependencies, inputs/outputs, filters, or local/remote caching."
---

# Turborepo tasks and cache correctness

## When to invoke

Use when configuring Turborepo task graphs, workspace dependencies, inputs/outputs, filters, or local/remote caching.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Turbo/package-manager versions, workspace manifests, dependency graph, turbo.json, environment inputs, and artifact outputs.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Model task dependencies from real package and artifact ownership.
2. Declare complete cache inputs/outputs and noncacheable persistent work.
3. Verify cold and cached execution produce the same supported artifacts.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run dry-run graph inspection and representative cold/hit/miss checks, including a changed env/input and restored output.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
