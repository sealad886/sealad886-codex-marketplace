# Overlap, prerequisites, and serial integration

Use when choosing how each source's useful outcomes should survive on current
default, including shared commits, competing implementations, stacks and uncertain
squash/cherry-pick/revert history. Use the existing consolidation ledger; a branch
is a source, not automatically one independent work unit or a replay instruction.
This analysis grants no merge, history rewrite, retargeting, or product decision.

## Compare content and intent

Pin source tips and the current destination first. For each candidate pair,
inspect shared ancestors, unique commits, merge parents, aggregate changes from
the appropriate base, and the current destination's files and tests. Use the
[inventory commands](git-inventory.md); where useful, compare known series with
`git range-diff OLD_BASE..OLD_TIP NEW_BASE..NEW_TIP`. Inspect its actual output:
range-diff is a human comparison aid, not a stable machine-readable mapping or
proof that behavior, binaries, merge resolutions, or every change is retained.

Classify each overlap with exact source commits/hunks and current evidence:

| Relationship | Integration decision |
| --- | --- |
| Same ancestor/prerequisite shared by two sources | Give the shared change one unit and one destination mapping; dependent units contain their remaining intent. |
| Cherry-picked or squash-equivalent content | Match aggregate deltas and accepted behavior; different hashes alone do not justify replay. Account for adaptations and omissions. |
| Independent changes in the same file | Preserve both outcomes and their checks; textual proximity is not a dependency. |
| Consumer requires another unit's API, schema, configuration, or data | Record a directed prerequisite and the observable contract, including necessary migration ordering. |
| Conflicting implementations or incompatible product intent | Preserve both sources and surface the exact choice; a clean merge cannot decide product intent. |
| Earlier matching change deliberately reverted or superseded | Inspect the revert's rationale and current accepted behavior. Keep a product decision open; do not classify it as integrated or silently restore it. |
| Missing history/content or ambiguous equivalence | Keep the comparison blocked/unknown and retain the source. |

A shared commit may contain unrelated work: split the mapping by verified hunks
or behavior, not just commit ancestry. A destination descendant can also have
removed its ancestor's behavior. Patch IDs, PR state, and merge-base evidence
help find candidates; current content, history and acceptance establish what
survives. Do not treat an intentional revert as a conflict to resolve away.

## Choose the destination implementation

1. State the accepted outcome and its required inputs, outputs, errors, side
   effects, ordering, resource ownership and cancellation behavior as relevant.
   Compare that contract with current default and each source, including tests,
   consumers, configuration and docs. Recency, ancestry and a clean merge do not
   decide which behavior belongs in the product.
2. Prefer an existing suitable canonical owner. For an included outcome, choose
   retain, adapt/combine or replace; otherwise explain already-covered,
   superseded, preserved/excluded or blocked work. Record the source-to-result
   mapping even when no original commit or helper is copied. Reconstruct a
   useful fix against current APIs when that gives a smaller complete change
   than replaying its stale implementation.
3. Reconcile equivalent rules through their in-scope callers. Check actual
   semantics rather than syntax; preserve required caller policy and necessary
   public, dynamic, resource and cancellation boundaries. Do not add forwarding
   layers, mode flags or compatibility shims merely to keep competing designs.
   If accepted requirements do not resolve a material conflict, retain the
   evidence and ask for that decision while independent work continues.
4. Prepare one coherent candidate containing the missing behavior, its consumer
   changes, and [verified obsolete-source removals](cleanup.md). Inspect the net
   diff against pinned default before choosing merge/cherry-pick as transport.
   A branch containing one useful fix, an obsolete wrapper and stale config is
   not three obligations to import; adapt the fix and omit or remove the residue.
5. Verify both the accepted outcome and the surviving call path. Keep source
   omissions and removals explicit. Do not claim reconciliation when an equivalent
   old implementation remains active without a required/blocked reason.

## Derive and refresh the order

1. Assign stable unit IDs and record prerequisite edges with reasons. Separate
   shared content from each consumer's remaining changes. Include tests/docs,
   configuration and migrations belonging to the contract.
2. Order prerequisites before consumers. A cycle usually needs one coherent
   unit or an explicit design decision; do not force an arbitrary order or add
   compatibility layers without a demonstrated need. A blocked prerequisite
   blocks its dependents; independent inspection/preparation can continue.
3. Integrate one focused PR through the existing serial review protocol. Do not
   preemptively rewrite sibling branches or run concurrent review loops.
4. After actual merge readback, pin the new destination. Recompare all affected
   remaining units, remove only proven covered content from their proposed
   changes, and update prerequisite satisfaction, PR bases, adaptations, and
   acceptance checks. Changes to head/base require the existing review gates.
5. Repeat the three coverage passes at their normal boundaries. Final proof
   checks the combined consumers, not merely that each PR merged separately.

For example, sources A and B add equivalent parser helpers plus import and preview
callers. If default already has a suitable parser, adapt both useful callers to
that owner and omit the duplicate helpers; map all source intent to those results.
Otherwise establish one suitable owner once, then prepare the callers against its
verified interface on refreshed default. Keep both callers' required behavior
checks. If the parser was deliberately reverted, resolve the product decision
instead of replaying it from either source. Similar-looking parsers with different
required error or cancellation semantics must not be unified blindly.

Primary references: [merge-base](https://git-scm.com/docs/git-merge-base),
[range-diff](https://git-scm.com/docs/git-range-diff),
[revert](https://git-scm.com/docs/git-revert).
