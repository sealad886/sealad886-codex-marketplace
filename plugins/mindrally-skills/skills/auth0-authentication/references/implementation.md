# Auth0 Authentication: implementation guidance

## Application and token security

SPAs and native apps use Authorization Code with PKCE; public clients have no
client secret. Prefer browser memory for token storage unless a reviewed threat
model justifies persistence. Server apps use the supported SDK and protected
session cookies. Allowlist exact production redirects and use TLS, with documented
loopback development exceptions where applicable. Validate API access tokens at
the API and enforce scopes/ownership; ID tokens are for the client, not API access.

## Actions and session policy

Use Actions rather than adding legacy Rules. Keep secrets in Action secrets and
bound external calls within the documented trigger execution limits; a total
execution limit is not a default HTTP timeout. Set token/session lifetimes by risk,
not a fabricated universal one-hour maximum. Enable refresh rotation and reuse
detection only through authorized tenant configuration. Check supported enrolled
MFA factors and plan/trigger APIs before issuing challenges. Avoid logging user
identifiers or full event objects unnecessarily. Auth0 MCP tooling is an optional
separately installed integration; this skill supplies no server or tenant access.

## Primary documentation

- [Browser token storage guidance](https://auth0.com/docs/secure/security-guidance/data-security/token-storage).
- [Rotation and reuse detection](https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation).
- [Actions execution limits](https://auth0.com/docs/customize/actions/limitations).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
