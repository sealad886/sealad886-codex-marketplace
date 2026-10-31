# Zod runtime validation: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use z.infer<typeof Schema> or explicit z.input/z.output types; inference is a TypeScript utility, not a schema .infer method.

- A JSON date normally arrives as a string, not a JavaScript Date. Choose validated ISO representation/coercion deliberately rather than z.date for every API payload.

- safeParse returns a discriminated result; async refinements/transforms require parseAsync/safeParseAsync.

- Zod 4 changes error customization/formatting and deprecates error.format; use current top-level formatting utilities supported by the installed version.

- Use refinements for business constraints and transforms for deliberate representation changes; preserve input/output typing after transformation.

- Choose strip/strict/loose unknown-key behavior explicitly and limit size/depth where untrusted input can exhaust resources.

- Zod schema reuse is useful, but do not claim generic schema precompilation without a documented supported compiler.

- partial update schemas do not authorize sensitive fields or guarantee at least one update; validate writable fields, patch semantics, and ownership separately.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Zod 4 changes APIs and deprecates instance error.format in favor of top-level formatting.](https://zod.dev/v4/changelog)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
