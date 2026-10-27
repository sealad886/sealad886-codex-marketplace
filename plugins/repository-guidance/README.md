# Repository Guidance

Version: **0.1.0**. Create, adapt, and audit coding-agent instructions using the
repository’s actual architecture, commands, tests, and delivery policies.

The [repository-guidance skill](skills/repository-guidance/SKILL.md) turns useful
engineering conventions into evidence-backed local rules. It maps each relevant
candidate to **adopt**, **adapt**, **not applicable**, **conflict**, or **unknown**;
then produces the requested audit, draft, or focused instruction-file patch.

## Install and use

Register this marketplace and install the plugin with your client:

```bash
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add repository-guidance@sealad886-codex-marketplace
```

```bash
copilot plugin marketplace add sealad886/sealad886-codex-marketplace
copilot plugin install repository-guidance@sealad886-codex-marketplace
```

Start a fresh task after installation. In Codex, invoke
`$repository-guidance:repository-guidance`. In Copilot, ask it to use the
`repository-guidance` skill; client invocation surfaces can differ.

Example requests:

- “Use repository-guidance to audit this repo’s AGENTS.md. Report stale commands,
  unsupported rules, and ownership gaps without editing files.”
- “Use repository-guidance to adapt the Multica-inspired engineering conventions
  to this repository and update its existing AGENTS.md.”
- “Draft instructions for this package from its code, CI, and contribution guide.
  Keep the root policy authoritative and explain unresolved decisions.”

An audit or draft request does not authorize file edits. An instruction-edit
request allows the scoped local patch; it does not itself authorize commits,
installation, external writes, or release. Existing user and repository authority
continues to apply. Substantial authorized replacements retain a local backup.

## How adaptation works

Inspect the target’s applicable instructions and current repository state, locate
its real owners and command sources, and evaluate only relevant concerns. Keep
shared rules with their canonical owner and scoped rules with their package or
platform. Verify referenced paths and commands; state when a command was only
inspected rather than executed. Report missing evidence instead of inventing rules.

The [adaptation lenses](skills/repository-guidance/references/adaptation-lenses.md)
include a worked mapping for this marketplace’s package boundaries, paired
manifests, canonical/generated catalogs, Python environment, both client checks,
and publishing authority. The optional
[adaptation record](skills/repository-guidance/templates/adaptation-record.md)
can be replaced by an existing project format or a concise response.

## Sources and limits

This original synthesis was informed by
[Multica’s AGENTS.md at d7d1831](https://github.com/multica-ai/multica/blob/d7d1831fcf39b874911aae1e48b2fbf804bd068e/AGENTS.md).
See [source provenance](skills/repository-guidance/references/source-provenance.md)
for the inspected revision, research date, license distinction, and excluded
project-specific assumptions. No upstream source text, runtime, branding, or
assets are included; this plugin has no Multica affiliation or endorsement.

The package contains one shared skill for Codex and GitHub Copilot. It includes
no MCP server, network client, credentials, shell runtime, or required sibling
plugin. The host supplies repository-reading/editing tools and enforces approvals.
Browsing is optional unless the task requests current external-source verification.
A valid package does not prove that every target host automatically loads
AGENTS.md or that future agents follow it. See [security boundaries](SECURITY.md).

## Maintainer validation

From the marketplace checkout, use its existing Python environment:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_plugin.py plugins/repository-guidance --layout source
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_distribution_bundle.py plugins/repository-guidance
```

Follow the current [marketplace contribution guide](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/CONTRIBUTING.md)
for both catalog checks, skill validation, isolated native client discovery and
installation, installed-file parity, and release scanning. Documentation and
package checks establish structural validity; evaluate the actual adaptation’s
claims against the target repository before accepting its guidance.
