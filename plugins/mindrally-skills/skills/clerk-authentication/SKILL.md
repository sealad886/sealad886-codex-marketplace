---
name: clerk-authentication
description: "Use when integrating Clerk authentication, server authorization, organization access, or session handling in Next.js."
---

# Clerk Authentication

## When to invoke

Use when integrating Clerk authentication, server authorization, organization access, or session handling in Next.js. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Clerk/Next.js versions, router/render/cache mode, middleware or proxy file, claims configuration, resource ownership, and SDK keys. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace server entry points and data access; define authentication plus resource/organization authorization independently.
2. Implement supported provider/middleware and protect every sensitive server action, handler, and data path with runtime validation.
3. Test signed-out, expired, wrong-user/wrong-organization, insufficient-role, redirect, and cache-isolation behavior.

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
