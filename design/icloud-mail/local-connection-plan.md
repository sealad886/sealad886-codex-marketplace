# iCloud Mail: local connection design

Final design specification — 2026-10-03. Implementation and release are pending.
This supersedes any hosted connector or OAuth intermediary proposal.

## 1. Purpose and scope

Give Codex on the user's Mac direct, on-demand access to the user's iCloud-hosted
mailbox. iCloud remains the source of truth. The plugin is a mail client bridge:
it does not replicate, synchronize, archive, or index the mailbox locally.

Retain the existing bounded search, read, attachment, thread, draft, send, reply,
forward, flag, move, archive, and trash operations. Mail mutations require the
user's applicable intent; connecting an account grants no blanket permission to
send or organize mail. Setup sends no message and changes no mailbox content.

The new guided connection experience targets macOS and uses an Apple
app-specific password. It requires no developer-operated backend, hosted login
service, OAuth issuer, database, scheduled synchronization, or persistent setup
daemon. Ordinary connections to Apple and Codex's model service still occur.

Native Codex Connected Accounts and Reference my writing style registration are
not acceptance requirements for this release. No supported integration contract
has been verified for this local plugin. Do not imply that a manifest flag or
local login automatically enables either feature.

## 2. Architecture and existing code

```text
User browser ── temporary loopback setup ── macOS Keychain + account settings
                              │
                              └── validate directly with Apple's mail servers

Codex ── local stdio MCP server ── TLS IMAP / SMTP ── iCloud mailbox
              │
              └── reads local settings and Keychain credential
```

Extend the canonical implementation instead of replacing the mail client:

| Component | Responsibility |
| --- | --- |
| `.mcp.json` | Launch local Python MCP process; no remote connector mapping |
| `mcp/server.py` | Existing mail operations, validation, settings, scoped candidate credentials, setup launcher |
| `mcp/setup.py` | Temporary loopback HTTP service and connection transaction |
| `mcp/setup.html` | Self-contained, accessible connection form; no external assets |
| `mcp/keychain.py` | Shared native macOS credential reads and writes through Security.framework |
| Plugin skill and README | Connection guidance, authorization boundaries, accurate storage disclosure |
| Distribution checker | Include and verify every runtime setup dependency |

Use Python's standard library and macOS system frameworks. Keep Apple hosts
fixed: IMAP `imap.mail.me.com:993` with TLS; SMTP `smtp.mail.me.com:587` with
STARTTLS and certificate verification. No arbitrary server URLs or relay.

## 3. User experience

1. User asks to connect iCloud Mail. Codex calls `open_account_setup` with no
   credentials or arguments. The local process opens the system browser.
2. A single page requests **iCloud Mail address** and **App-specific password**.
   Explain that the mailbox address may differ from the Apple Account login
   address; a Gmail Apple Account login is not automatically an iCloud mailbox.
3. Prominently state: **Do not enter your normal Apple Account password.** Link
   to <https://account.apple.com/account/manage> and explain Sign-In and Security
   → App-Specific Passwords → generate a password for this plugin. Mention that
   Apple requires two-factor authentication. Keep the page open during this step.
4. Explain before submission: credentials are stored in this Mac's Keychain;
   mail remains on iCloud; mail requested through Codex is returned to Codex.
5. User submits Connect. Disable duplicate submission, show validation progress,
   and authenticate with both IMAP and SMTP. Do not send a test email.
6. On success, save the credential and settings, show confirmation, clear the
   password input, and stop the setup service. User can close the tab.
7. On failure, show a safe, actionable error, clear the password input, preserve
   the previously saved connection, and permit another attempt before expiry.
   Expired sessions require reopening setup.

Provide field labels, keyboard access, visible focus, password input semantics,
accessible progress/error announcements, and usable narrow-window layout. No
credential in a URL, browser storage, analytics, or error report. The unavoidable
in-memory form value exists only while needed; do not promise secure erasure of
browser or Python memory.

## 4. Authentication and connection lifecycle

The app-specific password authenticates directly to Apple's IMAP/SMTP services;
it is not exchanged for a plugin-issued token. No custom authentication protocol.
Normalize Apple's password formatting and reject clearly invalid input locally.
Formatting validation cannot prove that a supplied value is not a primary
password; the explicit instruction remains essential.

`open_account_setup` returns only launch status and instructions. It never
returns the session URL, token, password, or a claim of successful authentication.
`get_account_status` distinguishes saved configuration from live connectivity.
`validate_account` provides explicit current network verification.

Candidate validation uses `account_session` to scope candidate configuration and
password without changing environment variables or saved settings. Reuse existing
IMAP/SMTP validation, resource limits, and deadlines. Save only after both pass.
Same-account reconnection preserves sender settings; selecting a different account
uses that account's defaults. Local Keychain credentials take precedence over an
older password in the process environment.

Persist the Keychain item, then atomically write non-secret settings. Restore the
previous Keychain value if settings persistence fails. Serialize saves across
concurrent setup sessions and detect stale state before replacement, so two
windows cannot silently combine different accounts or overwrite a newer save.
A process crash between the two stores is not an atomic transaction. Do not
claim reliable crash detection without evidence or add a journal solely for it.
If an incomplete save is detected, report it honestly and recover by reconnecting. Never log old or new
credentials. Setup must not delete another account's saved credential.

Retain the existing explicit clear-configuration operation with an accurate
receipt: clearing settings does not revoke Apple's password or remove a retained
Keychain item. Explain local removal in Keychain Access and revocation at Apple;
do not introduce a misleading Disconnect control. Revoked credentials require
user reconnection; no background reauthentication or retry loop.

## 5. Storage and privacy contract

| Data | Location and lifetime |
| --- | --- |
| App-specific password | macOS Keychain, service `codex-icloud-mail`, account keyed by mailbox; no plugin-managed synchronization |
| Mailbox address and optional sender settings | Existing local configuration file, restrictive permissions and atomic replacement |
| Setup session token and candidate password | Process/browser memory for the temporary setup session |
| Messages, headers, attachment bytes, search results, drafts being composed | Bounded memory for the requested operation; no persistent plugin cache |
| Mailbox drafts and mail mutations | Apple's mailbox, through existing authorized operations |
| Results sent to Codex | Conversation/model processing; subject to Codex's own handling, outside plugin retention control |
| Explicit user export | User-selected destination only when requested; no automatic export or new export subsystem |

No persistent email database, mailbox replica, search index, content-bearing
telemetry, body/attachment temporary files, offline mailbox, background prefetch,
or content saved for writing-style analysis. Searches run against iCloud. Release
operation buffers when no longer needed. Small transient protocol metadata such
as login-candidate hints is not a content repository and must remain bounded.

Configuration is currently under `~/Library/Application Support/Codex/iCloud Mail/`
on macOS, with the existing explicit path override. Existing non-macOS manual
configuration is outside the new guided setup scope; add no compatibility layer.
Do not put passwords in MCP inputs/results, shell arguments, setup-child environment,
configuration, application logs, or browser storage. MCP stdout carries protocol
output; the setup child emits only a fixed readiness signal. Production Keychain
reads use the same native helper in a killable child with a ten-second cap bounded
by the remaining operation deadline. Its credential response uses a private pipe,
never the MCP transport or logs. Mail returned through MCP is intentional output,
not a diagnostic log.

The plugin cannot guarantee that the OS never swaps memory, that browser history
never records the non-secret loopback address, or that Codex does not retain a
conversation. Describe the guarantee as no plugin-managed persistent email store.

## 6. Local setup security and failure handling

- Bind only `127.0.0.1` on an ephemeral port. Use an unpredictable session path
  and token, exact Host and Origin checks, and a required token on submissions.
- Pass the session token in the browser URL fragment, remove the fragment after
  reading, and keep it in memory. Never print the private URL through MCP/logs.
- Reject wrong routes, methods, content types, oversized bodies, invalid tokens,
  and cross-origin requests before attempting Apple authentication.
- Apply restrictive CSP, no-store and no-referrer headers, no external assets,
  and no access logs. Bound request/socket times and authentication attempts.
- Allow only one validation per session at a time. The service expires within
  ten minutes, including stalled requests; success terminates the session.
- Strip inherited password variables from the setup child. Native Keychain APIs
  write secrets without embedding them in command lines.
- Handle Keychain denial, authentication rejection, network/TLS failure, config
  write failure, browser launch failure, and expiry with secret-free feedback.
- A hostile process already executing as the same OS user is outside the local
  browser isolation guarantee. Use native Keychain protections; do not invent
  a second encrypted vault or promise isolation from a compromised Mac.

Retain the existing mail safeguards: UIDVALIDITY-aware references, bounded MIME
and attachment handling, read-only reads, explicit mutations, no permanent
expunge, and honest reporting of uncertain SMTP outcomes. Do not automatically
retry an uncertain send.

## 7. Acceptance and verification

| ID | Required evidence |
| --- | --- |
| AC1: Clear single-page setup | Browser check for two fields, correct Apple link, primary-password warning, mailbox identity explanation, keyboard/error/progress behavior |
| AC2: Local credential handling | Tests and source review show no password in MCP, argv, child environment, files, logs, or browser storage; native Keychain save/read/delete checks use an isolated synthetic item |
| AC3: Safe validation and persistence | IMAP+SMTP success required; failure preserves prior state; rollback, same/different account, reconnect precedence, concurrent/stale saves tested |
| AC4: Temporary local service | HTTP tests cover loopback binding, Host/Origin/token checks, content/size/time limits, success shutdown and expiry |
| AC5: No email repository | Representative search/read/attachment/draft operations against synthetic network fixtures produce no content-bearing filesystem writes or logs; inspect all persistence paths and confirm no sync/index/cache subsystem |
| AC6: Existing mail contracts | Focused and full regression suites, self-test, privacy/security review, and operation-boundary checks |
| AC7: Complete distribution | Bundle checks and clean packaged launch include HTML, setup, Keychain helper and canonical server |
| AC8: Truthful connected state | Page launch differs from configuration and live validation; expired/revoked/unavailable account outcomes do not claim connection success |

Use synthetic mail and mocked network/persistence boundaries in automated tests.
Separately verify native Keychain behavior with a uniquely named synthetic item
and clean up only that item. Real Apple acceptance requires user-entered private
credentials; never obtain them through chat. Record separately what was actually
verified. A successful mock test does not establish a successful live connection.

## 8. Alternatives and decision

- **Existing manual setup only:** avoids a new page but fails the approved simple
  connection experience. Retain useful primitives; make one guided page primary.
- **Hosted OAuth/credential bridge:** rejected by the user; adds remote secret
  custody and service operation that this plugin does not need.
- **Apple-authorized local OAuth client:** potentially appropriate if Apple grants
  a supported registration and contract. Not established for this plugin; do not
  invent endpoints or delay the documented app-password implementation for it.
- **Local email sync/index:** explicitly excluded. It would change the product's
  purpose and retain user content without a requirement.

## 9. Delivery and release

Execution details and the single start command are in
[implementation-handoff.md](implementation-handoff.md). That handoff resolves
native Keychain read/write reuse, save locking and live-acceptance release policy.

Current branch: `codex/icloud-mail-connect`. Existing code changes are an
uncommitted implementation draft, not evidence of acceptance. This finalization
changes the design document only. No remote service has been provisioned.

- [x] Finalize architecture, storage boundary, connection flow and acceptance.
- [ ] Reconcile draft implementation with this specification.
- [ ] Verify automated, native Keychain, browser and packaged behavior; document live Apple acceptance separately.
- [ ] Make coherent Conventional Commits; run CodeRabbit and independent Codex review until clean, within the established ten-round limit; satisfy required CI/security gates.
- [ ] Merge and publish under the user's existing release authorization after gates pass; verify tag/catalog/install identity.

Intended version: 0.2.0 from 0.1.1 for the new setup capability. Keep the production
catalog on the prior immutable tag until the new release is published and verified.
Update user documentation to match this storage/authentication contract. No mail
data migration exists because no local mail store is introduced. Reuse the current
configuration shape and Keychain identity; no conversion is currently needed. If
implementation requires a schema change, specify a one-time local backup and
conversion before editing existing configuration. Rollback uses the prior release
and preserves account settings; it cannot undo mail actions already requested.

## 10. Primary references

- [Apple: app-specific passwords](https://support.apple.com/en-us/102654)
- [Apple: IMAP and SMTP settings](https://support.apple.com/en-ie/102525)
- [Apple: authorization for supported third-party apps](https://support.apple.com/en-us/121539)
- [Google: desktop OAuth](https://developers.google.com/identity/protocols/oauth2/native-app) — demonstrates that OAuth itself does not require a developer-hosted backend; not an Apple implementation contract.
- [OpenAI: plugin packaging](https://developers.openai.com/plugins/build/plugins) — registered app mappings and bundled MCP servers are distinct mechanisms.
