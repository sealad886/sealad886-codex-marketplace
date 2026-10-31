# Supabase backend boundaries: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Enable and test RLS on exposed tables; policies must cover the relevant SELECT/INSERT/UPDATE/DELETE behavior and required grants.

- Server secret/service-role access can bypass RLS depending on request auth context; never expose privileged keys in browsers or client-public environment variables.

- Authentication identifies a user; record ownership and tenant membership still require explicit policies and server authorization.

- Supabase client requests do not make arbitrary SQL/RPC implementation safe automatically; inspect dynamic SQL and SECURITY DEFINER functions.

- SSR session cookies must follow the current supported framework integration and verified claims/user checks; do not trust unverified client session data for privileged decisions.

- Storage needs bucket/object policies and validated upload paths/types/sizes; signed URLs are bearer access until expiry.

- Realtime subscriptions need cleanup, appropriate authorization, and reconnect/error handling; filters are not a replacement for access control.

- Use Edge Function secrets and explicit allowed origins/inputs; CORS does not authenticate a caller. Schema, policy, and cloud changes require corresponding authority.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Privileged secret/service-role requests can bypass RLS; keys must remain server-side.](https://supabase.com/docs/guides/database/postgres/row-level-security)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
