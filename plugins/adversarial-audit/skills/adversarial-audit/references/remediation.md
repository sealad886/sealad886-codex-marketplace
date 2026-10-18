# Authorized remediation

Use only after task authority includes implementation. Assessment findings are
recommendations until accepted within the authorized scope.

1. Select the highest-value coherent finding cluster. Identify the invariant,
   root cause, canonical owner, affected callers, intended behavior, and proof.
2. Reproduce or establish a baseline when practical. If reproduction cannot run,
   retain source evidence and the specific runtime uncertainty.
3. Choose the smallest sufficient repair. A broader corrective simplification
   can be appropriate when authorized and bounded patches would retain the cause.
   Do not create a new abstraction merely to silence one reported line.
4. Protect meaningful behavior with existing checks; add a regression test when
   it proves the defect or a required invariant. Do not test incidental internals
   or duplicate prose. Keep performance and accuracy proof together where required.
5. Update all in-scope callers, configuration, dependencies, and docs affected by
   the repair. Delete code made obsolete by the change after checking references.
6. Run targeted checks and inspect real output. Review the complete diff for
   contract drift, unrelated edits, and new failure paths. Obtain independent
   review for material changes when available; preserve reviewed revision/scope.
7. Re-run the relevant audit slice. Update the ledger with patch/commit identity,
   proof result, remaining risk, and new findings before selecting the next unit.

For an unexpected failure, return to cause investigation. Do not stack speculative
fixes. A pre-existing or environmental failure should be attributed accurately;
it still limits any claim dependent on that check.

## A remediation unit

- Finding IDs and invariant.
- Root cause and repair boundary, including relevant sibling paths.
- Owned files and required caller/configuration/documentation changes.
- Acceptance criteria and exact proof command with expected result.
- Dependencies, resource budget, and recovery/rollback trigger.
- Fresh result, review coverage, disposition, and residual uncertainty.

Rollback planning does not authorize destructive Git operations, production
changes, or deleting user data. Follow the request and repository policy.

## Stop and report precisely

- `fixed`: correction identified and fresh verification supports it for this scope.
- `deferred`: outside this implementation slice or consciously postponed; record why.
- `accepted residual risk`: concrete risk accepted by the user or within explicitly
  delegated tradeoff authority; retain its conditions and consequence.
- `blocked`: exact dependency, permission, access, or decision prevents progress;
  give the smallest next action. Continue unrelated safe work where possible.
- `open`: still requires implementation or a decision; do not call it complete.

A severity threshold or time budget helps prioritize and bound the audit. It does
not silently authorize accepting unresolved risks or claim they were repaired.
