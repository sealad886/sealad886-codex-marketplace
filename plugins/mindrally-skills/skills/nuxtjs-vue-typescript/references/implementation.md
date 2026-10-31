# NuxtJS Vue TypeScript Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Nuxt data and configuration

- Nuxt 3 and 4 directory/default behavior differ; inspect the actual app directory instead of mandating one historical layout.
- useFetch/useAsyncData integrate server payload transfer and hydration; direct component fetch calls can duplicate work without proper ownership.
- runtimeConfig private keys stay server-side; runtimeConfig.public values are client-visible and cannot hold secrets.

## Vue and UI

- Composition API/script setup are useful defaults for compatible code, but Options API remains valid and may be project convention.
- Use reactive/ref/computed according to reference semantics and clean up watchers/browser effects; avoid request-shared mutable server state.
- Tailwind, Pinia, VueUse and UI primitives are optional existing integrations; respect installed package renames and APIs.
- Current Core Web Vitals includes INP rather than FID; measure actual pages instead of claiming built-in optimization suffices.

## Primary documentation

- [Primary documentation](https://github.com/nuxt/nuxt/blob/main/docs/4.api/2.composables/use-runtime-config.md) — Nuxt private runtimeConfig stays server-side while public keys are exposed to the client.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
