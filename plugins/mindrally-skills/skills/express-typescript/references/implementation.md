# Express TypeScript Development: implementation guidance

## Validation and errors

Express 5 forwards rejected returned promises; Express 4 needs explicit next(err)
or an existing wrapper. Use four-argument error middleware and handle headersSent
by delegating rather than writing a second response. Runtime schemas must validate
and supply parsed data to handlers: the upstream middleware discards parseAsync's
transformed/stripped result. Zod error properties differ by version; use the actual
issues API. Do not cast req.body into trust. Bound JSON/urlencoded input and parse
only expected content types.

## Security and integration

Authentication must parse the scheme and verify signature/issuer/audience/expiry
through supported code. Authorization also checks the target resource; merely
adding authenticate to an ID route does not prevent cross-user updates/deletes.
CORS is a browser policy, not authentication. Configure trust proxy and rate-limit
identity for the actual trusted topology; defaults can group users or trust spoofed
headers. Apply security headers and secure cookies deliberately, redact credentials
and body logs, and manage graceful server/database shutdown. Use existing libraries
and module structure rather than mandatory style/RO-RO/interface preferences.

## Primary documentation

- [Async error forwarding and error middleware](https://expressjs.com/en/guide/error-handling.html).
- [Trusted proxy configuration](https://expressjs.com/en/guide/behind-proxies.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
