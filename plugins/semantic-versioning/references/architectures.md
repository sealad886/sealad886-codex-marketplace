# Release architectures

Read for workspaces, multiple artifacts, or mixed languages. Keep policy in existing project docs and native release configuration.

| Architecture | Version owner and assessment |
|---|---|
| Single package | One baseline, canonical source, native update command, package metadata check. |
| One app, many artifacts | Shared product version; platform build identifiers and artifact digests remain separate. |
| Fixed-version workspace | One release group; highest relevant impact becomes group version; publish required members in dependency order. |
| Independent workspace | Per-package baseline and impact; calculate affected dependents using native workspace graph/range rules. |
| Mixed-language repository | Separate ecosystem release units; explicit group only when the product contract requires it. |

Record package edges and published dependency constraints. An internal implementation change is not automatically a breaking change to all dependents. Update required ranges and determine republishing with the native tool; don't propagate major bumps mechanically. Exclude private non-published roots. Detect cycles and use ecosystem-supported staged publication or stop with a concrete graph issue.

Consolidation is an authorized migration: inventory sources and consumers, locally back up originals outside the release payload, produce a project-specific once-off conversion, overwrite canonical artifacts, remove superseded active sources, rebuild and inspect package metadata, and document restoration from the backup. Never execute an unreviewed general rewrite across formats. No permanent compatibility adapter or plugin-owned state directory is required.
