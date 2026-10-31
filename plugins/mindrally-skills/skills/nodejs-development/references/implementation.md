# Node.js Development Guidelines: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Node and Payload boundaries

- Match ESM/CommonJS and supported Node APIs to package metadata and toolchain; do not assume every Node app needs Vue, Express or Payload.
- Current Payload imports and local API differ from older payload/types recipes; inspect pinned public exports.
- Payload Local API can bypass access control by default; explicitly use the request/user and overrideAccess false when enforcing user permissions.
- Authentication-only collection rules do not establish per-record ownership or publication visibility.

## Client and validation

- A TypeScript generic or JSON assertion does not validate response shape; use runtime schemas at trust boundaries.
- Check response.ok and handle rejected fetches; cancel stale requests and react to changing props where needed.
- Do not accept client-selected admin roles from a create-user schema; privilege comes from server policy.
- Promise.all starts concurrent work but does not bound concurrency or cancel remaining operations after one fails.

## Primary documentation

- [Primary documentation](https://payloadcms.com/docs/local-api/overview) — Payload Local API requires deliberate overrideAccess and user/request context to enforce access policies.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
