---
name: firebase-development
description: "Use when implementing Firebase Firestore, Authentication, Functions, Storage, offline state, or security rules."
---

# Firebase Development

## When to invoke

Use when implementing Firebase Firestore, Authentication, Functions, Storage, offline state, or security rules. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Firebase/client/Admin SDK versions, environment/project identity, database mode, rules/IAM, auth claims, queries, and emulator setup. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define user/resource ownership and document/query/storage authorization before data flow changes.
2. Implement supported client/server APIs, bounded indexed access, transactional invariants and explicit offline/retry semantics.
3. Test rules with authenticated/anonymous/wrong-owner fixtures and verify actual server IAM, functions and device/offline behavior separately.

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
