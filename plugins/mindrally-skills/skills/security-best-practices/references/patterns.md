# Secure application boundaries: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Validate structure and business constraints at entry; encode output for its destination. A single sanitize-before-storage step does not prevent every injection class.

- Bind SQL values through parameterized APIs; allowlist identifiers/SQL structure where binding is unavailable. ORM raw queries can still be injectable.

- Enforce resource/tenant authorization server-side for every sensitive request; authentication and a hidden control are insufficient.

- Use maintained password hashing and session libraries, secure cookie settings, expiry, and revocation according to the application’s design.

- CSRF defenses apply to ambiently authenticated requests; use the framework’s tokens/origin protections. SameSite and CORS are not universal replacements.

- Bound retries to idempotent or explicitly idempotency-protected operations; timeouts, backoff, and connection limits must not multiply duplicate writes.

- Keep secrets out of code/logs, use supported secret storage and narrow service identities, and rotate confirmed exposures with consumer coordination.

- Choose CSP/HSTS/frame controls for the deployment and test their effect; scanner output and configured headers alone do not prove security.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Parameterized values and allowlisted SQL structure are primary injection defenses.](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [CSRF controls depend on credential and request context.](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Request_Forgery_Prevention_Cheat_Sheet.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
