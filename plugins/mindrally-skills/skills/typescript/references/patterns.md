# TypeScript contracts and narrowing: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- TypeScript erases most types; annotations, interfaces, and casts do not validate untrusted JSON or prevent every runtime error.

- Use unknown for untrusted values and narrow through checks or an existing schema validator; any deliberately opts out of checking.

- Choose interfaces, type aliases, unions, enums, classes, and functions by semantics and project conventions rather than blanket prohibitions.

- Use discriminated unions and exhaustive handling for state variants; avoid optional fields that admit impossible combinations.

- readonly is a compile-time constraint and usually shallow; as const preserves literal/readonly inference but does not freeze runtime objects.

- Default parameters replace undefined, not null. Preserve intentional null/absence semantics rather than removing checks mechanically.

- Module/moduleResolution, emit, JSX, and library targets must match the runtime/bundler; strict mode upgrades need scoped fixes rather than suppressed errors.

- Function/class line counts, RORO, quote styles, and file naming are readability choices, not language correctness rules.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Control-flow checks narrow runtime values into usable static types.](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
