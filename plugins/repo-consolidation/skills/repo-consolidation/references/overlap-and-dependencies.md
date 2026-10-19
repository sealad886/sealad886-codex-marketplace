# Overlap, prerequisites, and serial integration

Read when sources share commits, touch the same behavior, form a stack, or have
uncertain squash/cherry-pick/revert history. Use the existing consolidation
ledger; a branch is a source, not automatically one independent work unit.
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

For example, sources A and B both add a parser helper P; A adds an import caller
and B adds a preview caller. Map P once, then A's and B's caller changes to their
own units. After P merges, verify its actual interface before preparing each
caller on refreshed default. Keep both callers and their behavior checks. If P
was squashed and later deliberately reverted, stop the dependent chain for the
product decision instead of replaying P from either source.

Primary references: [merge-base](https://git-scm.com/docs/git-merge-base),
[range-diff](https://git-scm.com/docs/git-range-diff),
[revert](https://git-scm.com/docs/git-revert).
