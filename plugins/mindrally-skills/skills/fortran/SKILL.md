---
name: fortran
description: "Use when implementing or reviewing modern Fortran modules, numerical procedures, kinds, arrays, C interfaces, or builds."
---

# Modern Fortran Development

## When to invoke

Use when implementing or reviewing modern Fortran modules, numerical procedures, kinds, arrays, C interfaces, or builds. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect compiler/standard/flags, numeric accuracy/units, array shape/lifetime, interoperability ABI, and existing build/tests. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define numerical preconditions, kinds, units, shape contracts and supported compiler standards.
2. Implement module procedures with explicit interfaces, allocation/intent/error semantics, and stable numerical algorithms.
3. Compile with relevant warnings/runtime checks and compare numerical/boundary results using justified absolute/relative tolerances.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
