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

## Source inventory

| Source | Kind/exact ref or path | Original SHA or dirty-byte evidence | Current identity | Owner/activity | Availability/freshness | Units | Disposition/preservation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S-01 | Local/advertised remote branch, worktree, detached, stash, index, working, untracked, relevant ignored, local-default delta | Immutable identity | Fresh recheck | Known/shared/unknown | Complete/stale/missing/blocked | U-* | Evidence and retained destination |

Retain equal-tip aliases; distinguish diverged local/upstream tips and staged/
unstaged bytes. Do not omit unavailable, dirty-default, or newly advanced sources.

## Units and PRs

| Unit | Source IDs and exact commits/hunks | Intended behavior and unfinished tasks | Disposition/reason | Dependency/PR | Result mapping | Acceptance/proof |
| --- | --- | --- | --- | --- | --- | --- |
| U-01 | Immutable source evidence | Concrete completion | Include/integrated/superseded/preserve-exclude/blocked | P-* or preservation path | Adaptations/omissions/result files/commits | Command/revision/outcome |

| PR | Current base/head | Units | Incorporation/conflicts | Checks | Review ledger | Actual merge/destination and cleanup |
| --- | --- | --- | --- | --- | --- | --- |
| P-01 URL | Exact revisions | U-* | Reuse/merge/cherry-pick/adaptation | Actual outcomes | One authoritative round ledger | Readback/eligible deletions/preserved |

## Three coverage passes

| Pass | Required question | Evidence | Gaps/disposition |
| --- | --- | --- | --- |
| Source, before review | Every source classified and included unit mapped? | Original sources, history/hunks, unit-to-result mapping | No unexplained omission |
| Behavior, before merge | Combined change meets accepted intent? | Current destination net diff, contracts/tests/docs/integration | Failure/skipped reason |
| Destination, after merges and finally | Included work present and residual work preserved? | Merge readback, content/behavior, fresh refs/dirty/stashes/remote inventory | Advanced/new sources classified |

## Cleanup and resume

| Candidate | Authority/expected tip/owner | Integration/valuable-file/active-use evidence | Action/time | Readback or preserved reason/recovery |
| --- | --- | --- | --- | --- |
| Exact identity | Fresh evidence | No unaccounted work | Eligible action only | Actual result |

Record completed/total units and serial PRs, one active phase, last head/base,
pending review/CI, conflicts/sequencer state, decisions, and next safe action.
Resume from live state without aborting another task's operation, resetting
work, repeating verified merges, or replaying deletions blindly.
