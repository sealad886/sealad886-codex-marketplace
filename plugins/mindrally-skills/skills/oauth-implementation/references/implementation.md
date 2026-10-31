# OAuth Implementation: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Protocol and transaction binding

- OAuth delegates authorization; use OIDC ID-token validation for authentication where required.
- Apply OAuth 2.0 security BCP and provider specifications rather than claiming every OAuth 2.1 draft statement is universally finalized.
- Use authorization code with S256 PKCE where supported; bind state/nonce/issuer to the transaction and reject missing values, not just unequal values.
- Redirect matching and native-loopback exceptions follow the applicable profile; do not hand-build a universal OAuth callback from sample code.

## Tokens and storage

- Access tokens can be opaque or JWTs; resource-server verification/introspection follows issuer metadata and the token profile.
- A browser client cannot keep a client secret; confidential client auth belongs on the server. Check token endpoint status and response schema.
- Refresh rotation/sender constraints and expiry depend on provider policy; persist replacements atomically and handle replay/revocation.
- Choose bearer/cookie/BFF storage deliberately with XSS/CSRF considerations; memory is not universally the most secure architecture.
- Redact provider error descriptions and tokens; never treat an unverified userinfo/decoded payload as identity.

## Primary documentation

- [Primary documentation](https://www.rfc-editor.org/rfc/rfc9700.html) — OAuth security BCP covers PKCE, redirect validation, token replay and transaction-bound CSRF protections.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
