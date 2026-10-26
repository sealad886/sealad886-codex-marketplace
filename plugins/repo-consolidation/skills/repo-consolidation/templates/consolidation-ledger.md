# Consolidation ledger

Keep canonical evidence outside source worktrees when needed. Redact credentials
and private contents. Stable IDs survive branch renaming/deletion.

## Scope and baseline

- Human request, mode/grants/restrictions/exclusions:
- Repository root/common Git directory, provider and tool versions:
- Verified integration/push remote, default evidence, baseline destination SHA:
- Baseline timestamp, remote/fetch/API pagination coverage and failures:
- Worktree owners/activity, shallow/sparse/partial/bare/offline limits:
- Secured recovery locations, retained bytes, and restore instructions:
- Restoration scope/scratch identity, content and representation comparisons,
  object/LFS/gitlink prerequisites, result and unresolved gaps:

## Source inventory

| Source | Kind/exact ref or path | Original SHA or dirty-byte evidence | Current identity | Owner/activity | Availability/freshness | Units | Disposition/preservation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S-01 | Local/advertised remote branch, worktree, detached, stash, index, working, untracked, relevant ignored, local-default delta | Immutable identity | Fresh recheck | Known/shared/unknown | Complete/stale/missing/blocked | U-* | Evidence and retained destination |

Retain equal-tip aliases; distinguish diverged local/upstream tips and staged/
unstaged bytes. Do not omit unavailable, dirty-default, or newly advanced sources.

## Outcomes and PRs

| Unit | Source IDs and exact commits/hunks | Accepted outcome and unfinished tasks | Disposition/reason | Dependency/PR | Canonical owner and result mapping | Acceptance/proof |
| --- | --- | --- | --- | --- | --- | --- |
| U-01 | Immutable source evidence | Required behavior and consumers | Retain/adapt-combine/replace; already integrated/superseded/preserve-exclude/blocked | P-* or preservation path | Surviving owner, adaptations/omissions and result files/commits | Command/revision/outcome |

For each included outcome record verified obsolete source/residue, exact removal
paths and reasons, caller/registration/generator/external-consumer checks, and
anything retained as required or blocked. Include affected flags, dependencies,
tests and docs; source removal belongs to the candidate, not only later ref cleanup.
Map an outcome even when its implementation is reconstructed and no source commit
is replayed. Source coverage is accounting, not a requirement to import every hunk.

Record shared content once with all contributing source IDs; give each consumer
its remaining intent. For prerequisite edges record the required contract,
evidence, satisfaction at the pinned destination, and serial order. Retain
conflicting intent and deliberate reverts as explicit decisions. Refresh these
mappings, bases and affected checks after each actual merge.

| PR | Current base/head | Units | Incorporation/conflicts | Checks | Review ledger | Actual merge/destination and cleanup |
| --- | --- | --- | --- | --- | --- | --- |
| P-01 URL | Exact revisions | U-* | Reuse/merge/cherry-pick/adaptation | Actual outcomes | One authoritative round ledger | Readback/eligible deletions/preserved |

## Three coverage passes

| Pass | Required question | Evidence | Gaps/disposition |
| --- | --- | --- | --- |
| Source, before review | Every source classified and included unit mapped? | Original sources, history/hunks, unit-to-result mapping | No unexplained omission |
| Behavior, before merge | Accepted outcomes, canonical ownership and source cleanup complete? | Current destination net diff, consumer/contracts/tests/docs/integration and residue checks | Failure/skipped reason or retained boundary |
| Destination, after merges and finally | Required outcomes present, verified obsolete residue absent, and valuable residual work preserved? | Merge readback, content/behavior, fresh refs/dirty/stashes/remote inventory | Advanced/new sources and remaining residue classified |

## Cleanup and resume

| Candidate (source file or ref/worktree) | Authority/expected tip or bytes/owner | Outcome/removal/valuable-file/active-use evidence | Action/time | Readback or preserved reason/recovery |
| --- | --- | --- | --- | --- |
| Exact identity | Fresh evidence | No unaccounted work | Eligible action only | Actual result |

Record completed/total units and serial PRs, one active phase, last head/base,
pending review/CI, conflicts/sequencer state, decisions, and next safe action.
Resume from live state without aborting another task's operation, resetting
work, repeating verified merges, or replaying deletions blindly.
