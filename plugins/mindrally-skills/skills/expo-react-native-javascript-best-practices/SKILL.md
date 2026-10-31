---
name: expo-react-native-javascript-best-practices
description: "Use when building JavaScript Expo/React Native screens, navigation, lists, images, or native interactions."
---

# Expo React Native JavaScript Best Practices

## When to invoke

Use when building JavaScript Expo/React Native screens, navigation, lists, images, or native interactions. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Expo SDK/React Native/React versions, navigation stack, native modules, runtime configuration, device targets, and app state. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace navigation and screen/data state, including lifecycle, permissions, offline behavior, and native-module availability.
2. Implement the selected feature with supported Expo modules, accessible native controls, and measured list/image behavior.
3. Run type/lint/unit checks as applicable and exercise keyboard/safe areas, navigation, backgrounding, errors, and target devices.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
