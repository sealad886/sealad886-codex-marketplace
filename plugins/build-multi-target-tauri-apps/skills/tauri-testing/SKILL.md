---
name: tauri-testing
description: Use when testing, reproducing or verifying Tauri behavior across Rust, frontend, packaged desktop, iOS simulator/device or Android emulator/device.
license: MIT
---

# Tauri Testing and Device QA

Read [common operating contract](../.shared/operating-model.md) before work and [validation reference](../.shared/validation.md) for this workflow. Current sources and adaptation rationale: [research ledger](../.shared/research.md).

## When to invoke

Use when testing, reproducing or verifying Tauri behavior across Rust, frontend, packaged desktop, iOS simulator/device or Android emulator/device.

## Inputs and evidence

Requirements, changed diff, build artifacts/digests, test config, automation provider/tool versions, native devices and runtime logs.

## Workflow

1. Map changed requirements to narrow behavioral checks and target matrix. Identify exact revision/artifact, runtime/build profile, supported methods and authority.
2. Follow [validation reference](../.shared/validation.md). Run existing Rust/frontend checks and clean up mocks/listeners; distinguish source, mock, browser and native evidence.
3. For desktop discover configured WebdriverIO provider or native harness. Verify versions; keep embedded automation in explicit test-only variants. Direct tauri-driver is Windows/Linux; embedded WDIO can support macOS. Never infer mobile support.
4. For Android select explicit serial/package/activity and inspect live UI/logs. For iOS select exact UDID/generated project/scheme and verify bundle/live screen. Use documented available tools; preserve device data and other sessions.
5. Exercise changed success/failure/denied boundary plus relevant back/keyboard/resume/restart behavior. Capture fresh state after interaction; incomplete WebView UI trees require supported WebView or manual evidence.
6. Triage first causal failure, apply authorized bounded repair and rerun affected scenario. Report all requested targets, pass/fail/not-run/blocked and limitations.

## Outputs and handoff

Requirement-to-method results, commands/exits, target/artifact identity, captures, causal failures and remaining proof gaps.

## Completion evidence

Relevant tests executed and observed results bound to exact target/artifact; unsupported checks clearly identified.

## Must not

Call browser tests real IPC proof, leave production automation endpoints, reset user devices/data, clear shared logs or declare success from an empty/incorrect screen.
