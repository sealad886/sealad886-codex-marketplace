---
name: swr
description: "Use when implementing SWR data keys, conditional fetching, cache scope, optimistic mutations, pagination, or revalidation."
---

# SWR cache and mutation behavior

## When to invoke

Use when implementing SWR data keys, conditional fetching, cache scope, optimistic mutations, pagination, or revalidation.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect SWR version, cache provider boundaries, authentication context, fetcher error semantics, keys, and mutation behavior.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define data identity and cache ownership, including the current account or tenant.
2. Implement conditional reads and failure-aware mutations with deliberate revalidation policy.
3. Test loading/error/stale states, rollback, account changes, and pagination termination.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test missing dependencies, non-2xx mutations/rollback, duplicate requests, cache-provider scope, and infinite-query end conditions.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
