# Git Workflow Best Practices: implementation guidance

## Commits and branches

Stage only inspected in-scope files/hunks and inspect the full proposed commit.
Conventional Commits supports type(scope)! and BREAKING CHANGE footers; lowercase
whole-body text and a fixed 60-character subject are not specification requirements.
A feat/fix label influences release automation only when configured and within the
versioning policy; it does not itself publish or determine every SemVer impact.
Follow established branch naming rather than imposing feature/ prefixes or an
absolute never-commit-main rule over explicit repository/user policy.

## Synchronization and preservation

Fetch updates remote-tracking refs without integrating; pull also integrates.
Merge/rebase change history/state and must respect ownership and authority; do not
silently rebase shared/dirty branches or install global pull/prune aliases/settings.
Resolve real conflicts with test evidence and preserve unrelated changes. gitignore
does not untrack previously committed secrets; prevent exposure, then use approved
credential replacement and repository remediation when needed. Local branch -d
and remote deletion have different checks; verify integration/unpushed value and
permission before cleanup. Signing proves a signature under a key, not correctness
of content. Commits, push, PR, merge, tags and publication are separate actions.

## Primary documentation

- [Tracked files are not affected by ignore rules](https://git-scm.com/docs/gitignore).
- [Conventional Commit optional breaking markers and semantics](https://www.conventionalcommits.org/en/v1.0.0/).
- [Rebase/history behavior](https://git-scm.com/docs/git-rebase).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
