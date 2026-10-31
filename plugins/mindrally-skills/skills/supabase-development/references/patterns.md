# Supabase application integration: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use the supported @supabase/ssr approach for current SSR integrations; old framework auth-helpers examples require deliberate migration.

- Do not mix old helper and new SSR clients within one session flow without documented migration behavior.

- Middleware/hook redirects improve UX but do not replace server data authorization and RLS.

- Use migrations for tables, constraints, indexes, grants, and policies; avoid a blanket rule that every database interaction must use supabase-js.

- Update policies may require SELECT visibility plus USING/WITH CHECK constraints; test insertion/update ownership separately.

- Separate public configuration from privileged secret keys; test with actual anon/authenticated roles rather than validating only as an administrator.

- Realtime presence and database changes are different channel features; authorize and clean up each subscription.

- Connection pool mode, caching, and pagination must match transaction/session and data freshness requirements.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Supabase documents migration from auth helpers to the SSR package.](https://supabase.com/docs/guides/auth/server-side/migrating-to-ssr-from-auth-helpers)
- [RLS behavior depends on operation, role, and request authorization.](https://supabase.com/docs/guides/database/postgres/row-level-security)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
