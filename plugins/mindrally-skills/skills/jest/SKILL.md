---
name: jest
description: "Use when writing Jest behavior tests, async assertions, mocks, spies, fake timers, or test isolation."
---

# Jest Testing Best Practices

## When to invoke

Use for JavaScript or TypeScript projects whose configured test runner is Jest.

## Inputs and evidence

Inspect Jest major version, ESM/CommonJS transform setup, environment, mock reset policy, timer mode, and the public behavior under test. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Identify the requirement/regression and choose the narrowest stable test boundary.
2. Arrange deterministic fixtures and mock only external or costly boundaries.
3. Await async work and restore spies, replaced properties, timers, and other owned effects.
4. Run focused tests and relevant suite checks; assess failures as behavior evidence.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Tests fail for the intended defect, pass for the corrected behavior, and remain isolated across order and repeated execution.

## Must not

Do not equate clearAllMocks with restoring original implementations or use snapshots to freeze incidental output. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
