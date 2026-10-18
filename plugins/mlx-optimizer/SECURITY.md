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

The audit reads source without importing the inspected project. Reads are limited
to regular files up to 2 MiB, with symlink files and directory components below
the selected scan root rejected. A symlink supplied directly as the target is
also rejected. Explicit parent-path aliases such as macOS /var remain usable.
Oversized, linked, non-regular, and unreadable sources become read-error findings.

The environment probe executes the user-selected Python interpreter and imports
its installed MLX package. That interpreter and its installed packages must be
trusted. Child isolated mode excludes the caller's working directory,
PYTHONPATH, and user site packages; it retains the selected virtual environment
and uses the plugin script directory as its working directory. It is not an
execution sandbox for a malicious interpreter or installed package. The benchmark
template likewise executes code and must run only in a trusted environment.

The helpers do not modify target repositories. If a script can be made to write outside
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
