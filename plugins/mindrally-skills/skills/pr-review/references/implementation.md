# PR Review: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Finding discipline

- A general review should cover correctness and meaningful regressions across relevant concerns; do not silently narrow it to security or ask an unnecessary angle question.
- Prioritize by actual impact/likelihood and project requirements; architectural preferences, single-implementation interfaces and missing branch-count tests are not automatically defects.
- Verify the claimed trigger and surrounding behavior before recommending changes; distinguish new regressions from separable pre-existing issues.

## Review outcomes and authority

- Passing tests do not prove all requirements, but absent tests also do not prove a product defect; assess whether required behavior lacks meaningful evidence.
- Tie findings to the reviewed revision and provide concise evidence/rationale rather than unsupported safe-to-merge declarations.
- GitHub Comment, Approve and Request Changes are distinct external review actions; a textual verdict does not submit any of them.
- Read-only review does not authorize posting, approving, changing code, or merging; proceed only within the user’s requested action scope.

## Primary documentation

- [Primary documentation](https://docs.github.com/en/pull-requests/reference/pull-request-reviews) — GitHub review comments, approval and change requests are distinct review decisions with configured merge implications.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
