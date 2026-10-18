# Six skill plugins: candidate verification

Date: 2026-10-18 (Europe/Dublin).
Scope: six independent instruction-only plugins, initially version 0.1.0.
Design and implementation/publication were explicitly approved in chat.

This records the candidate checks before GitHub integration and publication.
Release tags, hosted checks and the resulting marketplace snapshot must still
be read back before publication is reported complete. The PR and GitHub release
records retain those later immutable integration/publication identities.

## Packages

| Plugin | Skills | Files | Archive SHA-256 |
| --- | ---: | ---: | --- |
| iterating-pr-bot-fixes | 1 | 15 | `9fb32aae743c64825aa301b8a2fff629adf2de653b35ba1c588115188bf99cb3` |
| repo-consolidation | 1 | 19 | `e394fe5c74c95b552fb80b1fe5f2d299f658f3508386e60b07d39a208fdc550f` |
| conventional-commit | 1 | 13 | `03dedcfe3a28e99a76d8fd76987a7cefbb33a5df6c8f85a97f7cc77e5c8f7b92` |
| simplify-code | 1 | 12 | `9b8ba7154208a7f9c5089958b269dd89187b5e8fa2d6ac984f26d043a7c2ffa6` |
| adversarial-audit | 1 | 14 | `ba59c7e665acb5b73d63e84f10f90548d9f4dabfcd031e90ae9d15071edf4ab0` |
| web-research | 1 | 12 | `ce1ab774525f45094bc96dfb4d5bbe6231bc2e2fdf8dce20cdc7f7845bc6b370` |

Archives contain exactly one enclosing plugin directory, portable and Codex
manifests, one skill, contained references/templates, metadata, artwork, license,
guide and security boundary. No runtime executable, server, app binding or hidden
sibling dependency is bundled. ZIP members were checked against validated
distribution bytes; archive checksums identify the release attachments.

## Checks performed

- Source structure and contract/link checks for all six new packages: passed.
- Exact distribution closure, including portable manifests and one-skill counts:
  passed for all six.
- CI-pinned OpenAI Plugin Creator validator: passed for all six. Downloaded
  validator SHA-256 matched the repository's pinned value.
- Skill Creator frontmatter validation: passed for all six.
- JSON/YAML, square contained SVG assets, display limits, manifest agreement,
  exact repository license and whitespace checks: passed.
- Marketplace catalog validation: passed with twelve plugins.
- Full existing regression suite plus packaging regressions: **587 tests,
  four skipped, zero failures/errors**.
- Independent specification and instruction-quality reviews: approved for both
  package groups. Independent Python/input-security and infrastructure reviews:
  approved after correcting portable schema validation, dark-artwork closure,
  category agreement and starter prompt length.

Regression tests cover portable-manifest retention, invalid fields/types,
identity/interface disagreement, contained regular artwork, dark artwork
inclusion and extra-skill rejection. No tests pin skill prose or private helper
architecture.

The full suite ran outside the filesystem sandbox for existing loopback HTTP
tests. Disposable fixture commits used process-only `commit.gpgsign=false` and
`maintenance.auto=false`; real commit signing and global Git configuration were
unchanged. An earlier cleanup-only failure was traced to detached Git maintenance
recreating a temporary fixture directory. A traced targeted run with maintenance
disabled observed no maintenance child and passed; the full rerun passed.

## Native candidate consumption

Using a fresh isolated Codex home and Codex CLI 0.163.0-alpha.10.2:

1. Registered the candidate repository marketplace.
2. Called native `plugin/read` before each install: complete display metadata,
   existing artwork, exactly one skill, and `installed=false` for all six.
3. Installed all six using native `plugin/install`; no connected apps required
   authentication.
4. Re-read installed state and native `skills/list`: all six enabled namespaced
   skills present with their intended interface metadata.
5. Compared all **85 files** against their source packages: exact byte parity.

Starter skill prompts use the actual `<plugin>:<skill>` identity to distinguish
these plugins from an independently installed skill of the same short name.
Everyday plugin installations were not altered by these isolated checks.

## Plugin Creator account saves

All six archives were saved as private personal plugins at 0.1.0 through Plugin
Creator after duplicate discovery. Readback returned each expected file set and
exactly one skill. Skill, reference, template, guide and artwork contents matched
the submitted package. The service normalized JSON formatting, added account
author metadata and normalized the Codex skills-directory trailing slash;
manifest identity/version/presentation otherwise agreed.

Private account saves do not publish the GitHub marketplace or submit to the
OpenAI public directory. Saved-plugin IDs/URLs are retained in the private task
handoff rather than added to this public source record.

## Evidence limits

These checks establish package structure, loading and content review. They do
not demonstrate every future agent execution, real provider operation, or
desktop visual rendering. Published marketplace discovery/install parity and
live hosted scanner results are separate final delivery gates.
