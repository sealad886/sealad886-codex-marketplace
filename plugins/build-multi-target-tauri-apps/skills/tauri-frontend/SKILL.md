---
name: tauri-frontend
description: Use when building, refining or debugging Tauri frontend layout, navigation, components, accessibility, responsive behavior or browser deployment.
license: MIT
---

# Tauri Frontend and UX

Read [common operating contract](../.shared/operating-model.md) before work and [frontend reference](../.shared/frontend.md) for this workflow. Current sources and adaptation rationale: [research ledger](../.shared/research.md).

## When to invoke

Use when building, refining or debugging Tauri frontend layout, navigation, components, accessibility, responsive behavior or browser deployment.

## Inputs and evidence

Design intent, components, framework/version, frontend config, existing screenshots/runtime, routes/services and requested target interactions.

## Workflow

1. Identify user flow, framework/design system, static build configuration and native services. Inspect current rendered state when available.
2. Define interaction and loading/error/offline/denied states. Follow [frontend reference](../.shared/frontend.md); share domain flow while adapting desktop keyboard/window and mobile touch/safe-area/keyboard behavior.
3. Implement within existing components/framework. For native operations use canonical service and real unavailable behavior on unsupported targets.
4. Discover browser capability/configured test runner; read its instructions before use. Run entry/action/result loop with page/content, console and screenshot evidence before and after changes.
5. Repeat changed native-dependent flow on packaged app via [tauri-testing](../tauri-testing/SKILL.md). Verify actual engine, accessibility and relevant viewports; retain explicit gaps.

## Outputs and handoff

Implemented UI, observed interaction/accessibility evidence, screenshots/capture locations and native/browser limitations.

## Completion evidence

Rendered target flow exercised; relevant layout/focus/error behavior observed; native-dependent claims backed by native evidence.

## Must not

Require React/shadcn; embed unsupported SSR runtime; call browser mocks native verification; use CSS effects as proof of native materials.
