# Security Policy

## Supported Versions

This plugin follows latest-release support. Security fixes target the current
released version unless a maintainer explicitly announces wider support.

| Version | Supported |
| --- | --- |
| latest | yes |
| older releases | no |

## Reporting a Vulnerability

Please report security vulnerabilities through GitHub Security Advisories. Do
not report vulnerabilities through public GitHub issues.

To report:

1. Open the repository's **Security** tab on GitHub.
2. Choose **Advisories**.
3. Create a new draft security advisory.
4. Include enough detail for maintainers to reproduce and assess the issue.

Useful details include:

- Affected file paths, manifest paths, scripts, or skill files.
- The affected tag, branch, or commit.
- Steps to reproduce.
- Expected and actual behavior.
- Proof of concept, when safe to share privately.
- Impact assessment for plugin installation, agent behavior, or generated
  recommendations.

## Scope

This package contains plugin metadata, Markdown skill instructions, reference
material, and local Python helper scripts. Security-relevant areas include:

- Plugin manifests and marketplace metadata.
- Scripts that inspect target repositories.
- Guidance that could cause unsafe agent behavior in downstream repos.
- CI and repository automation.

The audit and probe scripts are designed to inspect files and environments
without modifying target repositories. If a script can be made to write outside
its intended output path, execute unexpected code, or leak sensitive local
information, report it privately.

## Response Timeline

- Initial acknowledgement: within 48 hours when possible.
- Initial assessment: within 7 days when possible.
- Fix and disclosure timing: based on severity, exploitability, and release
  readiness.

## Attribution

Responsible disclosure is appreciated. With permission, reporters may be
credited in the advisory or release notes.
