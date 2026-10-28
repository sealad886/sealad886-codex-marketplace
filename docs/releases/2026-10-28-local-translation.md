# Local Translation 0.1.0 release candidate

Prepared 28 October 2026 (Europe/Dublin), before publication. The user authorized
publication after review, hosted checks, integration and release readback. This
preparation record does not itself establish publication or a live model
deployment; consult the GitHub release for its final state.

## User-visible change

Local Translation adds one professional-service workflow skill and eight local
MCP tools. The project manager coordinates actual translator, independent
bilingual reviser, terminology, subject, engineering and quality agents, with
queries, attributed expert exchanges, correction rounds and human decision
rights. Its role map covers all sixteen functions in the supplied whitepaper.

The text runtime calls an operator-configured local Index-Translate deployment
for UTF-8 prose and explicit JSON segments across multiple target locales. It
checks model identity, rendered token budgets, completion shape and supported
invariants; preserves source and candidate identities; invalidates stale review
evidence after corrections or shared queries; and prepares a delivery candidate
for human acceptance. The package includes an original square logo, matching vector icons and a README banner.

The local runner must expose `/v1/models`, `/v1/chat/completions` and chat
`/tokenize`. Model weights and runner installation remain operator prerequisites.
The host must supply real delegation facilities, and its agents may use cloud
providers. The release does not establish live Index quality, hardware fit,
egress confinement, qualified human revision, audiovisual production or human
publication acceptance.

## Version and distribution ownership

Both plugin manifests own version `0.1.0`; this is the first release of
`local-translation`. Its canonical Codex catalog entry uses a local package
source within the selected Git-backed marketplace checkout. The generated
Copilot catalog points to the same package. No new cross-plugin runtime,
account-plugin object or hosted service is required.

Publish an annotated `local-translation-v0.1.0` tag from the exact validated merged
source commit, with a single-plugin ZIP built from that commit. Preserve the root
portable manifest, Codex overlay, both MCP declarations, skill, runtime, examples
and artwork. Record the final payload/archive digests with the release.

## Preflight evidence

- Remote repository: public `sealad886/sealad886-codex-marketplace`; configured
  origin uses that repository for fetch and push. Default branch is `main`.
- At preflight, remote `main` is `44d1868292841f5866f2f82f3f33c045af8b2919`, the
  merged Repository Guidance PR #57. The candidate starts from that PR's original
  head `b175ecb348fc678a66089982ada3d7f1db9f86b5`; their trees match, but commit
  ancestry differs. Refresh and assess the integration base before final review.
- No existing PR for `codex/local-translation` or existing Local Translation
  release/tag was found during preflight. Recheck before creation/publication.
- Latest published marketplace snapshot is `marketplace-v0.1.12`, at remote
  `main`, published 27 October 2026. The next allocation would currently be
  `marketplace-v0.1.13`; the existing publisher owns final allocation and recovery.
- [Original candidate verification](../reviews/2026-10-28-local-translation.md)
  records 634 passing repository tests, including 19 translation regressions,
  both catalogs, all 15 package source/distribution checks, manifest/skill checks,
  independent review and isolated native Codex/Copilot installation. Refresh
  affected evidence after artwork or source changes; bind release checks to the
  actual final revision rather than inheriting these results automatically.

## Review, integration and publication sequence

1. Finalize original logo, icon and banner, their package references and final
   distribution inventory. Complete the local change and Conventional Commit.
2. Prepare the task PR against refreshed `main`; record exact head/base in the
   review ledger. Reuse existing automatic reviews rather than duplicating them.
   Recent PRs #56 and #57 demonstrate automatic Codex code/security summaries on
   opening a PR. Supported explicit triggers are `@codex review` and
   `@codex security review`. Independent exact-revision review remains required.
   Installed GitHub CLI 2.103.3 supports requesting Copilot with
   `gh pr edit <PR> --add-reviewer '@copilot'`; inspect active requests first.
3. Follow the Iterating PR Bot Fixes workflow for explicit source outcomes,
   scoped repairs and current final-head evidence. A provider request or passing
   CI alone is not a clean review. Preserve attributable Copilot unavailability
   separately if encountered; no such attempt has been made at this preflight.
4. Require hosted validation and the pinned HOL scan, including Local Translation,
   without high or critical findings. Existing CI runs on PR updates and pushes
   to `main`; semantic-versioning example CI has its own path filters. Batch
   settled repairs before pushing. Workflows use standard public Ubuntu runners.
   Account billing usage could not be read: the billing API returned 404 with a
   missing `user` scope. No measured account billing is claimed. GitHub's
   [billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
   states standard public runners and public-repository Copilot review compute
   remain free; storage and other quotas have separate accounting.
5. Re-read the active default-branch ruleset before merge. Preflight ruleset
   `20217661` requires signed commits and a PR, permits only merge commits, and
   requires zero approving reviews. It has no required-status-check or
   thread-resolution rule. Honor its requirements and the repository's stronger
   verification policy without using the available administrator bypass.
6. Verify the actual merged destination and exact source identity. Build and
   inspect the archive from that source; create the annotated plugin tag and
   stable GitHub release only after gates pass. Match the established asset name
   `local-translation-v0.1.0.zip` and provide the archive SHA-256 in release notes.
7. The existing `plugin-release-marketplace.yml` stable-release event validates
   the plugin release commit, then allocates/tags/publishes the marketplace
   snapshot as GitHub Latest. Do not create a competing manual snapshot while
   that publisher is running. Reconcile actual releases/tags before recovery.
8. Read back plugin tag/release asset and the resulting marketplace snapshot.
   Perform clean consumer discovery/install checks against the published source,
   then uninstall test/development Local Translation instances and confirm it is
   absent from the user's active installed inventory. Preserve unrelated plugins
   and user settings; do not reinstall the plugin for the user afterward.

## Installation after publication

```bash
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add local-translation@sealad886-codex-marketplace
```

```bash
copilot plugin marketplace add sealad886/sealad886-codex-marketplace
copilot plugin install local-translation@sealad886-codex-marketplace
```

For an existing marketplace registration, inspect its source and use the client's
upgrade/update command instead of adding a duplicate. Invoke
`$local-translation:translation-project` in a host with the required tools and
local configuration. Publication and loading are separate from translation
quality and human acceptance.

## Final local candidate checks before the first PR push

- Complete repository suite: 637 tests passed in 119.718 seconds, with no skips.
- Translation regressions: 22 passed, including persisted delivery retirement and
  controlled state/marker write failures.
- All 15 catalog packages passed source and distribution validation; both catalogs,
  route contracts, historical receipts, Semantic Versioning, Plugin Creator and
  Skill Creator checks passed. The final bundle contains 26 files and one skill.
- Codex 0.164.0 and Copilot 1.0.103 isolated discovery/installation passed after
  artwork integration. Codex exposed all eight tools. All new temporary installs
  were uninstalled, and the task-created Copilot local-marketplace registration
  was removed. Neither normal client profile had Local Translation installed.
- Original logo, vector icons and banner are included; their prompts and method
  are recorded in the [artwork provenance](../artwork/2026-10-28-local-translation.md).
- Hosted review, HOL scanning, merge and publication are subsequent provider gates.
  Synthetic checks do not establish real Index inference or translation quality.
