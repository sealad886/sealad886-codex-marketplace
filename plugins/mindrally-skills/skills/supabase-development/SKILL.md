---
name: supabase-development
description: "Use when connecting Supabase to application SSR, database migrations, auth lifecycle, storage, realtime, or Edge Functions."
---

# Supabase application integration

## When to invoke

Use when connecting Supabase to application SSR, database migrations, auth lifecycle, storage, realtime, or Edge Functions.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect framework and supabase-js/SSR versions, cookie handling, auth hooks, migrations, RLS grants, and deployment configuration.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Use the application’s existing supported Supabase client/session construction.
2. Implement scoped schema/policy and auth lifecycle changes with explicit ownership checks.
3. Verify real role isolation and session refresh/error paths in an isolated project or local stack.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run migrations and role/session tests with synthetic accounts, including expired sessions, unauthorized writes, and storage/channel cleanup.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
