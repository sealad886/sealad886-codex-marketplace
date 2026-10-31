# Mindrally Skills review and release ledger

## Identity and authority

- Repository: `sealad886/sealad886-codex-marketplace`; existing checkout.
- Authorized remote: `https://github.com/sealad886/sealad886-codex-marketplace.git`.
- Destination: `main`, initially `5075af6a3a3004f6c9864691ad4cc21bc676ef4a`.
- Task branch: `codex/mindrally-skills-plugin`.
- User authorized conversion of all upstream skills, individual accuracy review,
  progressive disclosure, milestone commits, ordinary push, the Iterating PR Bot
  Fixes lifecycle, marketplace publication, installation, development-install
  cleanup and local skill relevance controls. No new worktree is authorized.
- Upstream source: `7682ca77710e0971eab4e0ae5dddfa281aea0ba5`, 265 skills.
- Initial package version: `0.1.0`, the first published contract for this package.
  The existing stable `marketplace-v*` snapshot workflow owns marketplace numbers.
- Round budget: ten. Round one has not started; no task PR or remote push yet.

## Local milestones

- `57ccbba`: pinned source inventory and review plan; all 265 SHA-256 values
  matched the downloaded upstream source.
- Three non-overlapping batches perform semantic source review and write
  per-skill primary documentation, corrections and explicit execution limits.
- All 265 individual audits are complete, with 432 primary-source entries.
  Each skill and its conditional reference carry a prominent Apache-2.0
  modification notice; the upstream license remains unchanged.
- The coverage validator's five focused regression tests passed. They prove
  rejection of omitted skills/reviews, duplicate or mismatched review evidence,
  absent checked claims, and uncontained or unrouted references.

## Source preflight

| Source | Configuration and trigger | State | Evidence and limits |
| --- | --- | --- | --- |
| Independent Codex context | Required by the selected review workflow; fresh read-only reviewer after final implementation | Planned | Implementing agents' per-skill audits are implementation evidence, not the independent final-head check. |
| Codex on GitHub | Existing automatic review on PR open/ready; `@codex review` is the documented repository integration trigger | Preflight pending for this PR | PR #64 comment 6546598641 confirms the configured integration. Comment 6546599004 reports that earlier PR's review quota exhaustion; this is historical availability evidence, with no coverage of this task. |
| Copilot | No automatic request or submitted review found on preceding PR #64 | Not selected absent further configuration evidence | No assertion of availability or clean review. |

GitHub's active default-branch ruleset `20217661` requires signed commits and a
pull request, allows merge commits, and has zero required approving reviews.
No bypass will be used. Repository instructions still require successful
validation, scanner evidence with no high/critical findings, and independent
review. Re-read rules, head/base, checks and review state before merge.

## Execution and Actions usage

The repository is public. Existing workflows run validation and pinned HOL
scanner jobs on PRs and pushes to `main`; plugin publication triggers full
validation and automatic marketplace snapshot publication. Ordinary feature
branch pushes do not start these `main`-filtered push workflows. No billing,
runner, repository review setting or quota change is authorized. Exact billed
usage is unavailable; runner elapsed time is not treated as measured billing.
Batch coherent repairs into one push after each settled review round.

## Validation and remaining gates

| Check | Result |
| --- | --- |
| `scripts/check_mindrally_skills.py` | PASS, 265/265 individual reviews, matching source identities and directly routed references. |
| `scripts/check_marketplace.py .` | PASS, all 16 entries, preserved source declarations and release pins. |
| `scripts/check_copilot_marketplace.py .` after `--write` | PASS, all 16 entries and portable components. |
| `check_plugin.py --layout source` and `check_distribution_bundle.py` | PASS for all 16 catalog packages using clean temporary copies. Existing ignored files preserved. |
| Pinned OpenAI Plugin Creator validator | PASS; exact SHA-256 `ebda00d55d7518b127f675f062fb5c6e7a1ffdc0a99df1a55ac594400d7d3228`. |
| Installed Skill Creator `quick_validate` | PASS, all 265 skills. |
| Full `unittest discover -s tests -p 'test_*.py' -v` | PASS, 701 tests in 280.380 seconds, `ICLOUD_REMOTE_TESTS_REQUIRED=1`, existing project environment. |
| Native Codex CLI `0.166.0` | PASS, `plugin/read` before install shows full listing and 265 skills; `plugin/install` and fresh `skills/list` discover all 265. |
| Namespaced skill enablement | PASS, `skills/config/write` with `name: mindrally-skills:angular` disables only that skill; React remains enabled; test setting restored. |
| Clean prepared source / installed Codex cache parity | PASS, exact 538-file, 265-skill parity, payload SHA-256 `12dd601e6237957a66a23e9f095abce497e507646786d87bbb134553b168276d`. |
| Native Copilot CLI `1.0.105` | PASS, browse discovers the listing and the isolated local-marketplace install of the clean prepared package reports 265 skills. Copilot uses a live local source for this test; it does not create a copied cache. |

The first full-suite attempt inside the sandbox reported localhost socket
permission errors and failed signed Git fixtures. A focused fixture rerun and
the full suite passed outside the sandbox without changing signing settings.
The first clean-copy distribution check caught a globally ignored new
`.codexignore`; it was explicitly staged and the final package passed. A Finder
`.DS_Store` in the working package was preserved and excluded from prepared
release sources; the native installation/parity test uses the clean package.
No real client settings or credentials were used by these isolated tests.

- Fresh independent final-head/base review and configured-source outcomes:
  pending PR preparation.
- CI/scanner, protected merge readback, release tag/source identity, automatic
  marketplace release, installed cache parity and relevance settings: pending.

Per-framework examples have not been executed across 265 ecosystems. The
per-skill records distinguish primary-document checks from runtime acceptance.
No publication, merge, installed-plugin or enablement result is claimed yet.
