# Clerk Authentication: implementation guidance

## SDK and server boundaries

Use the installed Clerk SDK's asynchronous auth and protection APIs. Middleware
sets up authentication but does not automatically protect every route; verify
configured matchers and the Next.js middleware/proxy convention. Client hooks and
SignedIn-style UI do not enforce server access. Validate FormData/JSON at runtime;
TypeScript casts in the upstream server action do not validate input. Keep secret
keys server-side and distinguish them from publishable keys.

## Claims, external tokens, and caching

Custom session claims must actually be configured and typed; metadata is not a
guaranteed default claim path. JWT templates for external audiences are separate
from customizing the session token. Verify token audience/authorized parties and
provider configuration at external APIs. Enforce current organization membership,
permissions, and object ownership server-side; a role-string sample is not the
whole policy. Do not return private user data through a cross-user cache. Handle
null getToken results, upstream HTTP failures, and loaded/signed-in UI states.
Use supported redirect settings and keep Next redirect control-flow exceptions
outside broad catch blocks. Optional tooling provides no Clerk tenant permission.

## Primary documentation

- [Current async auth/protect contract](https://clerk.com/docs/reference/nextjs/app-router/auth).
- [Session token version and claims](https://clerk.com/docs/guides/sessions/session-tokens).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
