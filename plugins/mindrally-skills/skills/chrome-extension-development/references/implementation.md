# Chrome Extension Development: implementation guidance

## MV3 lifecycle and permissions

Register service-worker listeners synchronously and persist required state outside
global memory. Timers do not reliably survive worker termination; alarms require
the alarms manifest permission, missing in the upstream combined example. Recheck
alarms/state on relevant startup paths. chrome.storage read-modify-write is not
an atomic increment: coordinate concurrent updates through one owner or use an
appropriate transactional store. Handle Promise/callback API support and errors
for the minimum Chrome version.

## Messaging, UI, and distribution

Validate message shape, sender/origin, and allowed operations before privileged
work; do not expose arbitrary URL fetch or script execution to page messages.
Keep host permissions and web_accessible_resources narrowly scoped. MV3 CSP
restricts executable code sources; do not add remote hosted code or eval. Extension
storage is not a secret vault. Popups close and workers restart, so design durable
work and user feedback accordingly. Check keyboard/accessible names and chrome.i18n
locales. Store submission/privacy declarations and browser portability require
separate current validation and explicit publishing authority.

## Primary documentation

- [Worker listeners, persistence and alarms permission](https://developer.chrome.com/docs/extensions/get-started/tutorial/service-worker-events).
- [Messaging trust boundaries](https://developer.chrome.com/docs/extensions/develop/concepts/messaging).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
