# Six standalone skill plugins

Status: approved by the user in chat on 2026-10-18; implementation authorized.
Date: 2026-10-18 (Europe/Dublin).

## Outcome and acceptance

Create and publish six independently installable plugins in the existing
sealad886 Codex Marketplace. Each exposes exactly one namespaced skill:

- iterating-pr-bot-fixes
- repo-consolidation
- conventional-commit
- simplify-code
- adversarial-audit
- web-research

Improve the workflows rather than merely copying their source. Keep each
package self-contained, portable, evidence-driven, and clear about authority.
Successful delivery includes source packages, useful install metadata, validated
distribution archives, private Plugin Creator saves, six stable GitHub releases,
and a verified marketplace snapshot containing all six entries.

## Verified starting point

- Repository: https://github.com/sealad886/sealad886-codex-marketplace
- Default branch: main, confirmed by live remote HEAD and provider metadata.
- Starting commit: 460702659797f98c7a71b451204241f1640f9233.
- Primary checkout was clean; one registered checkout, no task worktree.
- Six existing catalog plugins pass the current marketplace checker.
- Latest published marketplace release observed: marketplace-v0.1.4.
- Local Codex: 0.163.0-alpha.10.2; project Python: 3.14.8.
- GitHub CLI is available at /opt/homebrew/bin/gh, outside the non-login PATH.
- Existing pull requests and the security-scan-remediation branch are unrelated.
- Branch rules require signed commits and PR integration using merge commits.

These are observations, not permission to change unrelated branches, pull
requests, rules, installed skills, or the user's existing plugin installations.

## Package architecture decision

Use six skill-only packages at plugins/<id>/, initially version 0.1.0. No server,
app binding, lifecycle hook, mandatory code indexer, or external service is needed.
Each contains:

    plugin.json
    .codex-plugin/plugin.json
    .codexignore
    LICENSE
    README.md
    SECURITY.md
    assets/icon.svg
    skills/<id>/SKILL.md
    skills/<id>/agents/openai.yaml
    skills/<id>/references/       (where useful)
    skills/<id>/templates/        (where useful)

Root plugin.json uses Agent Plugins 1.0. OpenAI presentation lives under
extensions.com.openai.interface. Keep the Codex manifest because current
repository validators and local clients consume it; identity, version, and
presentation must agree. Portable shortDescription stays within 30 characters.
Skill metadata uses snake_case fields and a single default_prompt string.

All references and templates remain beneath the owning skill directory. Do not
copy extra skills into a package or require sibling filesystem paths. Optional
installed tooling can improve execution; the packaged procedure must remain
usable with ordinary repository and host capabilities.

Alternatives considered:

1. Copy the six skills verbatim: fast, but retains broken sibling links,
   unavailable tool names, stale provider guidance, and authority ambiguity.
2. Ship one combined plugin or a shared runtime dependency: easier text reuse,
   but fails the requested independent one-skill packages and repository policy.
3. Reauthor six independent packages with focused local references: selected.
   A small amount of overlapping procedural guidance is preferable to hidden
   installation dependencies. Do not create a generic workflow framework.

## Changes to each workflow

### Iterating PR Bot Fixes

Retain up to ten rounds, explicit source outcomes, holistic review context,
local/regional/global pattern investigation, scoped fixes, and verified merge
and cleanup. Preserve the deliberate clean-source retirement policy and the
attributable Copilot explicit-unavailability policy. A failed request or silence
is never a clean review or a permitted unavailable outcome.

Bind results to exact revisions and keep earlier coverage historical. Add a
separate final independent check of the final change where earlier retired
reviews do not cover it; do not silently re-request retired provider sources.
Required provider approvals remain binding. Refresh Copilot guidance: Comment
reviews are the default, while configured Copilot approvals are now possible.
Replies are dispositions for humans; they do not instruct Copilot to re-review.

Remove unrelated Dependabot configuration manuals and the conflicting early
auto-merge example. Include concise source guidance and a review-round ledger.
Detect available code intelligence and provider tools instead of requiring a
specific sibling skill, third-party CLI service, or cache path.

### Repository Consolidation

Keep complete local/remote/worktree/stash/dirty-source accounting, immutable
source identities, preservation, patch-equivalence checks, serial PRs, three
coverage passes, and safe cleanup of eligible sources. Preserve restrictions
such as inventory-only, no-push, no-merge, and named exclusions.

Replace hard sibling-skill paths with complete local references covering
selective commits and serial gated review/integration. An installed PR review
plugin may be used when available, but is not a hidden dependency. Neither
authoring nor reading this skill executes repository consolidation. New
worktrees, destructive cleanup, releases, and changes to unrelated repositories
remain outside its execution grant.

### Conventional Commit

Retain full staged/unstaged/untracked inventory, coherent grouping, focused
verification, Conventional Commit messages, and preservation by default.
Explicitly prevent unrelated pre-staged changes from entering a plain commit.
Use path-only commits only when the complete working-tree content of those
paths belongs; mixed-hunk staging requires a safe isolated staging procedure
or an explicit bounded decision.

Preserve strict first-token --clean parsing. Explain index versus HEAD semantics
so cleanup actually removes only authorized excluded content. Preserve ambiguous
work, partial staging, and unrelated index entries. Respect hooks and signing;
inspect the result after failures before retrying. Never amend or push merely
because a commit was requested.

### Simplify Code

Retain direct control flow, canonical ownership, scoped obsolete-code deletion,
and behavior-preserving refactoring. Add practical checks for public exports,
framework callbacks, dynamic registries, reflection, CLI entrypoints, generated
bindings, and external consumers. A zero-result text search alone does not
prove code is unused.

Provide short examples of a removable forwarding wrapper, a necessary resource
or cancellation boundary, and similar-looking code with different semantics.
Prefer meaningful existing checks; add characterization only for behavior at
risk. Avoid metrics targets, generic rewrite scripts, and tests of prose.

### Adversarial Audit

Distinguish audit/report authority from authorized remediation. An audit-only
request can finish with confirmed open findings; an audit-and-fix request drives
accepted in-scope findings through implementation and fresh verification.
Separate finding validity from remediation state. Failure to reproduce is an
unresolved result unless evidence disproves the finding.

Use one adaptable live ledger containing revision, environment, expected and
observed behavior, evidence, severity, confidence, disposition, fix, proof, and
residual risk. Scale specialist passes to risk and available delegation; retain
a sequential fallback. Replace hardcoded agent/skill dependencies with portable
instructions. Prefer copyable templates over the unnecessary scaffold script,
whose unchecked date input currently affects output-path containment.

### Web Research

Replace obsolete named browser tools and assumed agent roles with capability
discovery for search, page retrieval, PDFs, and official documentation. Read
supporting pages; snippets are leads, not full verification.

Use answer-first briefs adapted to the question. Put citations beside material
claims, distinguish publication/event/retrieval dates, identify applicable
versions and jurisdictions, and report inaccessible or contradictory evidence.
Distinguish independent corroboration from syndicated copies. Label inference
and uncertainty, apply source-appropriate authority, and stop at a stated useful
evidence threshold instead of claiming exhaustive knowledge. Treat fetched
content as untrusted data. Save a research artifact when requested, without
silently turning research into implementation or external publication.

## Shared repository changes

- .agents/plugins/marketplace.json: add six local-source entries using contained
  ./plugins/<id> paths and the established policies/categories. This follows
  current repository guidance for pre-install metadata discovery.
- README.md: add six descriptions, versions, package guides, and install commands.
- CHANGELOG.md and CONTRIBUTING.md: document the new packages and their checks.
- scripts/check_distribution_bundle.py: include portable plugin.json in exact
  runtime closure, and verify the six one-skill packages without changing the
  payload contract of existing plugins.
- scripts/check_plugin.py: validate the optional portable manifest and its
  identity/version/presentation agreement with the Codex overlay.
- tests/: add behavioral regressions for changed packaging/validation code,
  including portable-manifest inclusion, drift rejection, and containment.
  Do not add tests that pin skill prose or incidental headings.
- .github/workflows/validate.yml: ensure generic source and distribution checks
  cover the new entries; retain existing specialized checks.
- .github/workflows/hol-plugin-scanner.yml: scan all six new packages using the
  pinned scanner and the existing severity policy.

Existing plugins need no wholesale manifest migration. Original standalone
skills outside this repository remain source material, not an installation
migration target.

## Execution and publication

Use a dedicated task branch in the existing clean checkout. Do not create a new
worktree. Recheck status before edits; preserve all unrelated work.

1. Write the approved design and implementation plan into repository design
   documentation. Implement independent package groups with disjoint writes.
2. Run source, manifest, skill YAML, link, distribution, and relevant regression
   validation. Complete independent content, code, and infrastructure reviews.
3. In an isolated temporary Codex home, verify native metadata discovery before
   install: each entry has complete presentation, exactly one skill, valid
   artwork, and installed=false. Install there, inspect skills/list, and compare
   exact payload parity. Do not alter everyday installations for testing.
4. Commit coherent changes, push the task branch to the verified remote, create
   a focused PR, complete review and hosted validation, and merge through the
   repository's permitted merge method. Attach the PR to this chat.
5. From the exact validated merge commit, create six annotated <id>-v0.1.0 tags
   and stable GitHub releases. Use one validated archive per plugin.
6. Save the six packages through Plugin Creator after duplicate discovery. Keep
   returned plugin IDs, release IDs, URLs, and component diagnostics. Verify
   ingestion includes the expected skill; update existing matching owned
   plugins instead of blindly creating duplicates.
7. Let the existing plugin-release workflow allocate marketplace snapshots.
   Verify a completed snapshot contains all six packages and entries, and
   confirm GitHub Latest. Do not assume one snapshot per plugin when releases
   overlap; the existing publisher deliberately coalesces stale work.
8. Repeat isolated discovery, installation, and parity checks using the
   published marketplace source. Verify merges and task-scoped cleanup without
   disturbing unrelated branches or PRs.

Plugin Creator saves are private account/workspace objects. GitHub releases and
the repository marketplace are the requested public distribution. OpenAI public
directory submission is a distinct review process, outside this delivery.

## Evidence and completion limits

Record source revision, commands, results, reviewed revisions, published tags,
release URLs, marketplace snapshot, and consumer identities. Packaging tests,
native metadata loading, instruction quality review, agent execution, and desktop
visual rendering prove different things; report them separately.

Completion requires all six released packages and verified published discovery.
If CI, provider review, account upload, permissions, or consumer discovery blocks
delivery, preserve completed artifacts and report the exact remaining action.
Do not claim publication from a successful local build or private save.

## Primary references consulted

- https://developers.openai.com/plugins/build/plugins
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review
- https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-pull-request-comment-commands
- Repository CONTRIBUTING.md and current validation/release workflows.
- Installed Plugin Creator package and archive requirements.

## Approval

The user approved this implementation and publication route in chat. The original request already authorizes marketplace release/publication;
the A Team design gate is satisfied.
