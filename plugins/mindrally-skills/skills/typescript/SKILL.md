---
name: typescript
description: "Use when designing TypeScript interfaces, narrowing unknown data, generics, module boundaries, or strictness improvements."
---

# TypeScript contracts and narrowing

## When to invoke

Use when designing TypeScript interfaces, narrowing unknown data, generics, module boundaries, or strictness improvements.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect TypeScript version, tsconfig inheritance, runtime/module target, public types, untrusted input boundaries, and existing tests.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Describe runtime behavior and model its valid states with precise types.
2. Use narrowing and generics to preserve information without unsafe casts.
3. Run the actual compiler/project references and behavior tests for changed boundaries.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run the configured compiler and relevant behavior tests, checking public inference and invalid input handling where changed.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
