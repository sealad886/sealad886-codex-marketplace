# Iterating PR Bot Fixes

Version **0.2.1**. One standalone skill for taking an identified GitHub pull
request through bounded review, scoped repairs, verified integration, and
eligible task cleanup.

The [skill](skills/iterating-pr-bot-fixes/SKILL.md) tracks explicit outcomes from
independent review and configured GitHub reviewers, investigates root causes
across affected code, and keeps findings within the PR's intended scope. The
default budget is ten review rounds. A source returning clean retires from
further manual requests; a separate final independent check covers later changes
without silently re-requesting retired providers.

Copilot's attributable cannot-run response can be recorded as `explicit
unavailable`, with no review coverage from that attempt. This never substitutes
for independent review or overrides an explicit Copilot requirement. CI,
required approvals, branch protection, and merge queues remain separate gates.

CI triage follows the first meaningful failure at the actual tested revision,
separates product defects from provider/environment and baseline failures, and
bounds authorized retries. Revision refresh distinguishes head, test-merge, and
merge-group evidence, handles late feedback, and resumes post-merge cleanup
without repeating a verified merge. Repairs from a settled review round are
batched, validated locally, and sent in one ordinary push, preserving final
remote checks. The ledger records push/review triggers and the basis of usage
claims. Private-repository Copilot reviews also consume Actions minutes under
[current GitHub billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions);
read-only status polling does not itself execute an Actions job.

## Install and use

In a Codex client supporting marketplace plugins:

```sh
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add iterating-pr-bot-fixes@sealad886-codex-marketplace
```

Start a fresh task after installation. Other clients can load the portable
Agent Plugins 1.0 package using its root manifest and `skills/` directory.

Example requests:

- "Use $iterating-pr-bot-fixes:iterating-pr-bot-fixes to drive this identified PR through scoped fixes,
  review, gated merge, and eligible cleanup."
- "Review and repair this PR, but do not push or merge."
- "Resume the PR's existing review ledger; verify current head before continuing."
- "Diagnose this PR's failed check before editing code; identify the tested SHA,
  failure cause, current merge gate, and whether a bounded rerun is authorized."
- "The base advanced and the queue rebuilt. Refresh current integration evidence
  while preserving retired clean reviewers."
- "This PR merged, but branch cleanup failed. Verify the merge and resume only
  the cleanup still authorized and safe."

An explicit full-lifecycle task supplies bounded authority for its necessary
commits, ordinary pushes, PR/review actions, gated merge, and eligible branch
cleanup. Review-only/no-push/no-merge instructions narrow it. Merely installing,
reading, quoting, or automatically loading the skill grants no action. New
worktrees require explicit authorization. Release/deployment, destructive Git
recovery, settings changes, and new source-export destinations stay outside it.

## Requirements and included references

Needs repository access, an available independent reviewer context, project
validation tools, and supported authenticated GitHub capabilities for provider
actions. GitHub CLI is optional; provider tools/API may be used. No MCP server,
runtime dependency, mandatory code indexer, or companion plugin is included.

- [Review sources and Copilot policy](skills/iterating-pr-bot-fixes/references/review-sources.md)
- [Pattern and scope analysis](skills/iterating-pr-bot-fixes/references/pattern-analysis.md)
- [Selective commit safety](skills/iterating-pr-bot-fixes/references/commit-safety.md)
- [CI diagnosis and bounded retries](skills/iterating-pr-bot-fixes/references/ci-triage.md)
- [Revision, queue, and interrupted-task refresh](skills/iterating-pr-bot-fixes/references/revision-refresh.md)
- [Conditional integration and cleanup](skills/iterating-pr-bot-fixes/references/integration-cleanup.md)
- [Resumable review ledger](skills/iterating-pr-bot-fixes/templates/review-ledger.md)

Use current provider documentation and installed capabilities. A successful
request, green CI, silence, or queue entry never proves review/merge completion.
Reports distinguish exact reviewed SHAs, source unavailability, actual merged
destination, and any preserved/blocked cleanup.

## Maintainer validation

From a checkout of the
[marketplace repository](https://github.com/sealad886/sealad886-codex-marketplace),
run its [source checker](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/scripts/check_plugin.py)
and [distribution checker](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/scripts/check_distribution_bundle.py):

```sh
python3 scripts/check_plugin.py plugins/iterating-pr-bot-fixes --layout source
python3 scripts/check_distribution_bundle.py plugins/iterating-pr-bot-fixes
```

Also validate JSON/YAML, contained links/artwork, exactly one skill, portable and
Codex metadata parity, and fresh-client discovery. These checks validate package
structure; actual provider requests, agent behavior, and desktop rendering need
their own evidence. See [security boundaries](SECURITY.md) and [MIT license](LICENSE).
