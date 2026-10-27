# Repository instructions

## Required marketplace support

Every plugin in this repository must remain valid for **both Codex and GitHub
Copilot**. Apply this requirement to new plugins and to all changes to existing
plugins, including metadata, versions, skills, MCP servers, package contents,
catalog membership, and release automation. A change is not complete when only
one marketplace validates.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the owning plugin's guide before
editing. Extend the existing package and validation tools; do not create separate
Codex and Copilot copies of the same skills or runtime implementation.

## Catalogs and manifests

- `.agents/plugins/marketplace.json` is the canonical catalog for membership and
  package paths. Preserve Codex source declarations and intentional release pins
  unless changing them is part of the authorized task.
- `.github/plugin/marketplace.json` is the generated Copilot catalog. Regenerate
  it with `scripts/check_copilot_marketplace.py --write` after additions,
  removals, renames, version changes, or description changes. Do not maintain a
  divergent hand-edited catalog or weaken validation to hide drift.
- Every package must ship root `plugin.json` using the Agent Plugins 1.0 schema
  and `.codex-plugin/plugin.json` for Codex. Keep common identity, version,
  description, author, homepage, repository, license, and keywords synchronized.
  Keep OpenAI presentation under `extensions.com.openai.interface` identical to
  the Codex overlay's `interface`; `shortDescription` must be at most 30 characters.
  Do not put legacy component-path or Codex-only fields at the portable
  manifest's top level.
- Keep shared skills in `skills/<skill-name>/SKILL.md`. Document client-specific
  tools and prerequisites honestly; marketplace validity does not imply that
  every host supplies the same UI, integrations, or runtime capabilities.

## MCP and distribution

- Packages with MCP servers must ship both the Codex `.mcp.json` declaration and
  portable root `mcp.json` using the Agent Plugins 1.0 MCP schema. Keep server
  names, commands, and entrypoints aligned. Use `stdio` and `${PLUGIN_ROOT}` paths
  in portable configurations; do not copy Codex-only `tool_timeout_sec` there.
- Final distributions must retain root `plugin.json`, the Codex overlay, all
  skills, both MCP configurations when applicable, and referenced assets,
  scripts, and supporting files. Update the existing distribution selector when
  introducing a new required resource; a valid source checkout is insufficient
  if the packaged plugin omits it.

## Required verification

Use the existing project Python environment. Before handing off a plugin change:

1. Regenerate the Copilot catalog when its inputs changed, then run both
   `scripts/check_marketplace.py .` and `scripts/check_copilot_marketplace.py .`.
2. Run `scripts/check_plugin.py plugins/<plugin-id> --layout source` and
   `scripts/check_distribution_bundle.py plugins/<plugin-id>` for every affected
   package. For shared packaging or catalog changes, check all catalog packages.
3. Run relevant regression tests and the owning plugin's checks from
   [CONTRIBUTING.md](CONTRIBUTING.md). Shared validator or packaging changes must
   include the marketplace, Copilot, manifest, and distribution regression suites.
   Disable Python bytecode writing during validation to avoid adding cache files
   to package source trees. Preserve any pre-existing ignored files; use clean
   temporary package copies when those files prevent distribution validation.
4. For changes to discovery, manifests, MCP declarations, or distribution layout,
   verify discovery and installation in both clients with isolated test settings
   when available. Keep real user settings and credentials untouched. Report
   client versions, commands, results, and any unavailable client or omitted
   runtime checks; static validation alone is not proof of live installation.

Keep CI checking both catalogs and portable components. Update installation,
contribution, and release documentation when the corresponding workflow changes.
