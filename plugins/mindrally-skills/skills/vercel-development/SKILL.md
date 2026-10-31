---
name: vercel-development
description: "Use when preparing Vercel application builds, function runtimes, environment scope, preview behavior, or Next.js/AI integration."
---

# Vercel application runtime and delivery

## When to invoke

Use when preparing Vercel application builds, function runtimes, environment scope, preview behavior, or Next.js/AI integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect framework/SDK/runtime versions, project config, deployment target, environment scopes, auth, function limits, and actual preview settings.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Choose runtime and framework APIs from installed versions and platform support.
2. Implement protected routes/functions, bounded work, and deliberate public/server configuration.
3. Build/test locally and verify authorized preview behavior before production publication.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run framework/type/build checks and test protected/invalid/runtime-limited routes; identify unperformed provider, preview, and production checks.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
