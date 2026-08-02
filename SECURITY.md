# Security policy

## Supported versions

Security fixes are made on the latest published release. Older versions may be assessed when a report shows that they are affected, but users should expect to upgrade to receive a fix.

## Reporting a vulnerability

Please use [GitHub private vulnerability reporting](https://github.com/sealad886/sealad886-codex-marketplace/security/advisories/new). Do not open a public issue for a suspected vulnerability or include credentials, personal data, private repository content, or exploit details in public discussion.

Include, when safely available:

- the affected version or commit;
- the skill, script, or workflow involved;
- prerequisites and a minimal reproduction;
- the security impact and likely affected users;
- any known mitigation; and
- whether disclosure is time-sensitive.

You should receive an acknowledgement within seven days. Assessment, remediation, release, and coordinated disclosure timing depend on severity, reproducibility, and user impact. No reporter is asked to run intrusive tests against systems they do not own or have explicit permission to test.

## Scope

The marketplace catalog and each installed plugin have separate package boundaries. Repository-only CI, tests, audit evidence, and maintainer validation tools stay outside installed plugin payloads.

- Project Delivery contains instructions, templates, and icons. It does not
  bundle an MCP server, app, hook, telemetry, credentials, executable
  validation code, or network service.
- Conversation Visuals includes a local MCP process but does not read local
  files or credentials or contact network providers. Its detailed boundary is
  documented in [its package security policy](plugins/conversation-visuals/SECURITY.md).
- iCloud Mail includes a local MCP process that connects directly to Apple's
  fixed IMAP and SMTP endpoints, reads and mutates mailbox data, reads selected
  local attachment files for outgoing messages, and retrieves an app-specific
  password from macOS Keychain or the launching environment. It must never use
  the primary Apple Account password. Its detailed credential, content,
  attachment, and mutation boundary is documented in [its package security
  policy](plugins/icloud-mail/SECURITY.md).

Reports about an optional third-party connector, platform tool, repository, or
provider should normally go to that component's owner unless this marketplace
or one of its plugins creates the unsafe behavior.
