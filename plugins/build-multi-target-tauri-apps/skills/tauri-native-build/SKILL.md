---
name: tauri-native-build
description: Use when setting up, building, running or debugging Tauri native desktop/mobile targets, plugins, deep links, windows or native bridges.
license: MIT
---

# Tauri Native Build and Debug

Read [common operating contract](../.shared/operating-model.md) before work and [build-and-platforms reference](../.shared/build-and-platforms.md) for this workflow. Current sources and adaptation rationale: [research ledger](../.shared/research.md).

## When to invoke

Use when setting up, building, running or debugging Tauri native desktop/mobile targets, plugins, deep links, windows or native bridges.

## Inputs and evidence

Target request, host/SDK/NDK/JDK/Rust versions, package scripts, merged config, Xcode/Gradle integration, device lists, build/runtime logs.

## Workflow

1. Inspect manifests/locks, config overlays, generated projects and scripts; record requested target and exact host/toolchain/device identity.
2. Follow [build/platform runbook](../.shared/build-and-platforms.md). Use installed local CLI help/info; resolve target prerequisites and first causal build failure without global installs or blanket upgrades.
3. Initialize only absent requested target projects, preserving customization. Connect static frontend output/dev URL; verify mobile TAURI_DEV_HOST and HMR reachability.
4. Prefer target-supported official plugins. Reconcile Rust registration, JS calls, capabilities and native usage declarations; guard unsupported compile-time dependencies.
5. Build/launch exact variant through canonical CLI/native workflow. Validate app identity and live screen/logs before interaction; route UI/IPC proof to [tauri-testing](../tauri-testing/SKILL.md).
6. For actual missing native features design narrow Swift/Kotlin bridge, target-scoped desktop integration or sidecar with shared domain ownership; validate error/lifecycle behavior.

## Outputs and handoff

Build/debug changes, exact artifact/device identity, causal diagnosis, launch evidence and setup gaps.

## Completion evidence

Requested build/run reaches actual app behavior or environmental/product failure is precisely located and separated.

## Must not

Overwrite generated projects, guess tool APIs, run unscoped device installs, promise desktop-only plugins/sidecars on mobile or silently sign/upload.
