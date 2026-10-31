---
name: monorepo-tamagui
description: "Use when building Tamagui cross-platform UI and shared packages in a Next.js and Expo workspace."
---

# Monorepo using Tamagui

## When to invoke

Use for building Tamagui cross-platform UI and shared packages in a Next.js and Expo workspace.

## Inputs and evidence

Inspect Tamagui/React/Expo/Next.js versions, compiler and bundler configuration, tokens/themes, package exports and platform targets. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Align supported packages and configure the existing Tamagui provider/theme path.
2. Share components and tokens where web/native semantics agree.
3. Implement platform navigation/images and data boundaries using installed integrations.
4. Build web/native targets and test themes, hydration, accessibility and package resolution.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Both targeted builds and representative shared-component/theme/hydration/accessibility tests pass.

## Must not

Do not call web-only or native-only verification complete cross-platform acceptance. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
