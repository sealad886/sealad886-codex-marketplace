---
name: apollo-graphql
description: "Use when implementing Apollo Client GraphQL queries, mutations, normalized caching, pagination, or React integration."
---

# Apollo GraphQL Best Practices

## When to invoke

Use when implementing Apollo Client GraphQL queries, mutations, normalized caching, pagination, or React integration. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Apollo Client major version, schema/generated operation types, authentication isolation, cache policies, and rendering environment. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Identify the operation and cache ownership contract, including user/session boundaries and pagination arguments.
2. Implement typed queries/mutations and version-correct hooks/links with explicit loading, error, empty, and partial-data handling.
3. Check cache updates, optimistic rollback, pagination deduplication/reset, auth changes, and server-side request isolation.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
