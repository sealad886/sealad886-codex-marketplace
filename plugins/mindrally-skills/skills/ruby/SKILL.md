---
name: ruby
description: "Use when implementing Ruby objects, modules, collections, errors, or version-specific language behavior."
---

# Ruby implementation

## When to invoke

Use when implementing Ruby objects, modules, collections, errors, or version-specific language behavior.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Ruby version, Gemfile/lockfile, public interfaces, object lifetime, and the project’s test/lint conventions.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify the public behavior and supported Ruby syntax.
2. Implement clear object/module boundaries and explicit error handling.
3. Run focused behavior tests and profile only the claimed performance path.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run supported Ruby syntax/lint and tests for normal, invalid, and failure cases; document any version-dependent syntax.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
