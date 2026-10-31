# Sanity content models and queries: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Register every referenced schema type in schema.types; defining a field or object file alone does not load it.

- Use defineType/defineField helpers where supported; validation rules guide Studio editors and must not be mistaken for a universal database write constraint.

- Keep preview selections and GROQ projections aligned with actual schema fields; source examples referenced mainImage/categories/seoTitle without defining them.

- Pass query values as parameters; use narrow projections and explicit ordering for predictable pagination.

- Pin a deliberate API date and perspective, and use generated types where supported; a handwritten generic cast does not validate remote data.

- Public project IDs and dataset names differ from secret read/write tokens. Never expose tokens with client-public environment prefixes.

- Choose CDN use according to published/draft freshness and preview needs rather than only NODE_ENV.

- Use image asset metadata and the supported image pipeline; keep portable-text rendering and allowed link schemes deliberate.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Schema types are explicitly registered and field validation rules are type-specific.](https://www.sanity.io/docs/studio/schema-types)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
