---
name: electron-development
description: "Use when implementing Electron windows, preload bridges, IPC, native modules, updates, or desktop packaging."
---

# Electron Development Guidelines

## When to invoke

Use when implementing Electron windows, preload bridges, IPC, native modules, updates, or desktop packaging. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Electron/Node/Chromium versions, main/preload/renderer code, trusted origins, permissions, target platforms, and update/signing configuration. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace each privileged action from renderer through preload to main and define narrow allowed operations.
2. Implement isolated/sandboxed windows, typed validated IPC, owned listeners/resources, and explicit file/navigation permissions.
3. Check hostile IPC senders/paths, window lifecycle, renderer compromise boundaries, native ABI and signed packaged behavior.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
