# Python Package Management with uv: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Projects and scripts

- Project add/remove/sync updates project dependency/environment state; standalone PEP723 scripts have their own metadata and optional lockfile.
- uv run can resolve/install or download an interpreter; inspect allowed network and environment effects before invoking it.
- Current uv supports script-oriented commands including sync --script where the installed help confirms it; do not confuse script and project lock ownership.

## Reproducibility and environment

- Use uv lock --script and locked execution where required; metadata alone specifies ranges rather than an immutable environment.
- Choose --locked versus --frozen according to the required freshness/check behavior; neither replaces reviewing lock changes.
- Never install into global/system Python or replace an established pip/Poetry workflow merely because this skill exists.
- Treat index credentials, build scripts and interpreter downloads as separate trust/resource boundaries; avoid logging full index configuration.

## Primary documentation

- [Primary documentation](https://docs.astral.sh/uv/guides/scripts/) — uv supports PEP723 script dependencies and separate locking/execution behavior for reproducibility.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
