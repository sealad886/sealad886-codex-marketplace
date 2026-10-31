---
name: convex
description: "Use when implementing Convex queries, mutations, actions, HTTP routes, subscriptions, scheduled jobs, or file storage."
---

# Convex Development Guidelines

## When to invoke

Use when implementing Convex queries, mutations, actions, HTTP routes, subscriptions, scheduled jobs, or file storage. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Convex version/generated APIs, schema/indexes, function visibility, auth/ownership policy, transaction needs, and client integration. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define validators and authorized access for each public function and resource, including files and webhooks.
2. Implement transactional reads/writes separately from action side effects and choose bounded indexed/paginated queries.
3. Test schema validity, denied access, cross-user isolation, retry/idempotency, pagination, and real-time client state.

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
