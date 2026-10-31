# Progressive Web App Development Guidelines: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Caches and updates

- Cache only intended safe GET resources; exclude private/mutation responses unless a deliberate identity-bound policy exists.
- Delete only caches owned by this application/version prefix, never every other cache on the origin.
- skipWaiting/clients.claim can create old-page/new-worker mismatches; coordinate updates instead of enabling them unconditionally.
- An offline HTML fallback belongs to navigation requests, not arbitrary images/API requests.

## Background work and capabilities

- Extend background cache writes with event.waitUntil and handle rejected fetch/update promises; network-first must distinguish HTTP failures from network rejection.
- Background Sync and installation/push criteria vary by browser; feature-detect and provide usable fallback.
- navigator.onLine is a connectivity hint and does not prove the application backend is reachable.
- Persist queued work with identity and idempotency keys, validate responses before dequeue, and handle conflicts/re-authentication.
- Request notification permission in an appropriate user interaction and validate push payloads; audit actual artifacts/flows rather than relying on removed Lighthouse PWA category checks.

## Primary documentation

- [Primary documentation](https://web.dev/learn/pwa/service-workers) — Service workers have scoped lifecycle and browser-support constraints for offline caching and updates.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
