---
name: nuxtjs-vue-typescript
description: "Use when building typed Nuxt/Vue pages, composables, server APIs, runtime configuration, or SSR data flows."
---

# NuxtJS Vue TypeScript Development

## When to invoke

Use for building typed Nuxt/Vue pages, composables, server APIs, runtime configuration, or SSR data flows.

## Inputs and evidence

Inspect Nuxt/Vue version and directory conventions, Nitro target, data-fetch composables, runtimeConfig and client/server state ownership. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use the installed generation’s app/server structure and existing component/style conventions.
2. Implement SSR-safe useFetch/useAsyncData flows with clear keys and errors.
3. Keep private runtime configuration and authorization in server code.
4. Build and test SSR hydration, navigation, locale/accessibility and target runtime behavior.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Configured build and SSR/navigation tests establish hydration, request-isolated data, config privacy and interactive behavior.

## Must not

Do not place secrets in public runtimeConfig or assume browser globals exist during SSR. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
