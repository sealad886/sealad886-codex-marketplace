# iCloud Mail review ledger

Budget: 10 rounds. Sources: CodeRabbit CLI and independent Codex.

## Round 1 — 2026-10-03

Head: `783b4d90886a934f8825143a07c2ed239ce86cb4`.
Base: `78d849a3716e7d8056aa177be26e5944998a8ae6`.
PR: https://github.com/sealad886/sealad886-codex-marketplace/pull/37

- CodeRabbit CLI 0.8.2: completed, one minor finding, reviewer and capture exit0.
  Captured report: `/tmp/icloud-coderabbit-round1.0keKsZ`.
  Unavailable setup page re-enabled Connect even though the user must reopen it.
- Independent Codex: completed, one P2 finding; report
  `/tmp/icloud-codex-round1.md`. A blocking native Keychain read could hang the
  synchronous MCP loop; former CLI lookup had a ten-second timeout.
- Both sources remain active for round 2 after fixes.

### Pattern analysis and repair boundaries

**Session termination:** local submit catch re-enabled the button; regional error
receipt handling also allowed retry after HTTP403. Same root cause: UI did not
honor terminal session state. Repair both paths. Other retryable validation errors
intentionally remain retryable. Global search found no sibling browser setup
implementation. HTML is outside the symbol index; source/DOM inspection used.

**Native read deadline:** Codanna index scope matched this repository; semantic
search, `_password` symbol61957, callers/callees and depth2 impact inspected.
Source confirmed IMAP, SMTP, validation and account status share the read owner.
Global native Keychain search found one helper implementation. Setup reads/writes
are bounded by a child watchdog; ordinary MCP reads were unbounded. Repair the
shared production read boundary with the same native implementation in a killable
helper process and private pipe; no second credential store or secret arguments.

### CI triage

Initial validation and every HOL scanner passed. GitGuardian reported the literal
alphabet sequence used by `test_password_shape` as a Generic Password at test
line41, incident37842720. Source confirms a synthetic normalization fixture, never
an Apple-issued credential. Its check disposition remains pending; do not weaken
scanning or rewrite history to hide it.

## Round 2

Head `1d4a6b876a0e34fce9fb817d559da6265a4bc40c`:

- CodeRabbit CLI completed with zero findings, both exit codes0;
  `/tmp/icloud-coderabbit-round2.9TWSuP`. Retired clean.
- Independent Codex completed clean, independently ran six timeout tests;
  `/tmp/icloud-codex-round2.md`. Retired clean.
- Native synthetic production lookup repeated after process-boundary fix: passed,
  test item removed. Focused iCloud suite269 passed.
- Configured Copilot review arrived for original head783b4d9: comments4173891039
  (same native timeout issue, already fixed) and4173891058 (IMAP disconnect
  classified as authentication failure). Retain Copilot as active source.

**Disconnect pattern:** Codanna `_network_error` symbol59883, callers/callees and
impact queried; local/regional/global searches confirmed SMTP disconnects handled
while wrapped IMAP aborts were omitted. Repair the one classifier; existing mail
operation abort handlers are intentional separate outcomes. Add regression through
real candidate validation with a synthetic IMAP abort, asserting no persistence.
Clean retired sources cover1d4a6b8; subsequent Copilot correction is outside their
reviewed revision. Round3 will request only Copilot.
