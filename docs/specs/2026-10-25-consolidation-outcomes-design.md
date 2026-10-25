# Repository Consolidation: reconcile outcomes and prune obsolete source

Status: proposed for user approval. Implementation and publication are not yet complete.

## Goal and scope

Make the verified default branch contain the useful, accepted outcomes of
disparate implemented work in one coherent repository. A branch and its commits
are evidence of intent, not a list of changes that must all be replayed. As each
outcome is reconciled, remove verified obsolete source and its residue so the
destination does not accumulate duplicate implementations or abandoned artifacts.

This changes only Repository Consolidation and its marketplace documentation.
Reading or authoring the plugin does not execute consolidation on this repository.
The user has authorized publication and verification of the marketplace default.

## Approaches and decision

1. Add a short warning against blind replay. Smallest edit, but leaves source
   pruning and canonical ownership detached from the main workflow.
2. Rework the existing outcome mapping, overlap guide, cleanup guide and ledger
   together. Recommended: make reconciliation and simplification explicit in
   each work unit without introducing another process or package dependency.
3. Require the Simplify Code plugin or combine both packages. Adds coupling and
   overlapping invocation rules without improving this standalone workflow.

Use approach 2. Adapt Simplify Code's principles into the existing skill;
Simplify Code itself remains unchanged. Keep one namespaced skill, its identity,
local/cloud eligibility, existing review gates and self-contained references.

## Workflow changes

- Establish accepted destination behavior from the human request and repository
  evidence. Map sources to capabilities and fixes, including their consumers,
  tests, documentation, configuration and dependencies.
- Compare each outcome with current default. Explicitly retain, adapt/combine,
  replace, omit as already covered or superseded, preserve/exclude, or block it.
  Preserve exact source-to-result evidence and reasons for omitted implementation.
- Choose the canonical surviving implementation by required semantics and clear
  ownership. Reuse an existing owner when suitable. Carry over only missing
  useful behavior; reconstruct it against current APIs when safer and simpler
  than replaying stale commits. Merge/cherry-pick only after reviewing the net
  change. Neither newest tip, commit count nor clean merge decides product intent.
- Keep meaningful caller-specific policy and necessary public, dynamic, resource
  or cancellation boundaries. Avoid speculative compatibility shims and generic
  wrappers that simply preserve competing implementations.
- In the same coherent candidate, migrate in-scope callers and delete obsolete
  tracked code, snippets, duplicate source, abandoned artifacts and associated
  imports, exports, registrations, generators, config/flags, assets, dependencies,
  tests and docs when evidence establishes they are unnecessary. Use the owning
  manifest/lockfile/generator workflow. Do not leave commented copies or backup
  source trees in the distributed repository.
- Inspect public/dynamic/external consumers and generated inputs before deletion;
  zero text matches, age or a branch name is insufficient. Preserve uncertainty
  and resolve only material intent choices. Do not turn this into unrelated
  repository-wide cosmetic refactoring.
- Retire eligible branches and worktrees only after destination verification and
  under existing ownership, tip, activity and authorization checks. A superseded
  unmerged branch is not automatically a merged branch or permission to force
  delete. Never discard unique dirty/untracked content, stashes, user data,
  operational artifacts or recovery copies under source-pruning authority.
- Refresh comparisons after each serial PR. Completion proves accepted outcomes
  and required callers work on actual default, obsolete source has been removed
  where verified and authorized, and all remaining sources/remnants are accounted
  for. Neither replaying every commit nor deleting every branch is a target.

## Package and release

Advance Repository Consolidation from the published 0.2.0 baseline to 0.3.0 for
the expanded reconciliation and source-pruning workflow. Synchronize portable
and Codex manifests, skill/plugin prompts, package guide, root README and
changelog. Reuse the existing guides and ledger; no new runtime, dependency,
executable cleanup tool, secondary ledger or sibling-plugin requirement.

Retain the catalog-local `./plugins/repo-consolidation` source. In a Git-backed
marketplace this resolves to the downloaded marketplace checkout, preserving
native pre-install details and making the package on main the default. Publish
through a focused reviewed PR, a signed immutable plugin tag on the validated
merge, its archive release, and the existing automatic marketplace snapshot.
Verify the resulting GitHub Latest snapshot and an unpinned fresh marketplace
registration/install; do not infer default installation from the tag alone.
Refresh the existing local marketplace installation after publication.

## Acceptance and verification

Review these scenarios against the written workflow:

1. Two branches contain equivalent helpers plus distinct useful callers. Keep
   one suitable owner and both required outcomes; omit duplicate implementation.
2. A branch mixes a useful fix, an obsolete wrapper, a stale config key and an
   abandoned generated artifact. Adapt the fix to current default; prune proven
   obsolete source/residue instead of replaying the entire branch.
3. An ancestor was merged and later deliberately reverted. Inspect accepted
   intent and current behavior; never silently resurrect it to close a ledger.
4. A nominally unused API is invoked through a registry or external consumer.
   Inspect that contract before deletion; preserve an unresolved necessary boundary.
5. A superseded branch has unique dirty/untracked files or an active owner.
   Account for and preserve that content; successful integration is not disposal
   permission. Source deletion and branch/worktree retirement stay distinct.
6. A merge removes one implementation but leaves its flags, dependency, caller,
   tests or docs. Cleanup remains incomplete until these are reconciled or an
   explicit required/blocked reason is recorded.
7. Each serial merge changes default. Recompare remaining outcomes against its
   actual behavior; retain newly discovered useful work without duplicate replay.

Run canonical source/distribution, dual-manifest, contained-link and marketplace
checks plus the pinned upstream validator and changed-skill validation. Obtain
independent quality/authority review. Use hosted regression/scanner checks on
the exact PR and published commit. Do not add brittle tests of prose wording.
Fresh native installation must expose one namespaced skill, complete metadata
before installation, version 0.3.0 and exact package parity. Verify archive digest,
tag target, publication workflows and the normal local refresh separately.
Instruction review and packaging checks do not prove behavior on every real
repository or an independently launched cloud task.
