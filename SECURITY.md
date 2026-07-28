# Security policy

## Supported versions

Security fixes are made on the latest published release. Older versions may be assessed when a report shows that they are affected, but users should expect to upgrade to receive a fix.

## Reporting a vulnerability

Please use [GitHub private vulnerability reporting](https://github.com/sealad886/andrew-cox-codex-marketplace/security/advisories/new). Do not open a public issue for a suspected vulnerability or include credentials, personal data, private repository content, or exploit details in public discussion.

Include, when safely available:

- the affected version or commit;
- the skill, script, or workflow involved;
- prerequisites and a minimal reproduction;
- the security impact and likely affected users;
- any known mitigation; and
- whether disclosure is time-sensitive.

You should receive an acknowledgement within seven days. Assessment, remediation, release, and coordinated disclosure timing depend on severity, reproducibility, and user impact. No reporter is asked to run intrusive tests against systems they do not own or have explicit permission to test.

## Scope

The marketplace catalog and each installed plugin have separate package boundaries. The current Project Delivery package contains instructions, templates, and icons; repository-only maintainer tooling includes standard-library validation scripts outside that installed package. Project Delivery does not bundle an MCP server, app, hook, telemetry, credentials, executable validation code, or a network service. Reports about an optional third-party connector, platform tool, repository, or provider should normally go to that component's owner unless this marketplace or one of its plugins creates the unsafe behavior.
