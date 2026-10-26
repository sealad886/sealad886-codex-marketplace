# Serial PR review and integration protocol

This procedure is complete within this package. Optional installed review tools
may assist, but no sibling skill is needed. Human consolidation execution
authority, restrictions, repository policy, and tool decisions control every
action. Read-only/inventory/plan modes do not create PRs, comments, or issues.

Only one PR review loop runs at a time. Finish it through actual merge readback
and eligible task cleanup before starting the next. Refresh default, planned
bases, dependencies, and affected integration checks. Preserve human context
when continuing an existing PR; avoid duplicates and unrelated assignments.

Read the [source runbook](review-sources.md),
[pattern procedure](pattern-analysis.md), and
[integration runbook](integration-cleanup.md). Use one
[review ledger](../templates/review-ledger.md) per PR and link it from the
consolidation ledger rather than maintaining contradictory counters.

## Prepare and select sources

Verify repository/remote, PR head repository/ref/SHA, destination/base, intended
behavior, requested limits, checks, and required approvals/queue. Bring the PR's
title/body/required metadata current, preserving human-authored context. Make
ready when review can start. Do not enable auto-merge before the review gate or
alter settings, owners, or destination without authority.

Select independent Codex review and configured GitHub reviewers according to
human/repository requirements. Do not introduce an external CLI review service
automatically. Preflight access/authentication, supported request, automatic
events, review scope/base, result location, and authority. Missing integrations,
unsupported triggers, permission failures, or unavailable independent review
are concrete source blockers, not clean outcomes.

## Rounds and explicit outcomes

Default budget is ten rounds including the initial round; the human can set a
different limit. A round covers its complete active source set, not a count of
commits, pushes, or comments. Maintain configured/active/retired source state.

1. Round one includes all configured sources except Copilot already retired by
   permitted explicit unavailability. Check automatic requests before requesting;
   at most one request per source/round/head. Give supported reviewers bounded
   holistic context: affected behavior, interactions, invariants, regressions,
   relevant validation, and exclusions. Record fixed-trigger limitations.
2. Record source identity, request/time/window, head SHA, base/scope, and result
   IDs/reports. Read paginated thread comments, reviews, non-thread summaries,
   check results, and independent reports. Attribute results to the request and
   reviewed revision; keep human feedback separate.
3. Require actionable feedback, explicit clean completion, or permitted Copilot
   unavailability from every active source. Silence, elapsed time, missing status,
   generic tool errors, exit zero, skipped output, and old results are not clean.
   Poll coarsely with user interruption; default routine ceiling is 20 minutes
   per round. Pending/failing required sources at the ceiling stop integration.
4. Investigate every actionable item through local/regional/global root-cause
   and scope analysis before editing. Repair coherent in-scope clusters and
   verify the owning invariant and affected caller paths. Follow up unrelated
   defects without silently widening the PR; safe containment cannot mask or
   duplicate a systemic defect. Address every thread/comment, including duplicates,
   obsolete items, no-change rationales, and independent findings without thread
   IDs. Resolve only genuinely addressed requests.
5. After repairs, the next round includes only sources that found actionable
   feedback in the immediately preceding round. Explicitly clean sources retire
   for this PR and must not be manually re-requested without human direction.
   Do not disable automatic-review settings; triage later automatic feedback.
   Keep retired sources' reviewed SHA/scope historical after head changes.
6. If head changes while sources are pending, record it and ensure every active
   source receives/has a supported request for the current head. Do not count a
   delayed earlier-head result as current. Late feedback still needs triage and
   disposition; it does not silently reactivate a retired provider. Report a
   coverage exception when relevant.
7. Stop rounds only at review completion, a concrete blocker, or budget
   exhaustion. Unresolved feedback at the limit prevents merge; obtain explicit
   extension before round eleven. Small comments and green CI do not relax this.

## Copilot explicit unavailability

Permit absence only after an attributable cannot-run response from Copilot or its
integration for this PR's request/preflight, including quota exhaustion or any
other stated reason. Record `explicit unavailable`, reason, evidence text/ID/link
or secured output, time, request, and attempted head SHA. State that this attempt
provided no Copilot review coverage. Preserve earlier reviews and all findings
separately. Silence, pending state, missing status, timeout, and local tool errors
do not qualify.

Unless specifically required by the human or repository policy, retire requests
for this PR without a waiver or repeated retries, including after later pushes.
Keep unavailable distinct from clean and retain it until the human re-enables
Copilot. Configuration alone is not a specific requirement. Continue available
independent review and all other gates; request independent review if none is
active or complete. An empty active set is insufficient. Explicitly required
Copilot remains a blocker when unavailable; earlier/late actionable feedback
still needs normal disposition.

## Exact final-head coverage and security

Before merge, require a sufficient independent check of the final head/base and
complete net change. If earlier retired results do not cover it, use a separate
fresh read-only reviewer context rather than re-requesting retired providers.
Record this gate independently, including validation and explicit result.
Unresolved findings return to scoped repair within the budget; unavailable final
review blocks integration. Reuse an adequate exact-head independent result when
the relevant revisions have not changed. Reassess integration/net diff after base
changes; never imply an old reviewed SHA covers new commits.

Codex Security is selective for explicit/required/material security work, with
its own timeout policy. Prefer stable HEAD; any head change makes its assessment
historical for current-head acceptance. Retain findings and rerun the appropriate
assessment when acceptance remains required. This overrides security-source
retirement; it does not add security review to every routine round.

## Merge and next PR

Review completion requires explicit clean outcomes from all remaining active
sources, no actionable feedback, sufficient final independent coverage, and any
permitted Copilot absence correctly recorded. Verify required CI/approvals,
protection, conflicts, and queue state separately. Use the integration runbook's
expected-head condition, actual merged-state/destination readback, and eligible
cleanup. A submitted/queued merge is still pending. Honor no-merge/review-only.

Link source units to actual destination changes, record retained sources, and
refresh the consolidation ledger before the next PR. A blocker stops dependent
integration while safe independent preparation may continue. Attach created or
continued task PRs when supported. Never repeat a verified merge for failed cleanup.
