---
name: nextauth-authentication
description: "Use when integrating Auth.js or NextAuth sessions, providers, callbacks, server authorization, or runtime-compatible adapters."
---

# NextAuth Authentication

## When to invoke

Use for integrating Auth.js or NextAuth sessions, providers, callbacks, server authorization, or runtime-compatible adapters.

## Inputs and evidence

Inspect exact next-auth/Auth.js release, Next.js router/runtime, adapter/provider versions, session strategy, cookies and credential storage. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use configuration and handler APIs from the installed generation rather than forcing a beta install.
2. Implement provider/session callbacks with validated types and minimal client exposure.
3. Authorize every sensitive route/action on the server and scope data to the authenticated identity.
4. Test session lifecycle, denied actions, callback errors, cookie settings and runtime/adapter compatibility.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Actual-version integration tests cover sign-in/out, refresh/expiry, access denial and chosen runtime behavior.

## Must not

Do not trust client session state as authorization or expose provider/session secrets. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
