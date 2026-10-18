---
name: repo-consolidation
description: Inventory a repository's branches, worktrees, stashes, and dirty work; account for changes absent from its verified default branch; finish authorized units through serial reviewed PRs and verified cleanup. Honor inventory-only, plan-only, no-push, no-merge, and exclusions.
---

# Repository Consolidation

## When to invoke

Use for scattered Git work, unfinished branches, worktree reconciliation, or
bringing outstanding work onto the verified default branch. Inventory/report
mode is read-only; plan mode adds a concrete integration/preservation plan.
Reading, quoting, authoring, installing, or automatically loading this skill
never invokes consolidation or grants mutation authority.

When the human explicitly requests execution on an identified repository, that
request authorizes task-scoped finishing, selective local commits, ordinary
pushes to its verified configured remote, PR creation/update, serial review,
gated merges, and deletion of eligible merged task branches. Restrictions and
controlling repository/tool policy narrow that authority. Do not repeatedly ask
for already authorized steps. New worktrees, data disposal, stashing/discarding
work, force pushes, rewriting existing history, settings changes, release,
publication, deployment, and unrelated repositories remain outside this grant.

## Inputs and evidence

Identify root/common Git directory, mode and exclusions, actual integration and
push remote, live default branch, pinned destination SHA, instructions, provider
capabilities/rules, existing PRs, owner/activity evidence, and environments.
Inspect status, all branches and worktrees, stashes, relevant ignored artifacts,
and active Git operations before editing. Preserve unrelated work.

Read [Git inventory](references/git-inventory.md). Keep the
[consolidation ledger](templates/consolidation-ledger.md) outside source
worktrees or in an established canonical project location, with secured recovery
copies where needed. This package contains its own
[selective commit](references/selective-commits.md) and
[serial review/integration](references/serial-review.md) procedures; no sibling
plugin or machine-specific cache path is required. Available installed tools may
assist without replacing the required evidence or authority checks.

## Workflow

1. **Capture all original sources before fetch or prune.** Inspect local refs,
   all registered worktrees including detached/locked/missing registrations,
   staged/unstaged/untracked work, relevant ignored artifacts, stashes, unique
   local-default commits, and nested/submodule boundaries. Query every configured
   remote's advertised heads; distinguish fork/upstream and push destinations.
   Resolve default from live provider metadata/symbolic HEAD and cross-check
   policy. Never assume `origin`, `main`, or that inaccessible means empty.
   Detect shallow/partial/sparse/bare/offline limits and API pagination gaps.
   Fetch relevant refs without pruning after preserving old tracking identities.
2. **Preserve and classify work.** Pin source/destination SHAs and preserve
   valuable dirty bytes before transfer/deletion. Git bundles do not preserve
   untracked, ignored, or uncommitted content. Keep secured recovery material
   outside distributed source and retain restore instructions. Compare ancestry,
   unique commits, patch equivalence, merges, actual file deltas, and intended
   behavior. Account for squash/cherry-pick/revert/supersession, binaries, LFS
   availability, gitlinks, and source aliases. A patch match alone is not retained
   behavior. Unknown ownership or inaccessible content remains visible.
3. **Map sources to reviewable work units.** Reconstruct intent from tests,
   source/docs, issues, PRs, and plans. Search canonical implementations before
   adding another. Finish in-scope partial work; do not adopt every repository
   TODO. Give each unit one disposition: include, already integrated,
   superseded, preserve/exclude, or blocked, with evidence and destination.
   A deliberate default-branch revert is a product decision, not permission to
   reintroduce it. Contradictory intent and uncertain ownership need direction;
   continue independent inspection while preserving those sources.
4. **Plan serial integration.** Group coherent outcomes into focused PRs; reuse
   matching existing PRs and preserve human context. Order dependencies, source
   SHAs/hunks, destination/base, authorized checkout, incorporation, completion
   tasks/conflicts, acceptance checks, reviewers, recovery, and cleanup candidates.
   Prefer refreshed default after each predecessor merges. Existing stacks need
   explicit base tracking and authorized retargeting. Reuse/merge/cherry-pick
   non-destructively; do not replay shared changes twice, blindly cherry-pick
   merge commits, or rewrite a source. Show the plan without an extra approval
   pause when execution is already authorized. Do not move unrelated dirty work
   by switching branches or create an unapproved worktree as a workaround.
5. **Finish one authorized unit at a time.** Recheck tips/status, incorporate in
   dependency order, and resolve conflicts from intended behavior rather than
   blanket ours/theirs. Record adaptations and omitted hunks. Finish required
   tests/docs/configuration and authorized migrations with backups. Use the
   project's environment, installed versions, and current primary documentation.
   Preserve excluded staging through the local commit procedure; never enable
   commit cleanup. Verify selected content and meaningful behavior before
   integration. Report completed/total units and PRs, active phase, failures,
   and blockers with at most one active checklist phase.
6. **Run three distinct coverage passes.** Before review, reconcile every source
   to units and every included unit to resulting changes. Before merge, verify
   the net change against current destination, behavior/contracts, tests/docs,
   migrations, and combined interactions. After each merge and at handoff,
   verify actual destination behavior/content and re-enumerate live refs,
   worktrees, dirty state, stashes, and remote tips. Add advanced/new items to
   the ledger. Counts or repeated rereading never substitute for these passes.
7. **Review and merge PRs in series.** Follow the complete local serial-review
   protocol: explicit sources/outcomes, up to ten rounds, pattern/scope analysis,
   deliberate clean-source retirement, attributable Copilot unavailability,
   separate final-head independent check, repository gates, conditional merge,
   actual merge readback, and eligible cleanup. Finish one PR's loop before
   starting another review loop. Refresh the destination/dependency plan and
   affected integration checks after each merge. A blocker stops its dependent
   chain; safe independent preparation may continue. Attach created/continued
   task PRs when the host supports attachments.
8. **Reconcile wider cleanup and retained work.** PR-source cleanup may leave
   original contributing branches. Use the [cleanup rules](references/cleanup.md)
   for each additional candidate, retaining source-to-result evidence. Delete
   only authorized, integrated/superseded, clean, unused task sources with
   current ownership and expected-tip evidence. Preserve advanced, shared,
   protected/default, ambiguous, valuable, or unaccounted sources. Retain
   recovery copies and excluded work. Do not reset divergent local default or
   repeat an already verified merge to resolve cleanup problems.

## Outputs and handoff

Report repository/remote/default identity, mode/exclusions, baseline/final SHAs,
source/unit totals and dispositions, serial PR links with review/merge evidence,
three coverage passes, checks, removals/readbacks, preserved dirty work/stashes,
recovery locations, and exact blockers. Keep original and current identities
after branch names disappear. State actions not performed and why; integration
does not establish release or deployment.

## Completion evidence

Every original and newly discovered source is reconciled; each included unit is
verified on destination; preservation is concrete; all three coverage passes
have evidence; and authorized eligible cleanup has readback. Unknown or blocked
sources prevent a claim of full consolidation. Inventory/plan modes complete
with honest coverage and next decisions. Say "merged; cleanup incomplete" when
integration succeeded but remaining cleanup is blocked.

## Must not

- Treat fewer refs as success, omit dirty/default/stashed sources, or prune away
  original identities before recording them.
- Assume ancestry, patch IDs, closed PRs, stale tracking refs, or clean tracked
  status alone prove integration or disposable directories.
- Discard files/stashes, run commit `--clean`, delete tags/arbitrary refs, create
  unauthorized worktrees, remove locked/active worktrees, or cross nested-repo
  boundaries without authority.
- Merge concurrent PR review loops, bypass required reviewers/checks/queues,
  silently broaden product intent, or force integration to meet a round limit.
- Upload recovery archives, secrets, private diffs, or local-only data as source.
- Release, deploy, publish packages, or change remote destinations/settings under
  repository-consolidation authority.
