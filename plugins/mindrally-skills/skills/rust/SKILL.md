---
name: rust
description: "Use when implementing Rust ownership, errors, modules, async tasks, channels, or measured performance changes."
---

# Rust implementation and concurrency

## When to invoke

Use when implementing Rust ownership, errors, modules, async tasks, channels, or measured performance changes.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Cargo manifests/lockfile, MSRV, edition, feature flags, public types, runtime, and concurrency ownership.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define ownership, borrowing, and error contracts at the public boundary.
2. Implement the smallest safe module or concurrency change within the existing runtime.
3. Run formatting, compile/lint/tests, then targeted concurrency or performance checks where needed.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Compile supported features/targets and run focused success/failure/concurrency tests; benchmark only performance claims.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
