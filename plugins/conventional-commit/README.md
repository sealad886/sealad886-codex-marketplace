# Conventional Commit

Version **0.1.0**. One standalone skill for inspecting dirty Git work, selecting
coherent changes, and creating verified local Conventional Commits while
preserving excluded bytes and staging.

The [skill](skills/conventional-commit/SKILL.md) accounts for staged, unstaged,
untracked, binary, renamed, and generated content. It prevents unrelated
pre-staged work from entering a plain commit, distinguishes path-only commits
from mixed-hunk selection, respects hooks/signing, and reads back actual results.
No push, PR, merge, release, or worktree creation follows from a local commit
request.

## Install and use

In a Codex client supporting marketplace plugins:

```sh
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add conventional-commit@sealad886-codex-marketplace
```

Start a fresh task after installation. The root Agent Plugins 1.0 manifest also
supports clients that discover portable skills from `skills/`.

Example requests:

- "Use $conventional-commit:conventional-commit to commit my changes to this feature, preserving
  unrelated staged and unstaged work."
- "Propose logical Conventional Commit groups without staging or committing."
- "Use $conventional-commit:conventional-commit --clean to commit the requested scope and discard
  only inspected unnecessary exclusions covered by that cleanup request."

Cleanup is off unless `--clean` is the first non-skill token immediately after
the human's direct invocation. A later occurrence, quoted example, plugin
description, or automatic loading does not enable it. Even valid cleanup
preserves ambiguous ownership, valuable work, ignored data, and content outside
the requested scope. A plan-only request remains read-only.

## Requirements and included references

Needs a Git repository and the project's existing validation environment. No
Python/runtime dependency, MCP server, external service, or companion plugin is
required. Hooks and signing can require normal human credential interaction;
the workflow does not disable them or alter global Git configuration.

- [Inventory, staging, hooks, and failures](skills/conventional-commit/references/staging-and-hooks.md)
- [Exact cleanup semantics](skills/conventional-commit/references/cleanup.md)
- [Commit plan and receipt](skills/conventional-commit/templates/commit-plan.md)

Mixed files need a proven staging procedure that preserves excluded index and
working content; the package refuses to improvise unsafe index recovery. Git
commands and suggestions are checked against installed capabilities and current
[Git documentation](https://git-scm.com/docs). Messages follow
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Maintainer validation

From a checkout of the
[marketplace repository](https://github.com/sealad886/sealad886-codex-marketplace),
use its [source checker](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/scripts/check_plugin.py)
and [distribution checker](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/scripts/check_distribution_bundle.py):

```sh
python3 scripts/check_plugin.py plugins/conventional-commit --layout source
python3 scripts/check_distribution_bundle.py plugins/conventional-commit
```

Check JSON/YAML, contained links/artwork, exactly one skill, manifest identity/
presentation parity, and fresh-client discovery. Static package validation does
not prove agent execution, commit isolation, signing, or native visual rendering.
See [security boundaries](SECURITY.md) and [MIT license](LICENSE).
