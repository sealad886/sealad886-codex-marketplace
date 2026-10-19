# Refresh revisions and resume safely

Use after a push, changed base, queue rebuild, late review, interruption, or
cleanup failure. Keep the same [review ledger](../templates/review-ledger.md)
and round budget. Refreshing evidence grants no new implementation, provider
write, history rewrite, worktree, or cleanup authority.

## Reconcile live state first

Read PR identity, head repository/ref/SHA, destination/base SHA, open/closed/
merged state, merge result, queue state, checks, reviews and unresolved feedback.
Inspect local status/index, relevant refs and active owners before any local
write. Compare with the last ledger checkpoint. Record what changed and which
evidence it invalidates; preserve original IDs, outcomes and reviewed revisions.

| Change | Evidence to refresh |
| --- | --- |
| Head H1 becomes H2 | Inspect H1..H2 and the final net diff against the current base. Old CI and reviews remain attributed to H1. Pending active sources need H2 results; obtain sufficient independent final H2/base coverage. |
| Base B1 becomes B2 with head unchanged | Reassess the changed net diff, affected interactions, conflicts and integration proof. Refresh independent coverage where prior scope no longer suffices, and read provider approval/check requirements. Do not silently merge, rebase, or rewrite the task branch. |
| Test-merge or queue group changes | Preserve the old tested SHA and composition as history; obtain the required checks for the currently applicable candidate. Do not relabel synthetic-merge results as head-only checks or independent review. |
| Review arrives late | Retain its reviewed head/base and request attribution. Check every finding against current behavior, then record actionable, already addressed, duplicate, obsolete, or unrelated disposition with evidence. Late clean H1 feedback is not an H2 review. |

A changed head/base does not reset rounds, erase findings, or reactivate clean
reviewers. Copilot clean at H1 stays retired after H2; retain its historical
coverage and use a separate fresh independent context for H2's uncovered final
change. Copilot's attributable `explicit unavailable` disposition also persists
until human direction re-enables it, subject to explicit requirements. Follow
the existing [source rules](review-sources.md), including the distinct security
freshness rule. Never disguise re-requesting a retired provider as a final check.

## Keep integration candidates distinct

Record head/base, actual tested SHA, event and candidate mapping together.
GitHub can evaluate required checks on a test-merge commit; inspect the PR's
current merge requirements rather than selecting whichever SHA is green. Check
the expected provider as well as the check name. A skipped or neutral result
accepted by protection does not by itself prove the intended tests executed.

A merge queue tests a synthetic group containing the latest base and queued
changes. Its SHA differs from the PR head. Track the group's current membership
and required-check results. A rebuild, removal, changed order, or advanced base
can supersede prior group evidence. Required Actions checks need the supported
`merge_group` trigger; missing configuration is a concrete blocker, not a reason
to bypass the queue or change protection. Propose a scoped workflow repair only
under implementation authority. Queue checks supplement independent final-head
review; queue entry or successful checks alone do not prove the PR merged.

Before an authorized merge, re-read current revisions and all gates. Bind the
request to the expected head using supported provider capability, honor queue
rules, and verify actual merged state and destination content afterward. If
identity changed, return to refresh rather than retrying a stale write.

## Resume the remaining phase

- **Already merged:** confirm merged PR identity, actual result/destination and
  source mapping through [integration readback](integration-cleanup.md). Record
  merge complete. Continue only remaining authorized cleanup; do not submit a
  second merge, recreate the PR, or infer branch equivalence from disappearance.
- **Queued:** inspect the current group and pending gate, then wait or diagnose
  within scope. Do not repeatedly enqueue or bypass protection.
- **Closed without a verified merge:** preserve state and report the closure;
  reopening or changing destination requires applicable human authority.
- **Cleanup failed:** retain the merge receipt and exact failed action/error.
  Refresh branch tips, worktrees, valuable files and owners. An advanced/shared
  source is preserved; an already-absent target is a read-back completed action.
  Retry only eligible authorized cleanup and verify its result. A divergent
  local destination is not permission to reset it.

Example: merge readback succeeded, but local branch deletion failed because a
checkout still owns it. Report "merged; cleanup incomplete," preserve that
checkout, and resume ownership/eligibility inspection later. Never repeat merge
to repair cleanup. No worktree is created or removed merely by this example.

Provider details checked 2026-10-19; verify current host capabilities. Primary
references: [required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks),
[merge queues](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue),
[workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).
