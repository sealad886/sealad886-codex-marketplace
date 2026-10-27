# Repository Guidance 0.1.0 candidate verification

Date: 2026-10-27 (Europe/Dublin). The user requested a reusable plugin inspired
by Multica's agent guide, marketplace incorporation, and publication.

## Scope

One shared skill creates, adapts, or audits repository instructions from local
evidence. Its references contain adaptation lenses, an example for this
marketplace, revision-pinned research provenance, and an optional record template.
It contains original text and artwork, no upstream source payload or runtime.
The package has 13 files and no server, dependencies, or account connection.

Both manifests declare `repository-guidance` version `0.1.0`. The canonical
Codex catalog uses a local package source; the Copilot catalog is regenerated.
The existing distribution checker enforces one skill, and the existing pinned
HOL workflow includes the package in its standalone-workflow matrix.

## Candidate evidence

- Both catalogs pass with 14 plugins. All 14 catalog packages pass source and
  distribution checks. A clean temporary copy excludes pre-existing iCloud Mail
  bytecode during distribution validation; the original ignored file is preserved.
- Full regression suite: 614 tests, zero failures/errors. Run with the existing
  project environment, `PYTHONDONTWRITEBYTECODE=1`, and fixture-only Git settings
  disabling automatic maintenance and signing. Real commit signing is unchanged.
  The suite ran outside the filesystem sandbox for local socket/MLX fixtures.
- Semantic-versioning, route, historical route-receipt, and both MCP self-checks
  pass. The changed skill passes Skill Creator validation. The new package passes
  the CI-pinned OpenAI manifest validator after verifying its SHA-256 pin.
- Independent review found no blocking correctness, contract, security, or
  packaging issues. Static scenarios covered documentation-only repositories,
  backend/data concerns, and this marketplace's dual-client contracts.
- Codex CLI 0.164.0, with a temporary `CODEX_HOME`: marketplace registration,
  app-server `plugin/read` before installation, `plugin/install`, `plugin/read`
  after installation, and `skills/list` pass. Pre-install metadata includes both
  starter prompts and existing artwork; one enabled namespaced skill loads.
- GitHub Copilot CLI 1.0.103, with a temporary `COPILOT_HOME`: `plugin marketplace
  add`, `plugin marketplace browse`, `plugin install`, `plugin list`, and `skill
  list` pass. One skill and enabled version `0.1.0` are reported.
- Installed Codex cache parity matches all 13 package files. No model prompt,
  live account test, or change to real user settings was needed for client checks.
- Initial overlong starter prompts were shortened in both manifests and retested;
  the final Codex discovery response retains both prompts without warnings.

Final distribution payload SHA-256:
`9d4c7860cc1b96b26440a01bd588d1b074badef1dbb11ebae7b87f83855d1d86`.
The 13-file ZIP was inspected and compared byte for byte with that closure;
archive SHA-256:
`7baa3c76ff5a721c25f12ee6ee91c8bd4bfacb09f584129f66710faebca7d05a`.

## Publication and limits

This record describes the candidate before public integration. The PR and release
retain immutable commit, tag, hosted-check, scanner, and asset evidence. Publication
must verify the actual merged package bytes, release asset, resulting marketplace
snapshot, and remote discovery/install identity. Candidate checks do not establish
future agent adherence, automatic AGENTS.md loading by every host, a private
account save, or an OpenAI public-directory submission.
