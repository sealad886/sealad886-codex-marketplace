# Verification receipt

Verified 2026-11-10 against the local working checkout, based on commit
`44ea8c5` plus uncommitted changes. Existing unrelated edits were preserved.
No commit, push, publication, release, normal-user installation, or global
instruction change was performed.

## Behavioral and shared regression checks

Using the existing project `.venv` with `PYTHONDONTWRITEBYTECODE=1`:

| Suite | Result |
| --- | --- |
| `test_worktree_activity.py` | 33 passed |
| `test_copilot_marketplace.py` | 8 passed |
| `test_validation.py` | 15 passed |
| `test_marketplace.py` | 16 passed |
| `test_distribution_bundle.py` | 29 passed |
| `test_validator_file_safety.py` | 9 passed |
| `test_installed_parity.py` | 4 passed |

Focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover \
  -s tests -p 'test_worktree_activity.py' -v
```

Shared suite commands substitute each table filename after `-p`. The shared
suite run used process-local `GIT_CONFIG_GLOBAL=/dev/null`,
`GIT_CONFIG_NOSYSTEM=1`, and `maintenance.auto=false` to isolate fixture commits
from real user configuration. Local-loopback fixture tests needed execution
outside the shell sandbox. Initial sandbox/signing failures were environmental;
all listed reruns passed. No actual project worktree was created or moved;
behavioral tests use disposable repositories only.

The tests cover owner isolation, cross-project grouping, diagnostic delegation,
missing/conflicting identity, explicit coordinator assertion, task idempotence,
terminal evidence/cancellation, retained registration/activity timestamps,
metadata reconciliation, detached HEAD, non-ASCII/spaced paths, malformed JSON,
unknown versions, identifiers/formats, symlinks, unreadable directories,
partial/bounded scans, concurrent writes/readers, update/finalize contention,
atomic-write failure injection, mutex timeout, relocation, external linked
worktrees, and stale paths reused by unrelated projects.

Independent review checked owner identity, deletion, concurrency, scan scope,
schema and packaging. Its concrete findings were corrected and regression
tested. The final stale-path mismatch checks were independently reproduced with
zero registry reads. Role assertion coverage is not native role authentication.

## Catalogs, manifests, and package closure

Both catalog commands pass: Codex has 17 packages; generated Copilot has 16,
intentionally excluding Worktree Activity. The generated Copilot catalog remains
byte-identical to its previous intended membership.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_copilot_marketplace.py --write
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_marketplace.py .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_copilot_marketplace.py .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_plugin.py \
  plugins/worktree-activity --layout source
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_distribution_bundle.py \
  plugins/worktree-activity
```

All 17 canonical packages passed source and exact distribution checks using
clean temporary copies. Pre-existing ignored bytecode and `.DS_Store` files were
excluded from those copies and preserved in the source checkout. The new package
also passes direct source/distribution validation.

The repository's pinned OpenAI Plugin Creator manifest validator passed:
source revision `2c351cb8646054427e0ea81a484233114b1234f7`, validator SHA-256
`ebda00d55d7518b127f675f062fb5c6e7a1ffdc0a99df1a55ac594400d7d3228`.
Installed Skill Creator `scripts/quick_validate.py` also passed.

A clean disposable virtual environment installed all eight runtime dependency
pins from `scripts/requirements.txt` with hash checking. `requirements.in`
contains the two direct dependencies; regenerate the hash lock with the command
recorded at its top. The packaged helper ran from a relocated package and an
unrelated checkout. Final archive inspection retains both manifests, the skill,
schema, helper, lock, examples, references, and referenced artwork, including
the helper's executable bit.

## Live integration and explicit limits

Desktop `26.1103.60933` build `25894`, bundled runtime
`0.167.0-alpha.3.2`: isolated app-server `plugin/read`, `plugin/install`, and
`skills/list` passed, with pre-install discovery and an enabled installed skill.
A native Desktop shell exercised registration, progress, validation, verified
completion, and finalization through the installed helper in a disposable linked
worktree, using the clean hash-locked environment. Captured native thread/session
values matched the shell; the exact owner record was removed after verification.

Copilot CLI `1.0.107`: isolated native catalog registration/browsing omitted this
plugin; installing its marketplace selector failed with the expected
plugin-not-found result. No Copilot runtime execution is intended.

See [runtime identity](runtime-identity.md) for sources and version scope.
Desktop visual rendering, an OS deep-link navigation round trip, mandatory
implicit activation, real interrupted-conversation recovery, and behavior on
network filesystems or power loss remain unverified. No messaging/resumption is
implemented. The full unrelated cross-plugin application suite and hosted CI/HOL
scanner were not run for this local task; CI now includes the package and its
locked dependencies. This receipt is not a release certification.

## Branding and first-release preparation — 2026-11-11

The original conversation/branch/bookmark identity now appears in the plugin and
marketplace READMEs, with one packaged PNG banner and one canonical SVG under
`skills/worktree-activity/assets/`. Both manifests and the skill reference that
same SVG. Image Generation produced the banner; the vector mark is original
native SVG. The source artwork ledger records its prompt and palette.

The 33 behavioral tests and 12 release-workflow tests passed again. Both catalog
checks, source/distribution checks, the checksum-pinned OpenAI manifest validator,
and Skill Creator validation passed. An isolated installation through the
Desktop-bundled runtime reported no skill errors; both installed skill icon
paths resolved to bytes identical to the canonical SVG. No normal-user settings
or unrelated development work were changed.

The initial receipt above describes the earlier local implementation milestone.
For this first release, the exact committed package is built separately from the
dirty working checkout. Publication requires successful validation and the pinned
HOL scanner on that source commit. The GitHub release and its automatically
created marketplace snapshot are authoritative for publication status; preparing
these files alone does not establish that publication occurred.
