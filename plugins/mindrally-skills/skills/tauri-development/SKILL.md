---
name: tauri-development
description: "Use when implementing Tauri frontend/Rust commands, permissions, events, filesystem access, native builds, or desktop/mobile integration."
---

# Tauri application boundaries

## When to invoke

Use when implementing Tauri frontend/Rust commands, permissions, events, filesystem access, native builds, or desktop/mobile integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Tauri major/plugins, Rust/JS versions, capabilities, command registration, frontend output, target platforms, and signing configuration.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define the smallest native command and permission boundary needed by the UI.
2. Implement version-correct IPC with validated inputs and owned resources.
3. Verify command errors, denied capabilities, lifecycle cleanup, and target-specific builds.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run Rust/frontend checks plus allowed/denied IPC and path tests; build intended native targets and identify device/signing/distribution gaps.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
