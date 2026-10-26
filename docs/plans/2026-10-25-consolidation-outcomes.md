# Repository Consolidation 0.3.0 implementation and delivery plan

Approved scope: [outcome reconciliation design](../specs/2026-10-25-consolidation-outcomes-design.md).
Use the existing task branch and checkout; no new worktree or actual repository
consolidation is part of authoring this plugin.

## 1. Implement the coherent workflow

- Files: `plugins/repo-consolidation/skills/repo-consolidation/SKILL.md`,
  `references/overlap-and-dependencies.md`, `references/cleanup.md`,
  `templates/consolidation-ledger.md` beneath that skill, and package `SECURITY.md`.
  Make accepted outcomes and canonical ownership drive integration. Include
  source/residue pruning in each candidate; distinguish it from source retirement
  and unique-content disposal. Preserve existing review/authority checks.
- Files: package `plugin.json`, `.codex-plugin/plugin.json`, `README.md`, skill
  `agents/openai.yaml`, root `README.md`, `CHANGELOG.md`. Synchronize 0.3.0 and
  describe the updated goal and prompts. Keep the catalog-local package source,
  one skill, and local/cloud eligibility. No dependencies or executable changes.
- Dependencies: approved design and clean dedicated branch. Risk: medium because
  source-pruning instructions must not become unrestricted data/Git deletion.

## 2. Verify and review the candidate

- Files: the changed package, catalog, and task evidence outside source.
  Run existing source/distribution/marketplace and pinned upstream validators,
  validate the changed skill, and inspect exact archive closure. Obtain separate
  specification and quality/authority reviews against all seven design scenarios.
- No prose-pinning tests: documentation changes introduce no new processing code.
  Required hosted regression and security scan workflows exercise the exact PR.
- Dependencies: step 1. Risk: low for packaging, medium for behavioral guidance.
  Distinguish scenario review, native host discovery and actual repository use.

## 3. Publish and prove default installation

- Files/targets: focused PR to current `main`, immutable signed
  `repo-consolidation-v0.3.0`, validated ZIP, GitHub release, automatic marketplace
  snapshot, and isolated/current Codex installations. Follow established release
  workflows; verify current-head reviews and checks before conditional merge.
- Confirm merge source equals the validated candidate, tag/asset identity and
  digests, successful publication jobs, and GitHub Latest snapshot. Register the
  marketplace without an explicit ref in a fresh Codex home and verify pre-install
  metadata, one skill, installed 0.3.0, and exact package parity. Also confirm the
  published snapshot resolves that package. Refresh only the local target plugin.
- Dependencies: step 2 and hosted merge gates. Risk: medium for externally visible
  publication. User has authorized the PR/release/default-install delivery. Keep
  branches and unrelated state; no branch deletion or private account update.

## Acceptance

The seven design scenarios have no unresolved in-scope contradiction. Source,
distribution, manifest and changed-skill checks pass. Exact-head independent and
hosted review/check gates pass. The published plugin and default marketplace
installation both contain 0.3.0, with verified source/archive/cache identity.
Report unrun cloud/repository-wide behavioral acceptance separately.
