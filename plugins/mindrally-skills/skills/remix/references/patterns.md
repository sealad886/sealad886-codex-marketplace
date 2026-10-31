# Remix full-stack routes: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Remix v2 documentation and packages differ from React Router framework mode and later Remix generations; do not mix imports or migrate implicitly.

- Use configured route filename conventions; the sample nested folder structure does not itself guarantee v2 URL nesting.

- Loaders must protect returned data; actions validate form fields, permissions, and CSRF requirements at the server boundary.

- Cookie session storage requires reading the request Cookie header with getSession, updating state, and returning commitSession through Set-Cookie. A getSession() call without the request does not resume a session.

- Validate redirectTo against allowed local destinations and configure secure, HttpOnly, SameSite cookies and managed secrets.

- Use Form for document navigation fallback; client fetchers and hooks need JavaScript and require their own failure/pending UI.

- Use isRouteErrorResponse for thrown route HTTP failures and avoid exposing raw internal errors.

- Streaming/defer behavior depends on the installed generation and adapter; verify it before adopting an older example.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Remix v2 has generation-specific routes and migration conventions.](https://v2.remix.run/docs/start/v2/)
- [Session storage reads request cookies and commits Set-Cookie responses.](https://v2.remix.run/docs/utils/sessions/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
