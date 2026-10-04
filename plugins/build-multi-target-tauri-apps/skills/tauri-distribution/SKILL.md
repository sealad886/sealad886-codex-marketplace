---
name: tauri-distribution
description: Use when preparing or verifying Tauri packages, native signing/entitlements, CI builds, desktop updates or mobile/browser distribution.
license: MIT
---

# Tauri Packaging and Distribution

Read [common operating contract](../.shared/operating-model.md) before work and [distribution reference](../.shared/distribution.md) for this workflow. Current sources and adaptation rationale: [research ledger](../.shared/research.md).

## When to invoke

Use when preparing or verifying Tauri packages, native signing/entitlements, CI builds, desktop updates or mobile/browser distribution.

## Inputs and evidence

Exact artifact/revision, channel policy, version owner, merged configuration, native signing metadata, CI scripts and actual test evidence.

## Workflow

1. Pin release unit, target/channel, revision/digest, owning versions/identifiers, locks/toolchain and exact execution authority.
2. Follow [distribution reference](../.shared/distribution.md). Inspect scripts/CI for build, signing, credential, upload and publication effects before running.
3. Reconcile version/config across selected native artifacts; inspect architecture, resources, entitlements/profile/WebView dependencies and removal of test tooling.
4. Separate OS signing, notarization, updater signature, store submission and install/launch evidence. Desktop updater remains desktop-only; mobile uses intended store/device channel.
5. Design/update recovery and schema conversion with local backup and verified restore/downgrade limits. Verify prepared artifact through [tauri-testing](../tauri-testing/SKILL.md) and sensitive controls through [tauri-security](../tauri-security/SKILL.md).
6. Report per-target release gate. Execute consequential steps only when explicitly authorized, retaining exact provider receipts/readback; preparation alone ends with a reviewable result.

## Outputs and handoff

Prepared/inspected packages, target/channel gate matrix, signature/update/recovery evidence and pending authorized actions.

## Completion evidence

Claims tied to exact artifacts; missing gates stated; published outcome claimed only with actual receipt and readback.

## Must not

Use signing credentials, notarize, publish/store-upload/deploy without authority; confuse updater signature with OS signing or treat CI green as installed user success.
