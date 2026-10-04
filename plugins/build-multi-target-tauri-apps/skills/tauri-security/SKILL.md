---
name: tauri-security
description: Use when adding or auditing Tauri commands, capabilities, permissions, remote content, filesystem/network access, credentials or privileged native integrations.
license: MIT
---

# Tauri Capabilities and Security

Read [common operating contract](../.shared/operating-model.md) before work and [security reference](../.shared/security.md) for this workflow. Current sources and adaptation rationale: [research ledger](../.shared/research.md).

## When to invoke

Use when adding or auditing Tauri commands, capabilities, permissions, remote content, filesystem/network access, credentials or privileged native integrations.

## Inputs and evidence

Rust privileged handlers, permissions/scopes, capabilities/config, remote navigation/services, credentials lifecycle, dependencies and test/release variants.

## Workflow

1. Inventory entry points, sensitive assets, invoke handlers, plugins, window labels/origins, capability files and effective target config.
2. Calculate actual grant union and custom-command exposure using [security reference](../.shared/security.md). Check AppManifest restriction and Rust-side scope/authorization rather than assuming capability JSON protects all handlers.
3. Review production CSP, remote API access, URL/navigation/path validation, HTTP scopes, sidecar arguments, native permissions and resource bounds.
4. Select secret storage with explicit platform/key lifecycle; inspect frontend env exposure and redaction. Keep test instrumentation absent from production.
5. Apply in-scope corrections when authorized; otherwise report located findings with reachable impact and recommended correction. Validate allowed/denied native paths through [tauri-testing](../tauri-testing/SKILL.md).
6. Report exact reviewed targets/revision, verified controls, unresolved findings and residual limits; release-sensitive issues feed [tauri-distribution](../tauri-distribution/SKILL.md).

## Outputs and handoff

Located findings or bounded fixes, command/window/origin matrix, denial-test evidence and release blockers.

## Completion evidence

Effective grant and backend enforcement inspected; changed sensitive paths have native or explicitly limited evidence.

## Must not

Disable CSP to repair dev, grant wildcards for convenience, expose secrets, infer custom scope enforcement from JSON or claim comprehensive security from mocks.
