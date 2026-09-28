# iCloud Mail security

## Supported authentication

Use an Apple app-specific password, never the primary Apple Account password.
The Apple Account must have two-factor authentication enabled. The server reads
the mailbox identity from the saved `configure_account` `account_address`.
`ICLOUD_MAIL_USERNAME` is a legacy fallback only when no saved configuration
exists. The server obtains the app-specific password from
`ICLOUD_MAIL_APP_PASSWORD` or, on macOS, a Keychain item named
`codex-icloud-mail`.

Non-secret account settings are stored outside the plugin cache in a user-only
configuration file. The account address authenticates the mailbox. Optional
aliases are outgoing identities only; incoming IMAP automatically includes
mail delivered to every alias in the mailbox.

The plugin does not implement Apple's newer third-party account authorization.
Apple documents that experience for supported apps, but does not publish a
general client-registration and token protocol that this local plugin can use.

## Data boundaries

- Mail content travels directly between the local MCP process and Apple's
  documented IMAP/SMTP hosts over TLS.
- Credentials are never accepted as tool parameters or returned in results.
- Configuration files contain no password or token, use user-only permissions,
  reject file symlinks and unknown fields, and are replaced atomically.
- Outgoing `From` addresses must match the account address or an explicitly
  configured alias and are revalidated immediately before SMTP submission.
- Logs and errors redact authentication material.
- Attachment reads are capped at 5 MiB of decoded data.
- Full-message downloads are rejected above a 20 MiB MIME processing limit.
- Tool results cap message bodies and result counts.
- Outgoing local-file attachments require explicit absolute paths, reject
  symbolic links, and are capped at 5 MiB each and 10 MiB total.
- No tool permanently expunges mail. Trash is recoverable through iCloud Mail.
- GUI helper tools only open Apple Account or Keychain Access. They do not
  inspect browser state, read credential fields, or automate password entry.
  Their child process environment explicitly omits `ICLOUD_MAIL_APP_PASSWORD`.

## Reporting

Do not include credentials, mailbox content, or personal addresses in a public
issue. Report security concerns through the repository's private
[security-advisory form](https://github.com/sealad886/sealad886-codex-marketplace/security/advisories/new).
