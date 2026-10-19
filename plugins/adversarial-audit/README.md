# Adversarial Audit

Version: **0.2.0**. One self-contained skill for finding consequential correctness,
performance, resource, testing, contract, and operational defects with evidence.

[The adversarial-audit skill](skills/adversarial-audit/SKILL.md) distinguishes an
assessment from authorized remediation. An audit can finish with confirmed open
findings. An audit-and-fix task carries accepted changes through review and fresh
verification. Findings track validity separately from implementation status.

## Use

Install from the marketplace:

```bash
codex plugin add adversarial-audit@sealad886-codex-marketplace
```

Example requests:

- "$adversarial-audit:adversarial-audit Audit this repository's import pipeline
  for correctness and memory risks; report findings without changing source."
- "$adversarial-audit:adversarial-audit Design and run bounded interruption and
  retry checks on disposable import data against its documented at-least-once
  delivery contract; report recovery evidence without editing source."
- "$adversarial-audit:adversarial-audit Assess this converter using an independent
  reference and justified metamorphic properties. Define comparison tolerances
  first and investigate disagreements before calling them defects."
- "$adversarial-audit:adversarial-audit Audit and fix the accepted in-scope retry
  and recovery defects, and verify corrected behavior with representative inputs."

Provide the target, important contracts, environment, allowed checks, and whether
implementation is included. The skill uses available repository/host search,
tests, profiling, browsing, and delegation. It bundles no server and requires no
particular indexer, review vendor, sibling plugin, Python environment, or agent type.

## Evidence and safety

The [audit method](skills/adversarial-audit/references/audit-method.md),
[remediation reference](skills/adversarial-audit/references/remediation.md), and
[ledger template](skills/adversarial-audit/templates/audit-ledger.md) keep scope,
proof, changes, and unresolved work together. Missing runtime or provider access
is a coverage limit, not a clean result. Audit invocation does not authorize
commits, worktrees, external publication, deployment, or deleting user data.

Use [failure experiments](skills/adversarial-audit/references/failure-experiments.md)
for credible duplicate/reordered delivery, ambiguous retry, partial checkpoint,
cancellation, truncated input, and restart paths. Each check has an accepted
contract, disposable fixture, resource cap, cleanup owner, and stop condition.
[Oracles and properties](skills/adversarial-audit/references/oracles-and-properties.md)
cover independent references, accepted historical checks, round trips, and
justified conservation, order, monotonicity, or bounded-error relations. A
round trip supports consistency; it does not establish ground truth.

See [security and authority boundaries](SECURITY.md). This instruction package
guides the host agent; it does not add a sandbox, scanner, or tool permissions.

## Package validation

The release includes a portable Agent Plugins 1.0 manifest and synchronized Codex
manifest, original SVG artwork, one skill, and contained support files. Maintainers
run source/skill checks and distribution closure validation, then verify native
discovery and installed parity separately. Follow the repository's current
[contribution and validation guide](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/CONTRIBUTING.md).
Static package validation does not demonstrate audit quality or runtime safety.
