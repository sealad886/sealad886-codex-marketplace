# Lua Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Language semantics

- Lua sequences conventionally use positive integer indices from one, but tables can use other non-nil keys; avoid claiming every table is one-based.
- The length operator and ipairs have sequence/hole semantics; use explicit counts or key iteration for sparse data.
- __newindex is invoked for absent keys rather than all assignments, so it is not a complete validation hook for existing fields.

## Host and performance

- Standard Lua does not provide a universal table preallocation function; LuaJIT/engine extensions must be checked before use.
- Use pcall/xpcall at meaningful recovery boundaries and preserve useful failure context.
- Weak tables change garbage-collection reachability and cache behavior; choose key/value weakness deliberately.
- Profile local/global lookup and allocation changes in the actual host; do not assume desktop Lua performance applies to every game runtime.

## Primary documentation

- [Primary documentation](https://www.lua.org/manual/5.4/manual.html) — Lua table keys, sequence length, metatable behavior and protected calls are defined by the language manual.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
