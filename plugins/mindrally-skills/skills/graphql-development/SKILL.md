---
name: graphql-development
description: "Use when designing GraphQL schemas, resolvers, typed operations, pagination, or React and Next.js client integration."
---

# GraphQL Development

## When to invoke

Use for GraphQL application contracts and client/server integration; select the repository’s existing GraphQL client.

## Inputs and evidence

Inspect schema ownership, generated types, resolver context, authorization rules, operation documents, cache policies, and expected query sizes. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define nullability, input types, pagination, and observable error semantics before resolver changes.
2. Implement authorization through the owning business layer and request-scoped batching where needed.
3. Generate or validate typed operations against the schema; update cache behavior for mutations.
4. Check partial data, denied fields, pagination boundaries, and resolver query counts.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Schema/operation validation and representative resolver and client tests establish authorized data access, error handling, and cache behavior.

## Must not

Do not equate generated TypeScript types with runtime input validation or introduce a second client without need. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
