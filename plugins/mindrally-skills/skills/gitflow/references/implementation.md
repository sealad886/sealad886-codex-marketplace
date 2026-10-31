# Gitflow: implementation guidance

## Branch model

Classic Gitflow uses main for released history, develop for integration, feature
branches from/to develop, and release/hotfix paths that return relevant changes to
both long-lived branches. This is one workflow; do not introduce develop or Gitflow
into a repository merely because the skill was loaded. Follow documented prefixes,
merge strategies, approval counts and branch protections rather than invented
universal settings. A release branch stabilizes its intended scope, and a hotfix
must reach the active development/release line to avoid losing the fix.

## Version and operation boundaries

Inspect actual manifests, release tooling and public contract before selecting
SemVer. Conventional Commits and a patch label do not independently authorize or
prove a release. Fetch/read status before integration; do not blindly pull/rebase,
rewrite shared refs, stash/discard work or create worktrees. Resolve conflicts with
appropriate tests and verify each actual merged destination. Tags should identify
the exact validated release commit; creating/pushing tags and publishing require
explicit user authorization. Clean local/remote task branches only after fresh
ownership, unpushed-commit and reachability checks. Branch-protection settings are
external policy changes, not automatic setup steps.

## Primary documentation

- [Documented integration workflow concepts](https://git-scm.com/docs/gitworkflows).
- [Merge identity and history semantics](https://git-scm.com/docs/git-merge).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
