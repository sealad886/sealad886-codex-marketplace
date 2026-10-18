# Local commits during a PR lifecycle

Use this procedure only within existing human task authority. It does not grant
commits, push, cleanup, or worktree creation by being loaded.

Inspect repository root, branch/upstream, worktrees, operations in progress,
cached/uncached diffs, untracked paths, and applicable hooks/signing rules.
Record all pre-existing staged entries and separate mixed staged/unstaged hunks.
Inspect intended changes for secrets and unrelated local configuration. Keep
private patches and recovery material secured outside distributed source.

Group complete behaviors with their relevant tests/docs/configuration. Stage
exact paths/hunks and verify the proposed tree, whitespace check, and meaningful
tests. Never use a plain commit while excluded staged entries remain in its
index; staging only your paths does not exclude somebody else's staged files.

When the complete working-tree contents of every selected path belong, a
path-only commit can preserve unrelated staged paths:

```sh
git commit --only -m 'fix(component): correct the scoped behavior' -- SELECTED_PATH
```

This takes selected working-tree contents, not just staged hunks. It is unsafe
for a selected file containing excluded staged or unstaged work. Use a verified
isolated-index method for mixed files only when the agent can inspect the exact
proposed tree, preserve excluded index entries and working bytes, and reconcile
the real index after the new HEAD. An alternate index does not automatically
preserve those semantics. Otherwise stop that group for the smallest necessary
staging decision; continue independent safe work. Never silently unstage, stash,
reset, or discard excluded content.

Respect hooks, configured author, and required signing. Inspect a hook before
running untrusted code; do not bypass checks, disable signing, or change global
configuration to hide a failure. Hook-driven file edits need fresh diff review.
After an apparent commit failure, read HEAD/status before retrying: a hook may
have changed content or a commit may exist already.

Messages follow `<type>[optional scope][!]: <imperative description>`. Use an
appropriate Conventional Commit type, no trailing period; keep behavior/tests
together. Explain a breaking change with `!` and a `BREAKING CHANGE:` footer.
Read back new hash/parent, message, full diff, signature where required, and
remaining index/worktree state. Unexpected content blocks subsequent push or
automatic recovery. Never amend/rewrite or enable excluded-change cleanup under
this procedure.

Primary references: [git commit](https://git-scm.com/docs/git-commit),
[git add](https://git-scm.com/docs/git-add),
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
