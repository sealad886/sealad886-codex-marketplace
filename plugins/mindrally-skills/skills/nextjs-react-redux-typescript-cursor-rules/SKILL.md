---
name: nextjs-react-redux-typescript-cursor-rules
description: "Use when building Next.js and React features using Redux Toolkit, typed state, hydration, or client/server data boundaries."
---

# Next.js React Redux TypeScript Cursor Rules

## When to invoke

Use for building Next.js and React features using Redux Toolkit, typed state, hydration, or client/server data boundaries.

## Inputs and evidence

Inspect Next.js/router and Redux versions, store creation/provider lifetime, server data flow, persistence and route-reset requirements. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Separate server-owned fetched data from mutable client state requiring Redux.
2. Create request-safe store instances and expose them through an appropriate client provider.
3. Implement typed slices/selectors and explicit hydration/reset behavior.
4. Test cross-request isolation, navigation, mutations, errors and user-visible UI behavior.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

SSR and client tests show isolated state, hydration consistency, correct route/user resets and intended updates.

## Must not

Do not share server stores across users or assume typed state validates incoming data. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
