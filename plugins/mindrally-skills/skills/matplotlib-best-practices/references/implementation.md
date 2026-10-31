# Matplotlib Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Visual representation

- Use categorical, sequential or diverging colors according to the data; a named palette alone does not prove colorblind accessibility.
- Show missing data and uncertainty without implying unsupported precision; label scales and units where meaningful.
- Use constrained layout or the existing layout engine deliberately; titles and legends are conditional on communication needs.

## Backends and export

- Interactive notebook backends and static export backends have different capabilities; %matplotlib inline is notebook-specific.
- Match physical figure dimensions and raster DPI to the output requirement; vector content is not improved by arbitrary higher DPI.
- Use rasterization for dense artists in vector output where it reduces file cost without losing required detail.
- MathText handles many mathematical labels without a full TeX installation; external usetex has separate dependencies.
- Close the created Figure, not plt.close(all), when other notebooks/tasks may own figures.

## Primary documentation

- [Primary documentation](https://matplotlib.org/stable/users/explain/figure/backends.html) — Matplotlib rendering/export capabilities depend on selected interactive and noninteractive backends.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
