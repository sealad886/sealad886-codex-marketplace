# Electron Development Guidelines: implementation guidance

## Process and IPC boundaries

Keep contextIsolation enabled, nodeIntegration disabled for renderer content,
and sandbox settings deliberate. A preload allowlist alone is insufficient:
main handlers must verify senderFrame/origin and runtime argument schemas.
Expose one narrow method per operation rather than arbitrary channels or raw
ipcRenderer. Do not allow a renderer to read/write any filesystem path supplied
without a reviewed authorization boundary. The upstream bridge never exposes
its renderer readFile call, so that sample is incomplete. Return unsubscribe
functions for subscriptions and remove owned IPC/window listeners on disposal.

## Desktop lifecycle and delivery

Set a restrictive CSP and control navigation, new windows, permission requests,
and shell.openExternal schemes. Avoid blocking main with synchronous file writes
or CPU work. Use workers/utility processes only within their supported APIs.
Rebuild native dependencies for Electron ABI/architecture. Spectron is deprecated;
use current supported test tooling and state its Electron support limits. Updates
need authenticated/trusted metadata, platform-specific signing and user-appropriate
restart handling; do not automatically quitAndInstall on every download. Packaging,
notarization, publication and production update changes need explicit authority.

## Primary documentation

- [IPC sender validation and process security](https://www.electronjs.org/docs/latest/tutorial/security).
- [Spectron deprecation](https://www.electronjs.org/blog/spectron-deprecation-notice).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
