# tRPC typed procedures: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Compile-time inference does not remove runtime validation, network errors, or server authorization. tRPC supports validators beyond Zod.

- V11 moved client data transformers to transport links; do not retain a v10 top-level transformer placement in a v11 client.

- Match server/client transformer behavior where non-JSON values are returned and test actual wire results.

- Create request/session context per request or supported batch semantics; shared database pools differ from shared user state.

- A protected procedure checks authentication, while object/tenant/admin authorization still requires explicit logic. Do not expose getById publicly unless the data is public.

- Select the current React/TanStack integration and Next Pages/App adapter for the project rather than imposing Pages Router layout.

- Bound batched work, URL sizes, payloads, and request cost; batching does not authorize unbounded procedures.

- Return deliberate public error shapes and redact internal exception details; TypeScript strictness and supported peer versions belong in the actual manifest constraints.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [V11 moves client transformers into links and documents current TypeScript requirements.](https://trpc.io/docs/migrate-from-v10-to-v11)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
