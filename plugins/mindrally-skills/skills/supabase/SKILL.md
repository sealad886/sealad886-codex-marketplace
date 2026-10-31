---
name: supabase
description: "Use when implementing Supabase database access, authentication, RLS, storage, realtime, or Edge Function integration."
---

# Supabase backend boundaries

## When to invoke

Use when implementing Supabase database access, authentication, RLS, storage, realtime, or Edge Function integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Supabase SDK/framework versions, exposed schemas, RLS policies, user/secret client roles, storage permissions, and realtime channels.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define which role may read or mutate each resource.
2. Implement authenticated clients and database/storage policies at the owning boundary.
3. Verify cross-user denial, valid access, session changes, and channel/resource cleanup.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test anonymous, owner, other-user, and privileged access in an isolated environment; verify storage and subscription behavior where changed.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
