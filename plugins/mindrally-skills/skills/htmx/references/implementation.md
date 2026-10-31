# HTMX Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Requests and fragments

- Use hx-get for safe retrieval and mutation methods for state changes; the server must validate and authorize each request.
- hx-target selects the destination and hx-swap controls insertion; return fragments compatible with that destination.
- Use hx-trigger delay/throttle and hx-sync when overlapping requests could produce stale state.

## Errors, history, and security

- Default response handling does not swap most 4xx/5xx bodies. Configure responseHandling or an appropriate response event/extension when errors should render.
- Preserve accessible labels, focus and pending indicators; provide a usable baseline when progressive enhancement is a requirement.
- History snapshots can contain sensitive HTML; avoid caching protected content and test direct navigation to pushed URLs.
- Use appropriate CSRF defenses, escaped server templates, and deliberate handling of injected scripts and untrusted hx attributes.

## Primary documentation

- [htmx documentation](https://htmx.org/docs/) — Request/swap semantics, configurable response handling, history, and security behavior.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
