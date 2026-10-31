---
name: lua
description: "Use when developing Lua modules, tables, metatables, protected errors, memory-sensitive loops, or engine integration."
---

# Lua Development

## When to invoke

Use for developing Lua modules, tables, metatables, protected errors, memory-sensitive loops, or engine integration.

## Inputs and evidence

Inspect Lua versus LuaJIT/host version, available libraries, engine callbacks, table ownership, and error/lifetime contracts. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Implement cohesive modules using local ownership and explicit public interfaces.
2. Choose table/sequence and metatable behavior supported by the host.
3. Handle nil/errors and long-lived resources without masking failures.
4. Run host-appropriate tests and profile allocations/hot paths before tuning.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Module/host tests cover table boundaries, error propagation and resource lifetime; optimization claims have measurements.

## Must not

Do not use host-specific extensions without checking the configured Lua runtime. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
