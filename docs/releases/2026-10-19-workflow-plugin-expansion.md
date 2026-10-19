# Workflow plugin expansion: candidate verification

Date: 2026-10-19 (Europe/Dublin). Versions: six plugins at 0.2.0.
Design, implementation, PR/merge, public/private publication and local refresh
were explicitly approved in chat. This records the validated candidate before
public integration; PR/release records retain later immutable publication IDs.

## Packages

| Plugin | Files | Archive SHA-256 |
| --- | ---: | --- |
| iterating-pr-bot-fixes | 17 | `a23b86188e91878011ec301335f1d1712f035ada1bcb53e41c0e13c22b9f4a84` |
| repo-consolidation | 21 | `744cf4c5be6f13760b6ed43f4232a66f82c3fa66b021929b14ea80c66375ea5f` |
| conventional-commit | 15 | `c05b2fd451e948c0036e38c4f24b88ba5280e2cc6c11608c70ea2103686d51fa` |
| simplify-code | 15 | `83a608a4b5ad4a579f1df92a95be1b06655f03ea388027b1c71bd127cac57454` |
| adversarial-audit | 16 | `b70962b8b738566bc216784b563701da2a93b0be2533ceecd4992b2ec1be87d9` |
| web-research | 17 | `69fe4b9805ec13a75059ef415fe04e84d4f279805d92f58947ccaa47b56f9ffe` |

All six retain one namespaced skill and independent installation. New conditional
references/templates remain inside their owning skill. Identity, existing starter
prompt values/type/order, artwork and license are retained. Web Research updates
its descriptive listing text for the new workflows. No executable, server,
new runtime dependency, local-executor requirement or sibling dependency is added.

## Candidate checks

- All six source and exact-distribution checks passed: 101 files, six skills.
- The CI-pinned OpenAI Plugin Creator validator passed all six; validator bytes
  matched the repository pin before execution.
- Full existing regression suite: 587 tests, four skipped, zero failures/errors.
  It ran outside the filesystem sandbox for loopback/MLX-related checks, with
  fixture-only process settings disabling automatic Git maintenance and signing;
  real commit signing and global configuration remain unchanged.
- Independent specification then quality/authority reviews approved both package
  groups. Scope, source-retirement policy, immediate-human cleanup opt-in,
  evidence limits, optional templates and conditional loading were checked.
- Fresh isolated native discovery found complete pre-install metadata and one
  skill per plugin; all six installed, appeared in skills/list with namespaced
  identities, and matched all 101 package files byte for byte.
- ZIP contents were compared with validated package bytes and committed package
  trees. Publication must still verify the actual merge source, tag and server
  asset digest before reporting release completion.

## Behavioral and scenario evidence

Conventional Commit's documented staged-subset procedure was exercised with
actual Git 2.54.0. A negative control showed a plain whole-index commit included
excluded staged changes. The constrained procedure then passed 13 scenarios,
including selected/excluded staged content, excluded unstaged/untracked content,
index bytes and flags, empty/unsupported selections, pre-commit/signing failures,
unsafe-hook detection, and concurrent head/index/working changes. A separate
reviewer inspected the fixture source and reran the negative control and all 13
cases successfully. Semantic independence and suitable hooks remain explicit
human-established preconditions; the fixtures do not automate those decisions.
Unsafe-hook probes show postflight detection and stopping, not prevention,
rollback or general recovery guarantees. No arbitrary index reconciliation is
claimed.

Consolidation's disposable Git checks covered shared prerequisites integrated
once with independent callers retained, historical equivalence followed by an
intentional revert, bundle-only recovery missing dirty layers, executable modes
and symlinks, and an LFS pointer without its required payload. These demonstrate
the distinction between Git-object preservation and complete checkout recovery.

PR revision/provider/cleanup, simplification lifecycle/caller, audit oracle/fault,
and research comparison/refresh/quantity scenarios received independent
instruction-level review. They were not real provider operations, production
fault injection, recovery of user data, or end-to-end research tasks.

## Remaining publication gates

Current-head hosted review/checks, actual merged source identity, private account
source readback, signed public tags/releases, resulting marketplace snapshot,
and published/local native installation parity remain required. Cloud eligibility
is configuration evidence; no separate cloud task execution is established by
candidate package or local installation checks.
