# iCloud Mail 0.2.0 validation

## Implementation milestone — 2026-10-03

- Local one-page setup, scoped candidate authentication, shared native Keychain
  reads/writes, serialized configuration saves, stale-state rejection and failure
  recovery implemented.
- No hosted service, database, synchronization process, index or email cache added.
- Full repository suite: **513 tests passed**. Focused tests cover scoped account
  contexts, setup HTTP/security/persistence behavior, locking, process startup,
  existing mail behavior and the no-content-persistence invariant.
- Source plugin validation, exact runtime distribution validation and MCP self-test
  passed. Distribution test launches the materialized runtime independently.
- Native macOS Keychain: a fresh synthetic service/account passed create, read,
  update and production `_password` lookup. Deleted that item and verified absence.
  Sandbox write failed; the inspected synthetic-only test passed outside sandbox.
- Browser: actual setup HTML rendered through the temporary server with mock
  Apple/persistence boundaries. Invalid input produced a safe error; keyboard
  submission of synthetic credentials reached success and hid the form. No actual
  Apple credential or mailbox was used. HTTP expiry is covered by automated tests.
- Privacy regression: representative search/read/attachment/draft operations reject
  filesystem writes, leave the temporary configuration unchanged, and emit no
  content to diagnostic streams. The remote draft receives the synthetic content.
  Source audit found only configuration persistence and user-requested outgoing
  attachment reads; no message store or background sync was introduced.

## Limits

Real Apple authentication and real mailbox operations have not been exercised.
Mock authentication is not evidence of live iCloud acceptance. Requested content
returned to Codex is subject to conversation handling outside this plugin.

## Release gates

CodeRabbit CLI, independent Codex review, final PR CI/HOL scanning, verified merge,
immutable tag, catalog activation and clean installation readback remain pending.
The production catalog still points to 0.1.1.
