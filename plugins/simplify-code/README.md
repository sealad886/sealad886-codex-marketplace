# Simplify Code

Version: **0.2.0**. One skill for removing unnecessary layers and obsolete source,
centralizing shared rules, and making required behavior easier to understand.

[The simplify-code skill](skills/simplify-code/SKILL.md) traces ownership through
callers, checks public and dynamic entrypoints, refactors coherent slices, and
uses proportionate behavioral checks. Fewer concepts matter more than line-count
or call-depth targets.

## Use

```bash
codex plugin add simplify-code@sealad886-codex-marketplace
```

Example requests:

- "Simplify this module: remove redundant forwarding layers and migrate their callers."
- "Deduplicate the repeated validation rule in this feature without merging
  caller-specific policy."
- "Review this change for unnecessary complexity; propose improvements without editing."
- "Use $simplify-code:simplify-code to simplify these interacting flags while
  preserving cancellation, cleanup, and the accepted state transitions."
- "Use $simplify-code:simplify-code to move the proven callers to this canonical
  API, preview the migration cohort, and report any uncertain dynamic consumers."

Provide the target and required behavior. An implementation request includes
verified obsolete-source deletion within that scope; a review request stays
read-only. Public/framework entrypoints and resource/cancellation boundaries are
retained when they serve a concrete requirement.

The package needs host access to relevant source, repository search, and its
existing validation workflow. It includes no automatic rewrite engine, server,
runtime dependency, or required sibling plugin. Available code intelligence is
optional. See [boundary checks](skills/simplify-code/references/refactoring-checks.md),
[worked examples](skills/simplify-code/references/worked-examples.md), and
[security and authority boundaries](SECURITY.md).

For state-heavy code, the [state/control-flow guide](skills/simplify-code/references/state-and-control-flow.md)
uses reachable states and evaluation order to distinguish redundant state from
necessary lifecycle information. The [migration guide](skills/simplify-code/references/mechanical-migrations.md)
defines eligible callers, previews representative changes, and verifies the
remaining consumers and repeat-run behavior. An optional
[refactor evidence sheet](skills/simplify-code/templates/refactor-evidence.md)
keeps multi-slice work resumable. These workflows use the tools available in a
local or cloud task; no rewrite engine or new runtime is bundled.

## Package validation

Portable and Codex manifests share identity/version/presentation; one skill and
its local support files form the runtime payload. Maintainers follow the current
[contribution and validation guide](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/CONTRIBUTING.md)
for source/skill checks, distribution closure, native discovery, and installed
parity. Packaging checks do not prove a particular refactor's behavior.

This skill grants no additional commit, worktree, history-rewrite, publication,
data-migration, or deployment authority. Performance improvements require measurement.
