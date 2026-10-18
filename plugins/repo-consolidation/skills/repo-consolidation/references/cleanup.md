# Reconcile all cleanup candidates

After a PR merge, apply the [PR cleanup procedure](integration-cleanup.md) first.
Then account for original contributing sources not identical to that PR branch.
This wider pass does not expand deletion authority or permit discarding files.

For each candidate retain exact original/current tip or byte evidence, source
unit mapping, integrated/superseded destination proof, current owner/activity,
open PR/worktree use, authorization, and preservation status. Inspect new commits
added after the original inventory before deciding. A name resembling a merged
branch, a missing tracking ref, or patch equivalence alone is insufficient.

1. Verify every original and current-tip unit is integrated or deliberately
   superseded with evidence. Preserve excluded work, deliberate revert/product
   conflicts, uncertain equivalence, missing objects, and unclassified content.
2. Re-read advertised remote tip immediately before an authorized deletion.
   Prefer provider-supported expected-tip deletion. A read then delete has a
   race; preserve the branch if exclusive ownership or a safe condition cannot
   be established. Never delete default, destination, protected, shared, advanced,
   active-PR, or unrelated branches. Verify exact remote absence afterward.
3. Inspect every worktree for tracked/untracked/valuable ignored files, staging,
   unpushed/unmerged commits, ownership, locks, and active processes before
   eligible Git-aware removal. A clean status is not sufficient. Removal must
   already be authorized; new worktree creation is not included. Preserve
   inaccessible/locked/active registrations rather than force-removing them.
4. Ensure no worktree or active task uses a local branch and all current work is
   accounted for before deleting it. Squash/rebase cases require content/result
   evidence plus authority beyond ancestry checks, not a blind forced delete.
5. Prune only verified stale tracking/registration entries in affected scope
   after retention decisions. Do not run broad housekeeping or raw directory
   deletion. Keep primary checkout usable; fast-forward default only when safe,
   preserving divergence and other tasks' dirty bytes.
6. Re-enumerate live refs, worktrees, dirty state, and stashes. Record every action,
   already-absent result, preservation reason, residual coverage gap, and recovery
   path. Retain secured recovery copies and restore instructions through handoff;
   never auto-delete them because integration succeeded.

A failed cleanup leaves cleanup incomplete, not the merge undone. Continue
unaffected work and report the exact remaining item. Inventory/report/no-merge
restrictions never become cleanup permission through this reference.
