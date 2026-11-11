# Claude Code marketplace support — 2026-11-11

## Scope and design

Add Claude Code support to every existing plugin except Worktree Activity.
Codex's catalog remains the membership and source owner. Copilot and Claude
catalogs are generated projections, and every included plugin retains one
shared skill tree and runtime. Claude overlays mirror common identity metadata
and declare inline MCP servers with `${CLAUDE_PLUGIN_ROOT}` entrypoints.
Existing Project Delivery [scope guidance (#29)](https://github.com/sealad886/sealad886-codex-marketplace/issues/29)
remains applicable: this adds host packaging without changing lifecycle routing.
Default same-name MCP declarations are replaced by the manifest's absolute
entrypoints; Codex and portable declarations remain intact.

Worktree Activity stays Codex-only at 0.1.0. No files in its package change.
Camofox follows its upstream/npm release process before its complete plugin
package is copied into this repository. Its new plugin version must have a
matching published npm runtime; changed packages never reuse a released version.

Acceptance: all three catalogs validate; all 17 package/distribution checks pass;
all 16 target plugins validate and install in Claude Code and Copilot; Codex
retains discovery/install of all 17; native inventories match package skills and
MCP names; shared CI and the pinned HOL scanner pass before publication.

## Package versions

| Plugin | Version |
| --- | --- |
| `project-delivery` | `1.5.1` |
| `conversation-visuals` | `0.1.3` |
| `mlx-optimizer` | `0.2.6` |
| `semantic-versioning` | `0.1.2` |
| `icloud-mail` | `0.4.1` |
| `build-multi-target-tauri-apps` | `0.2.1` |
| `iterating-pr-bot-fixes` | `0.2.2` |
| `repo-consolidation` | `0.3.1` |
| `conventional-commit` | `0.2.1` |
| `simplify-code` | `0.2.1` |
| `adversarial-audit` | `0.2.1` |
| `web-research` | `0.2.1` |
| `repository-guidance` | `0.1.1` |
| `camofox-mcp` | `0.1.2` |
| `local-translation` | `0.6.1` |
| `mindrally-skills` | `0.1.1` |

## Verification

- Claude Code 2.1.311: strict native validation of 16 packages; isolated catalog
  discovery and 16 enabled installations; exact inventory of 328 skills and four
  MCP servers. Worktree Activity absent. No model turns or runtime setup.
- GitHub Copilot CLI 1.0.107: isolated discovery and 16 enabled installations;
  exact inventory of 328 plugin skills. Worktree Activity absent. Local installs
  load the prepared source directly rather than a separate copied cache.
- Codex 0.167.0-alpha.3.2: isolated app-server `plugin/read` before installation,
  `plugin/install`, installed metadata and fresh-server `skills/list`; 17 enabled
  packages and 329 skills. Each of the 16 target caches retains its Claude
  overlay. Local-source fixtures test the candidate payloads; published pinned
  source resolution is a separate release check.
- All 17 source, 17 distribution, and 17 pinned official Plugin Creator checks
  passed on clean temporary copies. Existing ignored `.DS_Store` and bytecode
  files were preserved in the working checkout. All 22 changed skills or skills
  sharing changed references passed Skill Creator validation.
- Repository catalog, Semantic Versioning, route, historical route receipt,
  Mindrally 265/265 review coverage, Conversation Visuals MCP and iCloud MCP
  self-checks passed. Independent implementation review found no open blocker.

Commands use the existing `.venv` and `PYTHONDONTWRITEBYTECODE=1`. Tests requiring
loopback sockets run outside the sandbox. Native tests use disposable
`CODEX_HOME`, `COPILOT_HOME`, and `CLAUDE_CONFIG_DIR`; user settings and credentials
are untouched.

## Publication and limitations

Publish through a reviewed signed-commit PR and the common marketplace release
action. Each updated package receives an immutable version tag; one marketplace
release records the batch. Codex's four pinned sources advance to the validated
package content, and their bytes must match the tagged merge packages. No
per-plugin GitHub Release is needed to repeat the full snapshot pipeline for
every package in this one batch.

Marketplace compatibility does not provide every host's native UI or tools.
Claude lacks Codex panels and native plugin settings; the guides identify
available local/connected visual tools and Local Translation's file/environment
configuration path. Real mailbox/model operations, Apple Silicon execution of
all MLX guidance, and every framework recipe are outside these packaging checks.
Camofox's own release additionally requires its real-browser smoke workflow.
Existing immutable releases remain available for rollback; fixes use new versions.
