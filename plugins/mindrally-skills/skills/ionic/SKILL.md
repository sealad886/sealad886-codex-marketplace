---
name: ionic
description: "Use when building Ionic interfaces, routing, platform-aware navigation, or Capacitor native integrations."
---

# Ionic Development

## When to invoke

Use for Ionic Angular, React, or Vue projects, retaining the selected integration.

## Inputs and evidence

Inspect Ionic/framework versions, Capacitor or existing Cordova stack, router conventions, platform permissions, and device targets. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use the project’s framework integration and Ionic page/navigation lifecycle.
2. Build accessible Ionic components and theme through supported CSS variables and parts.
3. Connect required native APIs through supported plugins with permission/fallback handling.
4. Build target platforms and verify navigation, overlays, keyboard, and plugin failure paths.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Framework checks and target-platform tests demonstrate working routing, lifecycle cleanup, accessible overlays, and native permissions.

## Must not

Do not impose Angular on React/Vue projects or introduce obsolete Ionic Native camera wrappers into new Capacitor code. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
