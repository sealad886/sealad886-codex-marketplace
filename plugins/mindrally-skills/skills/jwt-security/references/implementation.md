# JWT Security: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Validation and keys

- A signed compact JWS commonly has three segments; encrypted JWTs use JWE and have a different representation. Encoding alone provides no confidentiality.
- JWT claim requirements come from the application/profile; RFC 7519 does not universally require iss/sub/aud/exp/iat on every JWT. Explicitly require the claims needed by the selected profile.
- Allow only trusted algorithms matched to key type; select keys from a configured issuer/key set, never arbitrary token-provided URLs or file paths.
- Require expiration when the profile needs it; reject at or after exp, subject to a deliberate clock-skew policy.

## Lifecycle and storage

- kid, typ, and jti serve profile-specific purposes; none is a universal security guarantee and EdDSA is not inherently the single most secure choice.
- Choose cookie or bearer-header transport deliberately. HttpOnly cookies require CSRF consideration; bearer values must stay out of URLs/logs.
- Rotate refresh tokens atomically with replay detection; revoking the old token after independently issuing replacements permits concurrent reuse races.
- Revocation state must have durable consistency and retention appropriate to token expiry; a process-local Set does not revoke across services.

## Primary documentation

- [Primary documentation](https://www.rfc-editor.org/rfc/rfc8725.html) — JWT best current practice requires algorithm verification, audience/issuer validation, explicit typing where useful, and mutually exclusive validation rules.
- [JWT standard](https://www.rfc-editor.org/rfc/rfc7519.html) — Registered claim requirements are application-specific and expiration is invalid at or after exp.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
