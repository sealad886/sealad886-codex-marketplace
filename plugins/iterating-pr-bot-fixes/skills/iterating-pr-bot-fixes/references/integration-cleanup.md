# Merge, readback, and eligible cleanup

Before each provider write, recheck repository, PR, base/head repository/ref/SHA,
human authority, and current state. Use supported authenticated tools or CLI/API
with explicit repository identity; do not trust the current directory alone.

## Integration gate

- All active sources have explicit outcomes; permitted Copilot absence is
  recorded separately from completed independent review.
- No actionable feedback remains unresolved, including late comments.
- Final independent coverage applies to the exact current head/base and net
  change; earlier retired-source results remain historical where appropriate.
- Required CI, human/provider approvals, branch protections, conflicts, and
  merge-queue rules are satisfied. Read actual provider state; do not substitute
  a generic green check or independent review for required approval.

Use the repository-supported merge method with an expected-head condition, such
as the installed CLI's `--match-head-commit` or a provider equivalent. Do not use
an administrator bypass. Reassess coverage/gates if head or relevant base state
changed. Do not enable auto-merge before the review/final-check gate. Queue
submission or accepted requests remain pending until merged-state readback.
In no-merge/review-only mode provide the requested handoff and stop there.

Read back merged state, destination, actual merged head, merge result/commit,
and destination content after fetching relevant refs. Closed PR, accepted API
request, missing source branch, or queue membership does not prove merge.
Squash/rebase merges need content/behavior/source mapping, not ancestry alone.

## Cleanup after verified merge

1. Capture fresh local status, worktrees, refs, advertised remote source/destination
   tips, and active task/PR ownership. Compare source to the actual merged head.
   Preserve commits added afterward, extra dirty/staged/untracked/valuable ignored
   files, shared branches, and uncertain equivalence.
2. For the exact remote PR source, establish exclusive task ownership and that
   its current tip equals the merged head. Use conditional deletion where
   available. A separate read then delete has a race; if safe ownership/expected
   tip cannot be enforced, preserve and report it. Never delete default,
   destination, protected, shared, unrelated, or advanced branches. An already
   deleted provider branch is a read-back "already complete" result.
3. Switch the task checkout to destination and fast-forward only when doing so
   preserves unrelated changes and local commits. Do not reset divergence or
   carry another task's dirty work across branches. A divergent local destination
   can remain preserved while remote integration is verified.
4. Remove only an authorized, clean, unused task worktree with no valuable
   ignored/untracked files or unmerged/unpushed work. Respect locks, owners, and
   repository cleanup policy. This procedure grants no new worktree creation.
   Keep primary checkout usable and use Git-aware removal, never raw directory
   deletion or unrelated registration pruning.
5. Delete only the merged local task branch when no worktree needs it and all
   current-tip work is accounted for. Squash/rebase cases may require deletion
   beyond ancestry-safe Git checks; perform it only when the existing human
   cleanup authority and evidence cover that exact action. Prune verified stale
   tracking refs only in affected scope; do not broaden cleanup to other branches.
6. Read back local/remote refs and worktree registrations. Record actual
   deletions, already-absent items, preserved items, and failures/reasons.

Keep durable review/merge evidence through handoff under controlling retention
policy. Remove disposable task-created debug debris, not source, recovery
copies, other tasks' artifacts, or required records. A cleanup failure leaves
cleanup incomplete; it does not undo the merge. Continue unaffected cleanup
and never repeat a verified merge to repair a cleanup receipt.

Primary reference: [GitHub CLI merge and expected-head option](https://cli.github.com/manual/gh_pr_merge).
