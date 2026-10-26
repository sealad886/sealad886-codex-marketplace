# Inventory, selective staging, hooks, and readback

## Establish the actual repository

Inspect Git root/common directory, branch/upstream, worktrees, instructions,
remotes, current status, and merge/rebase/cherry-pick/sequencer state. Do not
finish another operation, switch branches, or invent identity under a simple
commit request. Read repository commit/signing/validation conventions.

```sh
git rev-parse --show-toplevel
git rev-parse --git-common-dir
git status --short --branch
git diff --cached --stat
git diff --cached
git diff --stat
git diff
git ls-files --others --exclude-standard -z
```

For programmatic inventory use NUL-delimited paths and literal pathspecs; never
split unusual filenames on whitespace or execute porcelain as shell. Inspect
untracked directories/file metadata before content. Keep sensitive diffs local
and secured. Detect binary/LFS/gitlink changes and unavailable content. An empty
tracked diff does not account for ignored or untracked work.

For every candidate, separately record index delta from HEAD and working delta
from index. A file can contain two owners' staged hunks, selected staged content,
and unrelated unstaged changes. Preserve excluded bytes and stage intent; an
index backup alone does not preserve untracked/working files. Do not make broad
secret-bearing backups in tracked source. Stop if concurrent writers change the
selected state while it is being classified.

## Choose a commit path

**Normal staged commit:** allowed when every entry in the index for that commit
belongs to the group. Inspect the whole cached diff and proposed tree; staging
selected paths does not remove existing unrelated staged changes. Do not use
`git add .` or `git commit -a` to save selection effort.

**Complete eligible files, unrelated files already staged:** path-only commit
can preserve other paths' staging:

```sh
git commit --only -m 'fix(component): restore the required behavior' -- SELECTED_PATH
```

This uses the working-tree content of each named path. It may include unstaged
edits in those files, so use it only when every selected file's entire delta
belongs. Inspect the selected diff from HEAD and a dry-run of the same command,
not only `git diff --cached`. Quote paths, use explicit argument boundaries, and
use literal pathspec handling for unusual names.

**Mixed eligible/excluded staged hunks:** conditionally use the
[verified staged-subset procedure](partial-staging.md). It builds the selected
candidate from original HEAD, requires independent already-staged text hunks
and audited hooks, and proves both patch orders reconstruct the original index
tree. It then leaves the real index untouched after HEAD advances; there is no
general reconciliation step. A copied full index alone still contains excluded
entries and cannot isolate the commit. Selected unstaged content, overlapping
hunks, unmerged state, ambiguous dependencies, unsafe hooks and concurrent
changes make this recipe inapplicable. Explain the smallest necessary staging
decision and continue independent groups rather than stashing, unstaging,
resetting or overwriting unrelated work.

Use `git add -p` or a precise equivalent only when supported noninteractively or
through an inspected interactive flow; never choose all hunks blindly. A changed
index can still be wrong: inspect selected tree/content and expected parent
before commit, then compare excluded index/working state afterward.

Choose the message from the resulting behavior, using
[message decisions](message-decisions.md) for type/scope, breaking consumers,
reverts and actual automation rules. Message choice neither assigns a version
nor authorizes the corresponding revert, release or production migration.

## Hooks, signing, and failure handling

Respect repository hooks and required signing. Inspect hook commands and execute
checks in the declared project environment; a hook can execute untrusted source,
contact providers, or modify files. A local commit request does not authorize
arbitrary external writes by hooks. Do not bypass with `--no-verify`, disable
signing, invent author details, or alter global config. Credential/signing-user
action may be necessary; report the exact failing boundary without exposing
key material.

Run appropriate checks before committing. If a hook reformats or generates
content, read fresh diffs and reclassify it rather than staging everything.
If the commit command fails, inspect HEAD, index, and worktree first. A post-commit
hook or transport layer can report failure after a commit exists. Avoid duplicate
retry commits; do not amend/rewrite to conceal a failure.

Read back new hash/parent, message, full diff, required signature, and remaining
status. Compare exclusions to the recorded baseline. Unexpected scope blocks
further mutation and needs a bounded recovery decision. Keep actual verification
results; a green command on different content is not proof of the commit.

Primary references: [git commit](https://git-scm.com/docs/git-commit),
[git add](https://git-scm.com/docs/git-add),
[Git hooks](https://git-scm.com/docs/githooks),
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
