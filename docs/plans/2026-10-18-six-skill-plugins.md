# Six skill plugins: implementation plan

Approved design: [six skill plugins](../specs/2026-10-18-six-skill-plugins-design.md).
User approved building, reviewing and publishing the design on 2026-10-18.

## Checklist

- [x] Build six packages and packaging validation.
- [x] Validate source/distributions, native discovery and isolated installation; review.
- [ ] Active: commit, integrate through a reviewed PR, publish six releases (Creator saves verified).
- [ ] Verify published marketplace snapshot and consumer parity; complete handoff.

## Work units

1. **Git workflow packages** (low risk; no runtime code). Create
   `plugins/iterating-pr-bot-fixes/`, `plugins/repo-consolidation/`, and
   `plugins/conventional-commit/` with exactly one skill each, package-local
   references/templates, root portable and Codex manifests, display metadata,
   original SVG icons, license, README, security boundary and ignore file.
   Follow the approved changes, preserve deliberate review policies, and make
   selective staging safe around an existing index. No sibling dependencies.
2. **Audit, simplification and research packages** (low risk; no runtime code).
   Create `plugins/adversarial-audit/`, `plugins/simplify-code/`, and
   `plugins/web-research/` using the same package contract. Remove hardcoded
   agent/tool requirements, distinguish authority from relevance, and retain
   meaningful evidence and uncertainty. Prefer templates over scaffold scripts.
3. **Packaging behavior** (medium risk; independent of content). Update
   `scripts/check_plugin.py` and `scripts/check_distribution_bundle.py` to retain
   optional portable manifests and reject mismatched identity/version/interface
   or escaping artwork. Add focused failing tests first in
   `tests/test_validation.py` and `tests/test_distribution_bundle.py`, then
   implement. Keep existing packages valid and existing source-boundary defenses.
4. **Catalog, CI and docs** (low risk; depends on final package identities).
   Update `.agents/plugins/marketplace.json`, `README.md`, `CHANGELOG.md`,
   `CONTRIBUTING.md`, `.github/workflows/validate.yml`, and
   `.github/workflows/hol-plugin-scanner.yml`. Add six local entries and generic
   checks plus a pinned-scanner matrix without redesigning existing jobs.

## Verification and review

- Use the existing project `.venv`; no dependency installation planned.
- Run source, distribution, marketplace, Skill Creator and Plugin Creator
  validation; inspect exact one-plugin archives and local links/metadata.
- Exercise changed validator behavior through focused synthetic fixtures and
  the existing full repository suite. Do not add prose-pinning skill tests.
- Test in an isolated temporary Codex home: discovery before install,
  installed skills/interface metadata, and exact source/cache parity. Repeat
  using the published marketplace after release.
- Perform separate spec and quality review; include Python and infrastructure
  review for changed validator/CI files. Fix all in-scope blockers and rerun
  affected checks before commits and integration.
- Baseline already verified: 578 tests, four skips, with process-only test Git
  signing disabled and loopback tests outside the sandbox. Real commits remain
  signed; no Git configuration changes are authorized or needed.

## Integration and publication

Use `codex/six-skill-plugins` in the existing checkout; no new worktree.
Create focused signed Conventional Commits. Push the verified task branch,
open/attach a focused PR, complete independent review and hosted validation,
and merge with the repository-supported merge method bound to current head.

Create six annotated `<plugin>-v0.1.0` tags from the exact validated merge
commit, publish six stable GitHub releases with inspected package archives, and
let existing automation allocate the marketplace snapshot. Verify source SHAs,
release states, snapshot contents, GitHub Latest and published consumer parity.
Discover matching account plugins before six Plugin Creator saves; retain IDs,
URLs and ingestion diagnostics. These private saves are separate from GitHub
marketplace publication and do not submit to the OpenAI public directory.

## Recovery and handoff

Preserve unrelated branches, PRs, dirty work and current daily installations.
Stop a dependent publication step on failed review, validation, identity or
discovery; preserve successful artifacts and record the exact blocker. Never
move an existing release tag. After verified merge, remove only eligible task
branches and report any preserved work. Record actual verification and release
evidence in `docs/releases/2026-10-18-six-skill-plugins.md` at handoff.
