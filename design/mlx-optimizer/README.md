# MLX Optimizer artwork

Original procedural artwork for MLX Optimizer 0.2.3. The canonical exports live in
[`plugins/mlx-optimizer/assets`](../../plugins/mlx-optimizer/assets/).

## Current design

The 2026-09-06 rebuild replaces generated-image cleanup with shared, editable
geometry and deterministic material rendering. The original generated sources and
cleanup proofs remain available locally as reference.

- A textured dark slate tile forms the bottom physical layer.
- One continuous beveled metallic M turns left into a hooked foot. There is no
  redundant descending metal diagonal beneath the white output rail.
- Cyan, blue, and amber glass inputs share one continuous junction. After the
  junction, the rail has a brighter white core and denser electrical discharge.
  Intensity continues increasing down the diagonal: clearly energized by its
  midpoint, with the brightest core and strongest irregular discharge at the tip.
- Each input uses an independent seeded random discharge with irregular spacing,
  displacement, and branching. The output has a separate seed and more strands.
- Three groups in Icon Composer separate slate, metal, and elevated glass.
  The slate's additional glass effect is disabled to preserve its surface.
  The rail uses refraction strength 16%, depth 18%, translucency 12%, and its own
  shadow. These are renderer settings, not a calibrated physical Z measurement.

## Editable sources

- [Apple Icon Composer document](MLX%20Optimizer%20Rebuilt.icon/)
- [Geometry and material renderer](rebuild/render.swift)
- [Export transparency and proof helper](rebuild/finish.swift)

The reproduction commands generate the source layers, Default and Dark previews,
small-size proofs, colored-background proof sheet, and alpha/component audit.
These intermediate outputs are local build artifacts; only the editable document,
source scripts, and canonical plugin exports are versioned.

All three source layers are 2048 by 2048 RGBA PNGs. Composer imports are 1024 by
1024 to match its point canvas. Each source layer contains exactly one connected
component above alpha 2, with alpha 0 on every outer edge and corner. The native
exports are clipped to the slate silhouette: Icon Composer's system background
otherwise remains visible beyond the custom tile even with a transparent fill.
The export helper retains source tile colors at antialiased boundary pixels to
avoid contamination from that system background. It does not change the rendered
metal or rail interiors.

## Reproduction

Run from this directory on macOS with Swift and Apple Icon Composer 2.0:

```sh
swiftc -O rebuild/render.swift -o /private/tmp/mlx-rebuild-render
/private/tmp/mlx-rebuild-render "$PWD/rebuild"
sips -z 1024 1024 rebuild/mlx-tile.png --out 'MLX Optimizer Rebuilt.icon/Assets/mlx-tile.png'
sips -z 1024 1024 rebuild/mlx-m-hook.png --out 'MLX Optimizer Rebuilt.icon/Assets/mlx-m-hook.png'
sips -z 1024 1024 rebuild/mlx-rails.png --out 'MLX Optimizer Rebuilt.icon/Assets/mlx-rails.png'
'/Applications/Icon Composer.app/Contents/Executables/ictool' "$PWD/MLX Optimizer Rebuilt.icon" --export-image --output-file "$PWD/rebuild/composer-raw.png" --platform macOS --rendition Default --width 1024 --height 1024 --scale 1 --design-generation 26
'/Applications/Icon Composer.app/Contents/Executables/ictool' "$PWD/MLX Optimizer Rebuilt.icon" --export-image --output-file "$PWD/rebuild/composer-dark-raw.png" --platform macOS --rendition Dark --width 1024 --height 1024 --scale 1 --design-generation 26
swiftc -O rebuild/finish.swift -o /private/tmp/mlx-icon-finish
/private/tmp/mlx-icon-finish "$PWD/rebuild"
```

In a restricted Codex shell, Swift needed a writable `-module-cache-path`, and
Apple's `ictool` needed native execution outside the sandbox. It failed to open
even a document saved by its own app inside the sandbox; native execution passed.
Cross-version CoreGraphics/PNG byte identity is not promised.

## Updating the plugin assets

After visually reviewing the generated previews, copy `rebuild/composer-preview.png`
to `../../plugins/mlx-optimizer/assets/mlx-optimizer-logo.png` and
`rebuild/composer-preview-256.png` to
`../../plugins/mlx-optimizer/assets/mlx-optimizer-icon.png`.
The plugin manifest references those 1024-pixel and 256-pixel RGBA PNGs.

The source artwork is original and covered by the repository MIT license.
Swift, CoreGraphics, and Icon Composer are build tools, not plugin dependencies.
