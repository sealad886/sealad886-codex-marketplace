---
name: react-native-cursor-rules
description: "Use when changing React Native components, virtualized lists, navigation, styling, or device performance."
---

# React Native implementation

## When to invoke

Use when changing React Native components, virtualized lists, navigation, styling, or device performance.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect React Native/Expo versions, target platforms, list item geometry, navigation setup, and release-build traces.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Reproduce the platform-specific interaction and identify JavaScript, layout, image, or native work.
2. Implement typed components using existing navigation and styling conventions.
3. Tune list and image behavior against measured device evidence; verify focus, touch, and orientation behavior.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run component checks and the changed navigation/list flow on available target devices; identify omitted native or update delivery checks.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
