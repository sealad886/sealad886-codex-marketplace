# iCloud Mail security

## Supported authentication

Use an Apple app-specific password, never the primary Apple Account password.
The Apple Account must have two-factor authentication enabled. The server reads
the mailbox identity from the saved `configure_account` `account_address`.
`ICLOUD_MAIL_USERNAME` is a legacy fallback only when no saved configuration
exists. On macOS the server reads the app-specific password through native
Security.framework APIs from Keychain service `codex-icloud-mail`, keyed by the
mailbox address. A saved Keychain item takes precedence over the launch-environment
`ICLOUD_MAIL_APP_PASSWORD` fallback. Non-macOS manual configuration can use that
variable; the guided connection page requires macOS.

Non-secret account settings are stored outside the plugin cache in a user-only
configuration file. The account address authenticates the mailbox. Optional
aliases are outgoing identities only; incoming IMAP automatically includes
mail delivered to every alias in the mailbox.

The plugin does not implement Apple's newer third-party account authorization.
Apple documents that experience for supported apps, but does not publish a
client registration and token protocol verified for this local plugin. No hosted
credential service or OAuth intermediary is used.

## Local setup

`open_account_setup` opens a temporary single-page form on `127.0.0.1` at an
ephemeral port. The form prominently distinguishes an Apple app-specific password
from the normal Apple Account password and links to Apple Account settings.
Candidates authenticate directly with Apple's IMAP and SMTP services before
persistence; setup never sends mail. Native Keychain calls keep passwords out of
process arguments. The child environment omits `ICLOUD_MAIL_APP_PASSWORD`.

The page uses an unpredictable path and session token, exact Host and Origin
checks, bounded requests and authentication, no access logs, no-store and
no-referrer headers, and a restrictive content security policy. It has no external
assets or browser storage. The session ends after success or ten minutes; its
private URL and token are never returned through MCP.

Settings changes use a shared, bounded local lock and reject stale setup saves.
If configuration persistence fails after a Keychain write, setup attempts to
restore the previous credential. Failed rollback is reported as a repair-needed
state, not as preservation of the old connection. A process crash between the two
stores is not an atomic transaction; reconnect to repair an incomplete save.
A hostile process already running as the same OS user is outside the local
browser isolation guarantee.

## Data boundaries

- Mail content travels directly between the local MCP process and Apple's
  documented IMAP/SMTP hosts over TLS.
- Credentials are never accepted as tool parameters or returned in results.
- Configuration files contain no password or token, use user-only permissions,
  reject file symlinks and unknown fields, and are replaced atomically.
- Outgoing `From` addresses must match the account address or an explicitly
  configured alias and are revalidated immediately before SMTP submission.
- No plugin-managed email repository, search index, message/attachment cache,
  background synchronization, or content-bearing temporary files are created.
  Mail is processed on demand in bounded memory; diagnostics do not contain mail
  content. Only settings, a non-secret lock file and Keychain credentials persist.
- Requested mail returned through MCP enters Codex's conversation/model handling.
  The plugin does not control that retention or operating-system swap.
- Logs and errors exclude authentication material.
- Attachment reads are capped at 5 MiB of decoded data.
- Full-message downloads are rejected above a 20 MiB MIME processing limit.
- Tool results cap message bodies and result counts.
- Outgoing local-file attachments require explicit absolute paths, reject
  symbolic links, and are capped at 5 MiB each and 10 MiB total.
- No tool permanently expunges mail. Trash is recoverable through iCloud Mail.
- Setup accepts credentials only in its local browser form, never MCP arguments.
  Other GUI helpers only open Apple Account or Keychain Access and do not inspect
  browser state or automate credential entry.
- Clearing configuration removes settings but leaves Keychain items and Apple's
  authorization intact. Local item removal and Apple password revocation are
  separate user actions.

## Reporting

Do not include credentials, mailbox content, or personal addresses in a public
issue. Report security concerns through the repository's private
[security-advisory form](https://github.com/sealad886/sealad886-codex-marketplace/security/advisories/new).

Production Keychain reads run in a short-lived helper using the same native API.
A private pipe returns the credential to the MCP process; no password is passed
in arguments or environment. Reads are capped at ten seconds and the remaining
operation deadline. Timeout kills and reaps the helper so an unanswered Keychain
prompt cannot indefinitely block the MCP loop.
