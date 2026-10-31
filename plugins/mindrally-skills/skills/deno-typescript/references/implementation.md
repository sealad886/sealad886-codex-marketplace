# Deno TypeScript Development: implementation guidance

## Runtime and modules

Deno executes TypeScript by stripping types; execution alone does not prove type
correctness. Use deno check or the installed documented checking option. Configuration
is optional for trivial scripts but meaningful projects can require imports,
compiler settings, tasks and lockfiles. Prefer the project's pinned JSR/npm/import
map conventions over copying dated deno.land URLs or introducing deps.ts. Deno.serve
is the modern HTTP primitive where supported; Fresh API generations differ, so
confirm framework version before copying $fresh handlers.

## Permissions and resources

Scope allow-net/read/write/env to required targets. Subprocesses granted through
allow-run are separate programs and are not confined by the parent Deno sandbox;
review their authority explicitly. Do not prompt for broader permissions merely
to bypass a denied operation. Check Deno KV availability/stability and consistency
for the deployed version, handle null values and atomic/version checks, and close
handles. Validate request bodies, bound streams/timeouts and redact errors. Check
CLI help before bundle/compile tasks because availability and flags changed
between Deno releases. Compilation does not automatically prove target portability.

## Primary documentation

- [Execution versus type checking](https://docs.deno.com/runtime/fundamentals/typescript/).
- [Scoped permissions and subprocess trust](https://docs.deno.com/runtime/fundamentals/security/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
