---
name: chrome-extension-development
description: "Use when building Manifest V3 Chrome extensions, content scripts, service workers, popups, messaging, or storage."
---

# Chrome Extension Development

## When to invoke

Use when building Manifest V3 Chrome extensions, content scripts, service workers, popups, messaging, or storage. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Chrome minimum version, manifest permissions/host matches, execution contexts, data flow, and store requirements. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define responsibilities and trust boundaries between page, content script, worker, and extension UI.
2. Implement least-privilege manifest configuration, persistent state, validated messages, and lifecycle-safe event handling.
3. Load an isolated unpacked package and verify worker restarts, permissions, concurrency, navigation, CSP, and UI behavior.

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
