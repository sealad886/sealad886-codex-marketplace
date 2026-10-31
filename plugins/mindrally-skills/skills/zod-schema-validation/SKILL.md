---
name: zod-schema-validation
description: "Use when defining Zod schemas, parsing untrusted data, inferring input/output types, transforming values, or reporting validation errors."
---

# Zod runtime validation

## When to invoke

Use when defining Zod schemas, parsing untrusted data, inferring input/output types, transforming values, or reporting validation errors.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Zod/TypeScript versions, boundary data representation, coercion/refinement needs, error UI, and schema reuse.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define the actual external representation and accepted business constraints.
2. Compose version-correct schemas and choose synchronous or async parsing appropriately.
3. Verify valid/invalid inputs, transformed outputs, unknown fields, and accessible error mapping.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run focused boundary tests for malformed/valid/date/coerced/async inputs, extra keys, transformations, and nested error presentation.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
