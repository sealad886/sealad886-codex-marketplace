---
name: julia
description: "Use when developing Julia multiple-dispatch APIs, type-stable numerical kernels, scientific code, or performance measurements."
---

# Julia Development

## When to invoke

Use for Julia modules and scientific or application code.

## Inputs and evidence

Inspect Julia version, Project/Manifest environment, dispatch signatures, array shapes/types, allocation profiles, and test conventions. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Design generic functions with clear dispatch and mutation ownership.
2. Implement kernels inside functions with concrete working values and deliberate allocation.
3. Profile inference, allocations, and dispatch before adding annotations or specialized arrays.
4. Test numerical/error contracts and benchmark representative warmed calls.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Project tests and numerical checks pass; performance claims include compilation-aware timing and allocation/inference evidence.

## Must not

Do not claim type annotations automatically fix instability or use dump as a general implementation of show. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
