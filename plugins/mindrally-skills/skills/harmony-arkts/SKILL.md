---
name: harmony-arkts
description: "Use when building HarmonyOS ArkTS and ArkUI components, state models, resources, lifecycle behavior, or accessible layouts."
---

# HarmonyOS ArkTS Development

## When to invoke

Use for HarmonyOS .ets application code and ArkUI interactions.

## Inputs and evidence

Inspect HarmonyOS SDK/API level, ArkTS restrictions, ArkUI state-management generation, target devices, and existing resource conventions. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Select the component and state model already supported by the project SDK.
2. Implement owned state and deliberate parent/child data flow; keep business operations outside UI composition.
3. Use app resources and responsive ArkUI layouts with intentional event and lifecycle cleanup.
4. Build with the selected SDK and check lifecycle, state propagation, accessibility, and device sizes.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

The target SDK builds the component and tests demonstrate intended state ownership, lifecycle cleanup, resource lookup, and accessible interaction.

## Must not

Do not treat ArkTS as unrestricted TypeScript or mix incompatible state-management decorator generations. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
