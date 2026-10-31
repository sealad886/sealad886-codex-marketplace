# Monorepo using Tamagui: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Tamagui UI and toolchains

- Keep Tamagui packages/configuration aligned to the installed generation; compiler and runtime styling have distinct setup requirements.
- Use tokens/themes and responsive primitives with platform-aware behavior; shared components still need accessibility testing on each target.
- Next.js SSR/hydration and native bundler resolution need separate configuration and evidence.

## Workspace integrations

- Keep direct dependencies and exports explicit; verify platform suffix resolution and shared React instance constraints.
- Solito, SolitoImage, Supabase, Zustand and Stripe are optional integrations, not guaranteed current project APIs.
- expo-localization provides locale detection; translations require the selected message library.
- Keep payment/auth server secrets outside shared UI code and test query-cache identity when user/locale changes.

## Primary documentation

- [Primary documentation](https://tamagui.dev/docs/intro/introduction) — Tamagui provides cross-platform components, themes and compiler/bundler integrations with versioned setup.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
