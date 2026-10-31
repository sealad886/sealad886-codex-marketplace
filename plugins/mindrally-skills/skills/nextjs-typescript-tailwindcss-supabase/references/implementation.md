# Next.js TypeScript TailwindCSS Supabase: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Server and database boundaries

- Do not assume Next.js 14 is the latest release or automatically upgrade every package; lockfile and task constraints control.
- Use current @supabase/ssr browser/server factories when supported and handle cookie writes at valid response boundaries.
- Verify identity with the documented server method for the installed auth version; a client-readable cookie/session object alone is not authorization.
- Keep service-role/secret keys out of browser bundles and enforce RLS for ordinary client access.

## UI and integration

- Tailwind configuration differs across major versions; extend existing tokens/plugins rather than replacing the build.
- Server Components suit server data and secrets; client state/events still need client boundaries.
- Test loading/denial/expired-session states, hydration, redirects and ownership filters with at least two identities.
- Report unverified database policy/runtime evidence instead of describing code as bug-free or production-ready by instruction.

## Primary documentation

- [Primary documentation](https://supabase.com/docs/guides/auth/server-side/creating-a-client?queryGroups=framework&framework=nextjs) — Supabase SSR uses separate browser/server client setup and documented server identity/cookie handling.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
