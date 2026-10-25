# Reconcile all cleanup candidates

Cleanup has two distinct parts: source simplification in the reviewed integration
candidate, and branch/worktree retirement after destination verification. Neither
expands the task's authority or permits discarding valuable content.

## Prune obsolete source with the outcome

For each reconciled outcome, identify source and artifacts that no longer serve
the accepted implementation. Remove verified obsolete tracked code, duplicate
implementations, snippets and abandoned artifacts within the authorized scope;
do not defer them merely because importing the new path already passes tests.

1. Record the candidate's exact paths, purpose, source outcome, surviving owner
   and removal reason. Age, names, apparent duplication or no text-search matches
   do not establish obsolescence. Inspect direct callers/imports, public exports,
   CLI/config dispatch, plugin registries, dynamic lookup, generator inputs and
   documented external consumers as relevant. Retain unresolved required boundaries
   and report the bounded gap rather than guessing them away.
2. Migrate required in-scope consumers to the surviving operation. Preserve
   meaningful differences in errors, timing, resource lifetime, cleanup and
   cancellation. Remove surrounding branches, forwarding wrappers and interfaces
   that existed only for the obsolete implementation; do not replace them with
   adapters or flags that reconstruct the competing designs.
3. Reconcile imports/re-exports, registrations, routes, feature flags, config,
   assets, dependencies and lockfiles, obsolete tests, comments, docs and sample
   snippets. Prove a dependency is unused across its owning package before removal.
   Update canonical generator inputs and regenerate through the declared workflow;
   inspect the resulting diff instead of deleting or editing output alone.
4. Run focused behavior/consumer checks and recheck the relevant entrypoints and
   residue. Protect required contracts rather than tests of removed internals.
   Verify the complete destination change; record any residue retained because it
   remains required or blocked. Use version history for source recovery, not
   commented-out copies, backup source trees or speculative compatibility layers.

This source-pruning scope does not include user data, operational artifacts,
unique dirty/untracked or valuable ignored content, stashes, recovery copies, or
unrelated files. Preserve those layers under the existing preservation procedure.
Tracked files may still be user data or operational material; tracking alone is
not permission to delete them. Expand an outcome's caller scope only when already
authorized or after obtaining the missing decision; avoid unrelated standardization.

## Retire integrated sources after verification

After a PR merge, apply the [PR cleanup procedure](integration-cleanup.md) first,
then account for original contributing sources not identical to that PR branch.

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
   A superseded unmerged branch remains unmerged: source-pruning authority and
   eligible merged-branch cleanup do not authorize its forced deletion. Obtain
   applicable explicit deletion authority or retain it with the verified reason.
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
