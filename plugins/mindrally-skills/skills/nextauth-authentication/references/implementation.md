# NextAuth Authentication: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Sessions and runtime

- Auth.js v5 auth/handlers patterns differ from NextAuth v4 APIs; environment aliases and setup must match the actual version.
- JWT and database sessions have distinct revocation/read costs; early JWT invalidation can require server state, key rotation or other deliberate mechanisms.
- Edge compatibility depends on every adapter/driver dependency. Split configuration commonly uses jwt strategy; the source example omitted it and could mismatch session interpretation.
- Middleware/proxy naming and Node/Edge support depend on Next.js version; middleware is not the only or final authorization boundary.

## Security and data

- Credentials need runtime schema validation, password verification and rate limits; adapters do not automatically supply that policy.
- Keep secure cookie defaults unless a demonstrated integration needs overrides; __Secure prefixes require secure transport.
- Auth.js CSRF/session protections do not automatically protect arbitrary custom mutations; validate inputs, resource access and applicable CSRF policy.
- Client sessions and type assertions do not prove trusted role values; define role freshness/revocation and server-authoritative access checks.

## Primary documentation

- [Primary documentation](https://authjs.dev/guides/edge-compatibility) — Edge support depends on adapter/driver compatibility; split configuration uses a deliberate JWT session strategy.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
