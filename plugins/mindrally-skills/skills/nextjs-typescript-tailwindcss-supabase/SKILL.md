---
name: nextjs-typescript-tailwindcss-supabase
description: "Use when building Next.js and Tailwind interfaces with Supabase authentication, database access, or SSR."
---

# Next.js TypeScript TailwindCSS Supabase

## When to invoke

Use for building Next.js and Tailwind interfaces with Supabase authentication, database access, or SSR.

## Inputs and evidence

Inspect Next.js/Tailwind/Supabase versions, SSR client factories, cookies, RLS policies, key types and data ownership. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use supported server/browser Supabase client boundaries for the project generation.
2. Implement server-verified identity and database authorization with explicit RLS.
3. Build responsive accessible UI with loading, mutation/error and session refresh behavior.
4. Test SSR, denied/authorized data access, session expiry and rendered user flows.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Framework build and isolated Supabase auth/RLS tests establish real server/browser data boundaries.

## Must not

Do not use a privileged key to make a client-side authorization test pass. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
