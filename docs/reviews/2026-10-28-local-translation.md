# Local Translation implementation and verification

Candidate verification captured on 28 October 2026 for `local-translation` 0.1.0,
before its commit and publication lifecycle. The candidate branch was
`codex/local-translation`, based on `b175ecb`. Later artwork, review, integration
and release status belong in the [release record](../releases/2026-10-28-local-translation.md)
and the associated pull request; this report preserves the original test scope.

## Implemented result

The original Translation Project skill maps all sixteen whitepaper functions to
explicit responsibilities, decision rights and work products. A project manager
uses the host's actual delegation tools to assign translators, separate bilingual
revisers, terminology and domain experts, engineering and quality work. Required
exchanges cover preparation, draft handoff, revision dialogue, adjudication,
final-format feedback and release. Human content decisions and acceptance remain
separate from agent recommendations. Conditional audiovisual roles require
verified media and capabilities beyond this text runtime.

Eight bundled stdio MCP tools manage immutable input jobs, local Index drafting,
status, shared queries, corrections, independent agent review and candidate
delivery. The runtime supports UTF-8 `.txt` and explicit `.json` segments, up to
eight configured target locales. It requires a configured numeric-loopback
vLLM-compatible deployment with `/v1/models`, `/v1/chat/completions` and a chat
`/tokenize` endpoint. Installation does not download weights or start a runner.
The package uses the Plugin Creator local-package workflow and its component
requirements; no account upload was requested or performed.

Both manifests, both MCP declarations, both marketplace catalogs, distribution
selection, contribution instructions and CI coverage include the package. The
pinned existing HOL scanner action has a new Local Translation job.

## Verification evidence

All Python checks used the repository `.venv` with bytecode writing disabled.

| Check | Result |
| --- | --- |
| `scripts/check_marketplace.py .` | Pass; 15 plugins |
| `scripts/check_copilot_marketplace.py --write`, then validation | Pass; generated catalog matches canonical membership |
| `scripts/check_plugin.py <package> --layout source` for every catalog package | All 15 pass |
| `scripts/check_distribution_bundle.py <package>` for every catalog package | All 15 pass, using clean temporary copies to preserve pre-existing ignored files |
| Final Local Translation source and materialized distribution | Pass; 24 files, one skill |
| Pinned OpenAI Plugin Creator `validate_plugin.py` | Pass; validator SHA-256 `ebda00d55d7518b127f675f062fb5c6e7a1ffdc0a99df1a55ac594400d7d3228` |
| Skill Creator `quick_validate.py` | Pass |
| `plugins/local-translation/mcp/server.py --self-test` | Pass; protocol/invariants only |
| `python -m unittest discover -s tests -p 'test_local_translation.py' -v` | 19 pass; independently repeated by reviewer |
| `python -m unittest discover -s tests -p 'test_*.py' -v` | 634 pass, 93.371 seconds, no skips |
| `git diff --check` | Pass |
| Final ZIP inventory and byte parity | Pass; all 24 files match source, including hidden manifests and both MCP declarations |

The full suite includes marketplace, Copilot, manifest and distribution regression
coverage. Fake-runner tests exercise successful multilingual work, partial
failure, exact model identity, token preflight, invalid/truncated responses,
placeholder/number/protected-span invariants, path boundaries, query and revision
invalidation, source/configuration changes, digest checks, metadata projection,
aggregate size limits and an actual stdio transcript. Loopback tests initially
could not bind inside the sandbox; approved execution outside it passed.

Independent review identified and verified two corrections: default status now
excludes free-text brief/glossary/query/review context; valid multilingual jobs
larger than 1 MiB remain readable, with coherent bounded job/artifact limits.
The original five-locale reproduction now completes review and candidate delivery.

## Native client checks

Codex CLI 0.164.0: registered this local marketplace in an isolated Codex home;
`plugin/read` exposed complete pre-install presentation, the skill and MCP server
with `installed: false`. `plugin/install` succeeded. After restarting the isolated
app server, `skills/list` exposed `local-translation:translation-project`, and
`mcpServerStatus/list` started the packaged server and discovered all eight tools
with no tools error. A separate subprocess launched that installed cache's MCP
entrypoint and completed initialize, discovery and a harmless health call against
a temporary synthetic local runner.

GitHub Copilot CLI 1.0.103: in an isolated Copilot home, ran
`plugin marketplace add <checkout>`, `plugin marketplace browse
sealad886-codex-marketplace`, `plugin install
local-translation@sealad886-codex-marketplace`, and `plugin list`. All succeeded;
installation reported one skill and an enabled live local plugin. Copilot did not
perform a native model turn or tool invocation. Real user settings and credentials
were not changed. Test processes received no inherited provider credentials.

## Unverified deployment and acceptance

No actual Index weights, GPU fit, latency, translation-quality benchmark,
representative language-pair pilot, interactive translation-agent run, final
document/media rendering, egress confinement or human acceptance was established.
The current upstream Index repository/prompt guide/model card and MCP transport
specification were consulted. Context7 was attempted but unavailable due to its
quota; current primary documentation/source supplied the integration evidence.
The runner's reported alias is checked, while artifact revision and runner build
remain operator-supplied provenance. Actor IDs are workflow attribution, not
authentication or proof of linguistic qualification.

At this candidate-verification checkpoint, the HOL job had been added to CI but
had not executed remotely. No commit, push, PR, merge, tag, release, deployment,
public listing, account-plugin save or installation into the user's real client
profile had occurred. Source PDFs, the supplied defective wrapper and model
binaries are not included in the plugin.
