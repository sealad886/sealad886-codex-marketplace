---
name: hono-typescript
description: "Use when implementing typed Hono routes, middleware, validation, runtime bindings, or API tests on supported JavaScript runtimes."
---

# Hono TypeScript Development

## When to invoke

Use for Hono APIs with the project’s selected edge or server runtime.

## Inputs and evidence

Inspect Hono major version, runtime adapter, bindings, middleware order, route inference, authentication, and validation dependencies. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Match the entrypoint and environment types to the actual runtime.
2. Implement validated routes and composable middleware with explicit response types and errors.
3. Enforce authentication and resource authorization; keep secrets in supported bindings or server configuration.
4. Run route tests with real middleware and build the selected runtime adapter.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Type checking/build and representative request tests establish validation, authorization, response status, middleware order, and runtime compatibility.

## Must not

Do not ship placeholder secrets, presume all runtimes expose Cloudflare bindings, or accept client-selected privileged roles. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
