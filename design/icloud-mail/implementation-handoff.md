# iCloud Mail implementation handoff

Prepared 2026-10-03. Authority in this step: planning only. Start execution only
after the user's next implementation instruction.

## Start command

> Implement the finalized iCloud Mail design and delivery plan through review,
> merge, and marketplace publication.

Read this file and `local-connection-plan.md` first. They are the scope baseline.
Use conventional-commit and iterating-pr-bot-fixes, including independent Codex
review, as already requested. No additional design approval is needed to begin.
Do not create a worktree. Reuse the task branch when its state still matches.

## Baseline and ownership

Observed branch: `codex/icloud-mail-connect`; HEAD:
`78d849a3716e7d8056aa177be26e5944998a8ae6`. One existing checkout. Reacquire status,
upstream, PRs and applicable instructions before edits; do not assume this
snapshot remains current. Preserve unrelated work.

Uncommitted draft already exists in:

- `plugins/icloud-mail/mcp/server.py`
- `plugins/icloud-mail/mcp/setup.py`, `setup.html`, `keychain.py`
- `tests/test_icloud_mail_context.py`, `test_icloud_mail_setup.py`
- `scripts/check_distribution_bundle.py`

These are starting material, not approved or verified implementation. Reconcile
rather than overwrite them. Design documents are also uncommitted. No runtime
code was changed during this planning step.

The executing Codex agent owns implementation, integration, evidence and release.
An independent Codex reviewer owns the separate review pass; CodeRabbit is the
other requested source. The user alone enters any real Apple credential through
the local page. No real credential is a prerequisite to start development.

## Fixed implementation decisions

1. Keep local stdio MCP, fixed Apple endpoints, standard library mail handling,
   one local setup page and native Keychain storage. No additional runtime
   package, server infrastructure, credential broker or mail repository.
2. One configured account per configuration path. Reconnecting the same account
   preserves optional sender settings; switching accounts resets optional values.
   Do not delete old Keychain items during switching.
3. Serialize account saves using an OS advisory lock associated with the canonical
   configuration path. All account-settings mutation paths must respect it.
   Capture a configuration revision before candidate authentication; recheck it
   under the lock before persistence. If it changed, reject the stale save with
   instructions to reopen setup. Read the previous credential under the lock;
   keep the lock through Keychain/config write and rollback. Lock acquisition is
   bounded by the operation deadline. The lock file contains no secret or mail.
   No persistent lock daemon or transactional database is needed.
4. Distinguish ordinary failure with successful rollback from failed rollback.
   Failed rollback means local connection state needs repair; report that and
   direct the user to reconnect. Never say prior state was preserved if it was not.
5. The setup lifetime is ten minutes; validation uses at most 90 seconds and
   never extends past the remaining session lifetime. Disable repeat submission
   while validating. No automatic retry of authentication or mail sends.
6. Use the same native Keychain helper for setup writes and production reads on
   macOS; remove the duplicate CLI read path once the shared helper is verified.
   Retain only existing necessary non-macOS manual behavior, not a second macOS
   credential backend. Verify an item written by setup is readable through the
   actual production credential lookup with expected OS authorization behavior.
   Use a uniquely named synthetic Keychain service/account for native verification.
   Clean up only that test item. Do not inspect or replace the user's real stored
   credential for testing. Denied system access is an environment limitation,
   not a passing native test.
7. Account status must distinguish configured from verified. No persisted message
   content or durable success assertion is needed. Mail can become unavailable
   immediately after successful verification; errors must remain truthful.
8. Do not create a new export tool, Disconnect workflow, OAuth flow, writing-style
   integration, or cross-platform GUI in this release. Preserve existing supported
   mail operations and describe clear-configuration semantics accurately.
9. Intended version is 0.2.0, subject to live tag/version verification. Personal
   marketplace publication means this repository's established tag and catalog
   workflow; it does not mean submission to OpenAI's universal directory.

## Ordered work and milestone evidence

| Work | Outcome and write set | Acceptance | Dependencies / completion evidence |
| --- | --- | --- | --- |
| WI-1 | Reconcile candidate auth, Keychain, save locking, failure receipts and setup launcher in `mcp/`; focused tests | AC2, AC3, AC8 | Inspect draft; successful and failed candidate auth, stale/concurrent save, rollback failure, startup failure, reconnect precedence proved |
| WI-2 | Finish page and temporary HTTP lifecycle; setup tests and isolated browser harness | AC1, AC4 | WI-1; keyboard flow, labels, progress, safe errors, no-store, request rejection, shutdown and expiry verified |
| WI-3 | Prove no plugin email persistence and preserve mail contracts | AC5, AC6 | WI-1/2; synthetic search/read/attachment/draft cases, filesystem/log capture and persistence source audit; full tests pass |
| WI-4 | Complete bundle closure, user docs, security disclosure, version/changelog and install checks | AC7 plus all user-facing contracts | WI-1–3; clean package imports/launches; docs agree with storage/auth behavior; manifest/version parity |
| WI-5 | Commit/push focused feature PR and obtain clean reviews and CI | All | WI-1–4; complete diff reviewed, CodeRabbit + independent Codex outcomes tied to exact commit; required checks pass |
| WI-6 | Merge, publish immutable release, activate catalog and verify installed artifact | Distribution | WI-5; merge SHA, tag SHA, catalog ref and installed version/source identities recorded |

Critical path: WI-1 → WI-2 → WI-3 → WI-4 → WI-5 → WI-6.
No calendar estimate is committed. External review availability and real-user
Apple authentication have unknown timing. Report meaningful milestones and any
blocking condition; do not expand scope to fill wait time.

Milestone commits should remain coherent and passing:

- MS-1: validated local connection and safe persistence (`feat(icloud-mail): ...`).
- MS-2: privacy evidence, complete packaging and documentation, version intent
  (`test`, `fix`, `docs` or feature commit as the final diff warrants).
- MS-3: review corrections in focused Conventional Commits.
- MS-4: release/catalog changes according to established repository workflow.

Do not split code and required dependencies into a broken milestone merely to
match this list. Include the finalized design/handoff with the first appropriate
commit. Inspect full staged diff and exclude unrelated changes before each commit.

## Verification runbook

Use the existing `.venv` locally. Run focused checks while developing, then once
on the release candidate; repeat only affected checks after further changes.

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_icloud_mail*.py' -v
.venv/bin/python plugins/icloud-mail/mcp/server.py --self-test
.venv/bin/python scripts/check_plugin.py plugins/icloud-mail --layout source
.venv/bin/python scripts/check_distribution_bundle.py plugins/icloud-mail
.venv/bin/python scripts/check_marketplace.py .
.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
```

Add behavioral coverage for gaps, not tests that freeze prose or private call
order. Verify the package from a clean isolated materialization with no source
checkout import dependencies. Reuse the existing bundle helper/checker rather
than introducing another packaging system. Check declared runtime compatibility.

Browser evidence must use the real rendered page with synthetic credentials and
mocked Apple/persistence boundaries; cover success, failure, expiry and keyboard
use. A production mock-auth option must not be introduced. Verify startup readiness
without returning its secret URL through MCP. Record native Keychain results
separately from browser/mock tests.

For AC5, capture attempted persistent writes and diagnostic output at operation
boundaries using synthetic mailbox fixtures and temporary configuration paths.
Check that no message headers, body or attachment sentinels appear in saved files
or logs. Intentional MCP result content is allowed. Inspect source for caches,
indexes, temporary attachment writes, telemetry and background jobs; tests alone
cannot prove a repository-wide absence. No claim that OS swap or Codex transcript
storage is controlled by the plugin.

Real mailbox smoke test is optional user participation, never a fabricated pass:
user enters credentials privately, then explicitly authorizes a bounded read-only
check. Sending mail needs separate explicit intent. Release may proceed with
passing required automated/native/browser/package/review gates and a prominently
recorded lack of real-account acceptance; do not call live authentication proven.

## Review and release gates

1. Re-read configured review skills, repository instructions and PR template at
   execution time. Preflight CodeRabbit availability, but attempt actual review
   before classifying historical authentication issues as current blockers.
2. Use CodeRabbit CLI and an independent Codex review, including security and
   no-email-storage requirements. Record base/head, source, timestamp, findings,
   fixes and terminal outcome. Apply pattern checks through Codanna and source
   searches. Limit to ten rounds; no silent reviewer substitution or false clean.
3. Run all applicable CI. Current workflows include validation and HOL iCloud
   scanning with minimum score 80 and failure on high severity. Recheck actual
   required branch rules and scan outcomes on the final head before merging.
4. Create/attach the feature PR, with catalog still pinned to the prior published
   tag. Merge only after required evidence is clean. If a reviewer is unavailable,
   preserve the completed code/PR and report the precise remaining release gate.
5. Publish the annotated `icloud-mail-v0.2.0` tag and release from the verified
   merged source, following current release docs. Never move an existing tag.
6. Activate the personal marketplace catalog only after that immutable artifact
   exists. Use a small follow-up PR if protected-branch rules require it; run
   relevant validation and review for that diff before merge.
7. The earlier request to update root README directly on `main` remains recorded.
   Recheck current branch rules: if direct writes are prohibited, include that
   documentation in the normal reviewed merge and report the constraint. Do not
   weaken branch protection or bypass signature requirements.
8. Verify source/tag/version/catalog and a fresh isolated install agree. Preserve
   the user's installed cache unless an update is explicitly part of the chosen
   verification. Remove only safe, merged task branches according to review skill
   instructions; never discard dirty files or unpushed work.

## Risks, stop conditions and recovery

| Risk | Response / owner | Disposition |
| --- | --- | --- |
| Secret leakage via form, exceptions or process launch | Implementer: boundary tests and independent security review | Blocks release if demonstrated or unresolved |
| Concurrent or partially failed credential/settings save | Implementer: bounded shared lock, stale check, rollback tests and repair receipt | Blocks release if known mixed-account state is possible in normal concurrent operation |
| Native Keychain access denied or untested | Implementer: isolated synthetic item; record OS prompt/access limitation | Required native gate remains open; never substitute mocks |
| CodeRabbit or CI unavailable | Release owner: record actual failure, complete independent work | No merge until required gate resolved |
| No live Apple acceptance | User may opt into private smoke test; release owner discloses coverage gap | Does not require collecting a credential or prevent starting work |
| Accidental email persistence | Implementer: AC5 evidence, source audit and review | Blocks release |
| Need for unsupported native account/writing-style registration | Keep outside scope, report verified platform limitation | No infrastructure workaround |

Rollback selects the prior immutable marketplace tag and preserves local settings.
It does not reverse intentional mail operations. Keep findings within required
correctness, privacy, security and regression scope; defer optional hardening or
new features explicitly rather than extending the project silently.

## Execution checklist

- [x] Requirements and final architecture recorded.
- [x] Existing draft and remaining work mapped.
- [x] Verification, review, release and recovery paths specified.
- [x] Independent readiness review incorporated (2026-10-03): no architectural
  blocker; native read/write consistency, save serialization, error receipts,
  privacy copy and live-acceptance disposition are included above.
- [ ] Await one implementation command.

Execution is ready when the independent readiness check has no unresolved material
design decision. This is readiness to implement, not a release-readiness claim.

Readiness disposition: **READY TO IMPLEMENT**. No unresolved product or
architecture decision blocks the start command. Runtime checks and reviews remain
future evidence, not completed work. Design finalization used read-only source/CI
inspection and independent review; no implementation test was rerun in this step.
