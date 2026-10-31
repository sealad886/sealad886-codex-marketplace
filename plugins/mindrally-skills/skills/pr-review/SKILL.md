---
name: pr-review
description: "Use when reviewing a pull request or diff for correctness, security, regressions, tests, performance, or architecture."
---

# PR Review

## When to invoke

Use for reviewing a pull request or diff for correctness, security, regressions, tests, performance, or architecture.

## Inputs and evidence

Inspect repository instructions, exact base/head revisions, complete changed-file context, callers, relevant tests and requested review scope. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Identify intended behavior and select risk-based review emphasis from the request.
2. Trace changed contracts through callers and failure paths, checking primary APIs where uncertain.
3. Report only actionable defects with accurate file/line, trigger, impact, severity and evidence.
4. Return a bounded review outcome with tested/untested scope and remaining evidence gaps.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

All relevant changed behavior has an explicit disposition; findings are reproducible/cited and evidence gaps remain stated.

## Must not

Do not report style preferences as defects or approve/merge a PR merely because a review found no issue. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
