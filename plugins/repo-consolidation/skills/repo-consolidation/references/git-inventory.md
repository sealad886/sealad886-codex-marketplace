# Complete Git inventory and comparison

These examples inspect sources. Confirm installed Git/provider support, inspect
exit status and complete output, quote arguments, and use explicit remotes.
Use NUL-delimited output for automation; do not split paths on whitespace or
execute status/ref output as shell. Preserve secrets in secured local evidence.

## Local baseline before fetch

```sh
git --version
git rev-parse --show-toplevel
git rev-parse --git-common-dir
git status --porcelain=v2 --branch -z
git for-each-ref --format='%(refname) %(objectname) %(upstream) %(upstream:track)' refs/heads refs/remotes
git worktree list --porcelain -z
git stash list --format='%gd %H %gs'
git rev-parse --is-shallow-repository
git submodule status --recursive
```

Read remote configuration, distinct push URLs, positive/negative refspecs, and
provider identity without printing embedded credentials. A configured remote is
not automatically an authorized destination. Inspect relevant extra refs only
when evidence identifies work; tags are not cleanup candidates.

For every accessible registered checkout, inspect its exact HEAD, cached/working
diff separately, unmerged state, and untracked paths:

```sh
git -C CHECKOUT rev-parse HEAD
git -C CHECKOUT status --porcelain=v2 --branch -z
git -C CHECKOUT diff --cached --binary
git -C CHECKOUT diff --binary
git -C CHECKOUT ls-files --others --exclude-standard -z
```

Keep potentially sensitive patches in secured local evidence, not shared logs.
Inspect relevant ignored artifacts by metadata first; tracked cleanliness is
insufficient for disposal. Include primary/default checkout, detached tips,
locked/missing registrations, active operations/owners, and local-default-only
commits. Inspect stash index/working/untracked payloads read-only using installed
Git's supported options; do not pop/apply/drop merely to enumerate. Do not recurse
into nested repositories or mutate submodules without authority.

## Live remote sources

```sh
git ls-remote --symref REMOTE HEAD
git ls-remote --heads REMOTE
git symbolic-ref refs/remotes/REMOTE/HEAD
```

Cross-check actual default with provider metadata/policy. A stale or absent local
symbolic ref is not authoritative. A non-default branch called `master` may
contain work when `main` is default. An unavailable remote is a coverage gap,
not an empty source. Keep fork and upstream identities distinct.

Snapshot tracking tips before fetch/prune. Custom refspecs can omit advertised
heads. Fetch necessary missing refs non-destructively into an appropriate local
namespace; do not overwrite branches/recovery refs or force-update local work.
Record advertised/fetched SHAs and refresh moved sources. Deepen partial/shallow
history only as needed within authority/resource limits. Do not prune until old
identities and retention decisions are captured.

Use complete paginated provider queries for PRs, including draft/open/closed/
merged states, head repository/ref/SHA, base, merge result, reviews and active
requests. Git refs do not enumerate PRs. Record unavailable endpoints and limits;
do not call a truncated response a complete inventory.

## Compare immutable tips

```sh
git merge-base --is-ancestor SOURCE_SHA DESTINATION_SHA
git rev-list --left-right --count DESTINATION_SHA...SOURCE_SHA
git log --oneline DESTINATION_SHA..SOURCE_SHA
git log --merges --oneline DESTINATION_SHA..SOURCE_SHA
git cherry -v DESTINATION_SHA SOURCE_SHA
git diff --stat DESTINATION_SHA...SOURCE_SHA
git diff --binary DESTINATION_SHA...SOURCE_SHA
git diff --stat DESTINATION_SHA SOURCE_SHA
```

Ancestry status 1 means not ancestor; other failures need diagnosis. Three-dot
shows source changes from merge base; two-tip includes destination-only deltas.
Missing/multiple merge bases, unavailable objects, unrelated histories, sparse
content, LFS objects, binaries, renames/deletions, and gitlinks need explicit
coverage decisions rather than a guessed empty diff.

Patch equivalence is evidence, not integration proof. Merges need separate
inspection; a squash may combine many commits, and a previously matching patch
may have been reverted deliberately. Check destination files/behavior, PR merge
evidence, source-to-result mapping, and relevant acceptance. Use range comparison
where helpful for adapted series, without claiming it proves binary/content
completeness. Preserve aliases of equal tips while keeping divergence distinct.

Primary references: [worktree](https://git-scm.com/docs/git-worktree),
[ls-remote](https://git-scm.com/docs/git-ls-remote),
[cherry](https://git-scm.com/docs/git-cherry),
[diff](https://git-scm.com/docs/git-diff).
