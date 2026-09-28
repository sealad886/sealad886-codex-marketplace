---
name: implementation-execution
description: Implement an approved delivery-plan slice safely in the existing repository. Use for features, fixes, refactors, infrastructure, configuration, migrations, or documentation changes that require edits and incremental verification.
license: MIT
---

# Implementation and Execution

Read `../.shared/operating-model.md` before editing.

## When to invoke

Use when Ready/Design gates are satisfied and the user has authorized changes. For incident/hotfix work, use the smallest safe hypothesis-driven fix and record any deferred lifecycle work.

## Inputs and evidence

Expect accepted scope/criteria/design and a ready work slice. Inspect applicable instructions, repository status, target modules and abstractions, tests, build/package tooling, lint/type/format conventions, dependency policy, Git history, CI parity, and canonical docs. Retrieve current authoritative docs before relying on external APIs.

## Workflow

1. Resolve repository root, instructions, branch/revision, dirty working tree, and exact write scope. Preserve and report unrelated changes; do not absorb or revert them.
2. Before executing a repository wrapper, lifecycle script, or unfamiliar build/test command, inspect the command and its delegated scripts or canonical documentation far enough to identify consequential side effects. Classify filesystem writes/deletes, fixed temporary paths, signing/notarization, credential access, network/provider calls, packaging, publication, deployment, and permission changes. Confirm authority for the actual consequences; generic build or test authority does not imply signing, publication, deployment, or destructive cleanup. Use a reviewed lower-effect path or stop when side effects exceed authority.
3. Find existing abstractions and canonical paths. Extend them before creating modules; resolve duplicates toward one canonical implementation incrementally. When one process is repeated, extract a well-named helper at the narrowest shared boundary and verify both shared behavior and caller-specific outcomes. Do not generalize incidental similarity or speculative future reuse.
4. Apply the shared simplicity test. Choose the smallest coherent patch that satisfies the work slice and maintains compatibility. Prefer a direct extension of the canonical path over new abstraction, dependency, configuration, or framework; add complexity only for a current requirement or demonstrated risk. Keep generated files, migrations, config, tests, and docs synchronized as required.
5. For bugs, reproduce and trace root cause before changing code. Form one falsifiable hypothesis at a time; add characterization/regression evidence when practical.
6. Use test-first development when it improves confidence; accept characterization, contract-first, invariant, snapshot, or post-change verification when domain/tooling makes strict red-green unsuitable. Never delete useful work solely to satisfy ceremony.
7. Implement in checkpoints. After each logical patch set, run the narrowest meaningful checks and update visible progress/RAID/status for multi-stage work.
8. Handle dependencies using the project’s lockfile/tooling. For Python, use project `.venv` or isolated compatible environment; never global install.
9. Follow current idioms and best practices for the repository's language, framework, and pinned versions, including error handling, types, resource ownership, concurrency, cancellation, and lifecycle behavior. Consult primary documentation when version-sensitive behavior matters.
10. Use Git safely: no destructive cleanup, hook bypass, history rewriting, merge/push/publish without authority. When commits are requested or repository instructions require them, inspect all changes, stage only owned scope, use Conventional Commits, and verify the index.
11. Hand completed code to `testing-quality`; do not self-certify release readiness.

## Outputs and handoff

Changed files/symbols, behavior summary, requirement/work IDs, checkpoint/commit references, checks run and results, unrelated changes preserved, deviations/decisions, and residual risks. Handoff to `testing-quality`, then documentation/review.

## Completion evidence

The approved slice is implemented in canonical paths; diffs are coherent; targeted checks ran; unrelated state is intact; no undocumented scope creep or unsafe operation occurred.

## Must not

- Implement unclear material requirements, build parallel abstractions, or silently widen scope.
- Add speculative flexibility, unsolicited cleanup, or adjacent improvements that are not required by the accepted slice.
- Turn an authorized bounded change into a rewrite without repository evidence and explicit authority for rewrite scope.
- Claim tests pass without running them, log secrets for debugging, or mutate global environments.
- Run an opaque wrapper whose signing, network, deletion, credential, packaging, or provider side effects have not been reconciled with authority.
- Merge, deploy, publish, delete, or rewrite history without explicit authority.
