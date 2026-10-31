---
name: nodejs-development
description: "Use when developing Node.js TypeScript services, Payload integrations, validated APIs, or Vue-backed client/server contracts."
---

# Node.js Development Guidelines

## When to invoke

Use for developing Node.js TypeScript services, Payload integrations, validated APIs, or Vue-backed client/server contracts.

## Inputs and evidence

Inspect Node/module/runtime versions, package exports, framework integrations, external input schemas, auth policies and async resource ownership. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Implement requested service behavior within the established Node/framework stack.
2. Validate untrusted input and authorize resource-level operations before side effects.
3. Handle async errors, cancellation, timeouts and bounded concurrency.
4. Run type/build and API/integration checks including denied/failed operations.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Tests cover API validation, resource authorization, async failure/cleanup and framework-specific integration behavior.

## Must not

Do not infer runtime safety from TypeScript casts or logged-in status alone. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
