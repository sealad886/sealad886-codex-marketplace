# Review sources and current evidence

Use available supported provider tools or authenticated CLI/API access. Discover
capabilities first; installation of this package supplies no GitHub credential,
review service, or permission. Keep the request and result bound to repository,
PR, source identity, head SHA, base/scope, and time. An accepted request proves
invocation, not completion. Refresh current primary docs when behavior differs.

## Independent review

Use a fresh read-only reviewer context with exact head/base, intended behavior,
affected interactions, validation results, and exclusions. Request concrete
correctness/regression findings across the complete affected flow. The
implementing agent's self-check is not independent review. Save the report or
retain a durable host reference; record explicit completion and any limits.

If a review source is retired after a clean result and later changes lack
independent coverage, use a separate fresh context for the final-head gate.
Do not disguise another request to a retired provider as this check. Reuse a
sufficient exact-head independent result when no relevant revision changed.
Unresolved final-check findings return to repair; do not merge on an empty
active-source set or unavailable independent review.

## GitHub Copilot

Private-repository Copilot reviews consume Actions minutes as well as AI credits
under current [GitHub billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions).
Include those reviews when assessing the cost of each push/review round. Standard
public-repository runner usage is free; self-hosted execution, larger runners,
storage and other providers' quotas need separate accounting. Inspect available
account evidence rather than applying a fixed OS multiplier or treating elapsed
workflow time as billed minutes. Missing billing access is an evidence limit,
not authority to change billing, runners, visibility or review policy.

Current GitHub documentation supports CLI review requests such as:

```sh
gh pr edit PR_NUMBER --repo OWNER/REPO --add-reviewer '@copilot'
```

Verify installed CLI support, target host, identity, request acceptance, and
automatic-review events first. The documented REST reviewer identity is
`copilot-pull-request-reviewer[bot]`; do not assume a human mention comment is
a supported review trigger. Do not add/remove repository settings to enable it.

Copilot normally posts a Comment review. Configured approvals can now be enabled
and may satisfy applicable repository approval rules. A readiness assessment in
the overview alone is not an approving review. Read the actual review state,
summary, findings, dismissal status, and reviewed commit; only explicit
no-findings or equivalent completion is clean for this workflow. Copilot may
repeat comments on re-review; duplicate findings still need dispositions.

Automatic review of new PRs, new pushes, and draft PRs depends on account and
repository/organization configuration. Several automatic sources can apply.
Inspect active requests/events before adding a request and do not manually
duplicate an automatic review. A clean-source retirement limits this workflow's
manual requests; it does not authorize disabling repository automation.

Replies to Copilot findings are visible to humans, but do not instruct Copilot
to re-review. Use a supported request mechanism for a still-active source.

### Explicit unavailability

An attributable response saying Copilot cannot run permits `explicit unavailable`
for any stated reason, including quota exhaustion. Preserve reason, raw response
or provider ID/link, request/preflight, timestamp, and attempted head. It supplies
no review coverage; do not relabel its attempted SHA as reviewed. Keep earlier
review evidence and all earlier/late findings separate.

Unless specifically required by the human or controlling repository policy,
retire Copilot requests for this PR without asking for a waiver or retrying on
every push. Preserve the disposition until human direction re-enables it.
Configuration alone does not make it mandatory. An explicit requirement remains
a review/merge blocker when unavailable. Continue available independent review
and all CI/approval/queue gates. Silence, timeout, missing status, generic local
errors, and pending requests never qualify for this exception.

## Other configured GitHub reviewers

Preflight the established trigger and result surfaces. Do not introduce another
external source or export private code without authority. A summary-only service
does not provide a clean findings review unless its documented explicit outcome
actually establishes that result. Capture a supported CLI's report and real
process completion; exit zero, skipped/no-change, authentication failure,
rate limiting, or interrupted output alone is not clean. Only Copilot has this
package's default explicit-unavailability exception.

## Codex Security

Use only when explicitly requested, required, or justified by material security
risk. Prefer ordinary fixes first and assess a stable head. Use the installed
assessment's own progress/timeout policy. Record its exact head and scope before
starting and recheck before accepting results. Any head change makes the report
historical for current-head acceptance; preserve findings and rerun the relevant
assessment if acceptance remains required. Security freshness overrides that
source's retirement without adding a security scan to every routine round.

## Primary documentation

Review-provider behavior checked 2026-10-18; Actions billing checked 2026-10-27.
Inspect current provider documentation and installed capabilities before use:

- [Using Copilot code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review)
- [Configuring Copilot reviews](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review)
- [GitHub review requests API](https://docs.github.com/en/rest/pulls/review-requests)
- [GitHub CLI PR edit](https://cli.github.com/manual/gh_pr_edit)
