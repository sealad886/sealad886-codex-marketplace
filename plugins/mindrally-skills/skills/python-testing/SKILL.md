---
name: python-testing
description: "Use when designing Python tests, pytest fixtures/parametrization, mocks, integration checks, or property-based invariants."
---

# Python Testing

## When to invoke

Use for designing Python tests, pytest fixtures/parametrization, mocks, integration checks, or property-based invariants.

## Inputs and evidence

Inspect requirement/defect, public interfaces, Python/test-runner versions, existing fixtures, external dependencies and environment constraints. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Identify the observable requirement and smallest reliable test boundary.
2. Choose deterministic success, failure and boundary examples or meaningful properties.
3. Use fixtures/mocks only at owned boundaries and guarantee cleanup.
4. Run focused tests and relevant integration scope; assess assertion strength and remaining gaps.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Tests demonstrate the intended regression/invariant, pass reproducibly in the selected environment, and leave no owned resources behind.

## Must not

Do not add implementation-mirroring tests or count mocks/coverage as proof of integration behavior. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
