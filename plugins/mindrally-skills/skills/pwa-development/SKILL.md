---
name: pwa-development
description: "Use when building web manifests, service-worker offline behavior, cache updates, background sync, or push notifications."
---

# Progressive Web App Development Guidelines

## When to invoke

Use for building web manifests, service-worker offline behavior, cache updates, background sync, or push notifications.

## Inputs and evidence

Inspect target browser/platform support, service-worker scope, existing cache ownership, sensitive routes, update policy and offline data contracts. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define supported offline/install behavior and explicit update/data-conflict requirements.
2. Configure manifest/resources and narrowly scoped service-worker routes.
3. Implement cache lifetimes, safe fetch fallback and queued effects with idempotency.
4. Test install/update/offline/reconnect/logout and browser-specific feature availability.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Target-browser tests demonstrate safe cache ownership, updates, offline/reconnect and authenticated data isolation.

## Must not

Do not erase other origin caches or cache authenticated content across users by default. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
