---
name: tauri-app-builder
description: Use when creating, adapting or delivering a Tauri 2 app across desktop, iOS, Android and an optional browser target; route focused work to the smallest relevant workflow.
license: MIT
---

# Build Multi-target Tauri Apps

Read [common operating contract](../.shared/operating-model.md) before work and [operating-model reference](../.shared/operating-model.md) for this workflow. Current sources and adaptation rationale: [research ledger](../.shared/research.md).

## When to invoke

Use when creating, adapting or delivering a Tauri 2 app across desktop, iOS, Android and an optional browser target; route focused work to the smallest relevant workflow.

## Inputs and evidence

User goal, target list, repository status/instructions, manifests/locks, native projects, existing CI/tests and current tool availability.

## Workflow

1. Inspect repository and recover requested user outcome, existing stack and target set. Record versions, toolchains, dirty files and authority using the shared discovery receipt.
2. Define one critical user flow and per-target feature/evidence matrix. Separate unsupported targets and optional browser deployment from required native behavior. Resolve only decisions that block work.
3. For architecture/IPC/persistence load [tauri-architecture](../tauri-architecture/SKILL.md). For UI load [tauri-frontend](../tauri-frontend/SKILL.md). For native target setup/run load [tauri-native-build](../tauri-native-build/SKILL.md). For privileged changes load [tauri-security](../tauri-security/SKILL.md).
4. Implement smallest complete slice through canonical app modules; maintain one active checklist item. Use [build/platform reference](../.shared/build-and-platforms.md) and [research ledger](../.shared/research.md), checking relevant current docs against installed versions.
5. Run [tauri-testing](../tauri-testing/SKILL.md) for changed contracts and requested targets. Route measured slowness/leaks to [tauri-performance](../tauri-performance/SKILL.md), packaging/preparation to [tauri-distribution](../tauri-distribution/SKILL.md).
6. Report actual per-target state and remaining executable proof steps. Do not claim all targets complete from a single host build.

## Outputs and handoff

Working slice or bounded adaptation, target/feature matrix, changed paths, commands/evidence, gaps and Git/release status.

## Completion evidence

Requested slice implemented and relevant target behavior verified, or specific blocked targets remain explicitly identified.

## Must not

Copy native SwiftUI/Compose recipes into WebView UI; require companion plugins; reset devices; publish or use signing credentials without authority.
