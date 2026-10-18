# Repository Consolidation

Version **0.1.0**. One standalone skill for accounting for scattered Git work
and integrating authorized changes through focused reviewed PRs in series.

The [skill](skills/repo-consolidation/SKILL.md) inventories local and advertised
remote branches, every worktree, stashes, dirty/default-branch changes, and
relevant ignored artifacts. It maps each original source to an explicit
integration or preservation decision, finishes included work, verifies destination
coverage, and removes only eligible sources. Fewer branches alone is not success.

## Install and use

In a Codex client supporting marketplace plugins:

```sh
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add repo-consolidation@sealad886-codex-marketplace
```

Start a fresh task after installation. A root Agent Plugins 1.0 manifest is also
included for portable clients discovering the `skills/` directory.

Example requests:

- "Use $repo-consolidation:repo-consolidation to inventory this repository without changing it."
- "Plan how to consolidate these sources; do not commit, push, or merge."
- "Consolidate this identified repository through focused commits, serial
  reviewed PRs, gated merges, and eligible cleanup. Preserve the named branches."

Explicit execution authorizes the bounded task lifecycle in the skill. Inventory,
plan-only, no-push, no-merge, and named exclusions narrow it. Reading, installing,
quoting, or automatically loading this package grants no action. New worktrees,
data disposal, destructive Git recovery, settings changes, release/publication,
deployment, and unrelated repositories remain outside consolidation authority.

## Requirements and included references

Needs Git, project validation tools, and supported authenticated provider
capabilities for execution. Independent review must be available for integration.
Inventory can expose honest offline/access limits. This plugin is independently
usable; it contains its own selective commit and PR review procedures, without
requiring the Conventional Commit or Iterating PR Bot Fixes plugins.

- [Complete Git inventory and comparison](skills/repo-consolidation/references/git-inventory.md)
- [Selective commit safety](skills/repo-consolidation/references/selective-commits.md)
- [Serial review and integration](skills/repo-consolidation/references/serial-review.md)
- [Review sources and Copilot policy](skills/repo-consolidation/references/review-sources.md)
- [Wider source cleanup](skills/repo-consolidation/references/cleanup.md)
- [Consolidation ledger](skills/repo-consolidation/templates/consolidation-ledger.md)
- [Per-PR review ledger](skills/repo-consolidation/templates/review-ledger.md)

The serial protocol retains ten-round default review, explicit outcomes,
root-cause/scope investigation, clean-source retirement, attributable Copilot
unavailability, a separate final-head independent gate, and repository approval/
CI/queue requirements. Three coverage passes establish original-source mapping,
combined behavior, and actual destination/residual state. Secured backups and
uncertain work remain preserved.

## Maintainer validation

From a checkout of the
[marketplace repository](https://github.com/sealad886/sealad886-codex-marketplace),
use its [source checker](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/scripts/check_plugin.py)
and [distribution checker](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/scripts/check_distribution_bundle.py):

```sh
python3 scripts/check_plugin.py plugins/repo-consolidation --layout source
python3 scripts/check_distribution_bundle.py plugins/repo-consolidation
```

Validate JSON/YAML, contained links/artwork, exactly one skill, dual-manifest
parity, and fresh-client discovery. Package checks do not prove runtime agent
behavior, complete access to an arbitrary repository, safe deletion decisions,
provider integration, or desktop rendering. See [security boundaries](SECURITY.md)
and [MIT license](LICENSE).
