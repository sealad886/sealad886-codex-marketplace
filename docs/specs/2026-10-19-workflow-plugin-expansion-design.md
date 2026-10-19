# Workflow plugin expansion design

Date: 2026-10-19. Status: approved in chat for implementation, PR/merge, publication, private account updates and local refresh.

## Outcome and approach

Expand all six plugins with concrete advanced workflows, keeping one coherent
namespaced skill per plugin. Preserve local/cloud portability, identities,
existing starter prompts, authority boundaries, and independent installation.
New capabilities are delivered through short entrypoint routing, conditional
runbooks, worked procedures, and existing or optional templates. No server,
bundled executable, new runtime dependency, or mandatory sibling plugin is needed.

Three approaches considered:

1. Deepen the existing workflows with operational runbooks and verified examples
   (recommended). This adds capability with the smallest maintenance and access
   burden, while keeping simple requests fast.
2. Add read-only evidence-collection CLIs. This can automate recurring capture,
   but adds parsing, portability, dependency, security, and maintenance contracts
   before a demonstrated need for a new executable exists.
3. Split each plugin into more entrypoint skills. This increases explicit
   commands but overlaps existing plan/execute/review modes and complicates
   discovery without a necessary new responsibility boundary.

## Bounded feature set

### Iterating PR Bot Fixes

- CI triage tied to the failed run and SHA: distinguish product defects,
  provider/environment failures, baseline failures, and unproved transients;
  trace the first meaningful error and use bounded authorized reruns.
- Revision and merge-queue refresh: handle advanced heads, changed bases,
  synthetic merge-group checks, late review results, already-merged PRs, and
  cleanup recovery while preserving source retirement and final-head review.
- Add `references/ci-triage.md` and `references/revision-refresh.md`; extend the
  existing review ledger, not a parallel mandatory tracking artifact.

### Repository Consolidation

- Analyze overlap and dependencies among branches/PRs: integrate shared
  prerequisites once, retain independent changes, detect deliberately reverted
  behavior, and derive a serial integration order that refreshes after merges.
- Verify recovery content before source retirement: distinguish committed
  objects, dirty/index/untracked/ignored work, symlinks/modes, gitlinks and LFS
  gaps; inspect restoration in explicitly selected scratch space. Create no
  worktree or destructive recovery action by implication.
- Add `references/overlap-and-dependencies.md` and
  `references/preservation-and-restore.md`; extend the existing source ledger.

### Conventional Commit

- Choose type/scope/breaking/revert semantics from observable behavior and the
  repository's actual automation. Describe automation impact without assigning
  versions, releasing, or introducing a dependency on another plugin.
- Add a deliberately constrained mixed-hunk recipe: commit a verified subset of
  already-staged content through an alternate index while preserving real-index
  semantic entries and working bytes. Reject unmerged state, selected unstaged
  edits, ambiguous dependencies, concurrent changes, and unsafe hook effects.
- Add `references/message-decisions.md` and `references/partial-staging.md`;
  link from the existing staging guide and extend its optional commit plan.

### Simplify Code

- Simplify state and control flow using reachable-state/decision tables,
  derived-state checks, guard clauses, and explicit states where they reduce
  concepts. Preserve lazy evaluation, side-effect order, cancellation and cleanup.
- Migrate repeated callsites in verified cohorts: define matches/exclusions,
  preview representative cases, use an existing transform or justified task-local
  codemod, then check remaining consumers and idempotence. No mandatory AST tool.
- Add `references/state-and-control-flow.md`,
  `references/mechanical-migrations.md`, and optional
  `templates/refactor-evidence.md`.

### Adversarial Audit

- Design bounded failure/recovery experiments with an interruption point,
  durable-state expectation, oracle, disposable fixture, resource cap, cleanup
  owner and stop condition. Cover credible retries, duplicate/reordered delivery,
  cancellation, truncated inputs and restart without imposing stronger contracts.
- Choose differential or metamorphic verification when direct expected outputs
  are unavailable. Define the supported relation, normalization/tolerance and
  independent oracle provenance; disagreement alone does not prove a defect.
- Add `references/failure-experiments.md` and
  `references/oracles-and-properties.md`; extend the existing audit ledger.

### Web Research

- Compare decisions using hard constraints, comparable units/periods, cited
  evidence and sensitivity to unknown values or priorities. Use qualitative
  elimination/dominance when invented numerical scores would mislead.
- Refresh an existing brief claim by claim, rechecking decision-relevant
  sources and identifying confirmed, changed, withdrawn and unresolved claims.
  Do not imply automatic recurring monitoring or publication.
- Appraise quantitative claims: denominators, populations, units, baseline,
  uncertainty and absolute versus relative effects. Separate reported values
  from transparent calculations; do not pool incompatible evidence.
- Add `references/decision-comparisons.md`, `references/research-refresh.md`,
  `references/quantitative-evidence.md`, plus optional decision-matrix and
  claim-ledger templates.

## Integration boundaries

Each plugin updates its existing SKILL routing/description and README examples;
preserve names, identities, current prompt values/order, artwork, license and
unrelated metadata. Keep detail conditional and reuse existing ledgers. Package
new files within the owning skill. No implicit commit, push, merge, release,
worktree, production fault injection, external messages or data-disposal grant.

The new capabilities justify minor versions: 0.2.0 for each plugin. Synchronize
both manifests, displayed versions, root README and changelog. Validate each
package independently; do not change shared validators to pin prose or file
counts unless an intentional machine-readable package contract requires it.

## Acceptance and verification

- PR workflow: classify a provider failure without editing code; reject an old
  green check as current coverage; retain clean reviewer retirement after a push;
  resume failed cleanup without a second merge.
- Consolidation: integrate shared prerequisites once; retain deliberately
  reverted work as a product decision; reject a bundle-only backup when dirty
  content is missing; preserve sources with unavailable LFS content.
- Commit: verify the staged-subset recipe in disposable Git fixtures with
  selected and excluded staged hunks plus unstaged bytes, empty proposals,
  signing failure, and hook effects. Check HEAD/index/working bytes and commit
  contents through actual Git. Do not infer support for arbitrary reconciliation.
- Simplification: preserve cancellation/cleanup and lazy evaluation while
  reducing state; migrate proven static callers and retain/report dynamic cases.
- Audit: an interrupted import is a finding only against its accepted delivery
  contract; a historical oracle can be wrong; round trips are not ground truth.
- Research: retain missing price as unknown; avoid carrying an unavailable
  source forward as current; revalidate changed-version claims; express a 50%
  relative reduction from 2 per 1,000 as an absolute 1 per 1,000 reduction.

Run existing package/schema/link/distribution checks, native pre-install and
installed-skill discovery, exact archive and installed-content parity, and
independent scenario/authority review. Use behavioral Git fixtures for the new
command recipe; add no prose-pinning or superficial coverage tests.

## Proposed delivery

Conventional Commit 0.1.1 PR #50 merged at d7e9c6bc8c6ae77e3c80d2c4374ee77bb0d26de9;
its stable release and exact local refresh are verified. With design approval,
write the canonical spec and concise implementation plan,
implement bounded package slices, review, then deliver approved updates through
focused PRs and releases. Update the six existing private account plugins using
their current identities and guarded release IDs; do not recreate plugins.
Refresh local copies through supported marketplace installation and verify the
published snapshot and native discovery in isolation and in the user's setup.
Cloud eligibility is checked separately from actual cloud task execution.
