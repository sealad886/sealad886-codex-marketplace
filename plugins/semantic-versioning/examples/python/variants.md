# Alternative Python owners

These are alternatives to the static example, not blocks to combine.

## Hatch file owner

Replace `project.version` with `dynamic = ["version"]`; retain Hatchling backend.

```toml
[tool.hatch.version]
path = "src/semver_example/_version.py"
```

Create `_version.py` containing `__version__ = "0.1.0"`. `hatch version 0.2.0` updates that source. Build and compare wheel/sdist metadata.

## setuptools-scm Git owner

Use `requires = ["setuptools>=80", "setuptools-scm>=8"]`, `build-backend = "setuptools.build_meta"`, and `dynamic = ["version"]`. Add:

```toml
[tool.setuptools_scm]
version_file = "src/semver_example/_version.py"
```

Tag history owns version; generated `_version.py` is not independently edited. Build from a clean exact tag with history available. Pin selected backend versions in actual adoption.

## Poetry / uv

Poetry 2 can own the static `[project].version`: `poetry version 0.2.0`, then `poetry build`. Existing `[tool.poetry].version` projects retain one canonical owner until explicitly migrated. uv builds the PEP 517 project with `uv build`; `uv version 0.2.0` applies to supported static project metadata. Neither `uv.lock` nor `poetry.lock` is a replacement package version source. Regenerate locks with the chosen tool after dependency changes; never hand-edit generated locks.
