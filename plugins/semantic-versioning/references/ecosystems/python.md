# Python

Read when Python distributions, build backends, or Git-derived metadata own versions.

## Sources and ownership

Static `[project].version` is authoritative for static builds. A backend supplies `version` when listed in `[project].dynamic`; inspect backend settings to find the actual owner. setuptools-scm uses Git tags/history, while Hatch can use a version file. Generated version modules are build outputs. Runtime access through `importlib.metadata.version(distribution_name)` avoids a second manually maintained value.

Do not write a static version over a dynamic configuration. uv and Poetry are project tools; the declared build backend determines wheel/sdist metadata. Requirements and lockfiles describe dependencies, not necessarily the current project's release identity.

PEP 440 is not SemVer. An explicit release mapping may translate `1.2.0-rc.1` to `1.2.0rc1`; development, post, epoch, and local versions require Python-specific interpretation. Check the actual normalized version accepted by the target index. Never compare Python versions using the strict SemVer helper.

## Example and checks

[Static Hatchling project](../../examples/python/pyproject.toml) and [alternative owners](../../examples/python/variants.md). Run `uv build` in a disposable copy. Inspect `*.dist-info/METADATA` inside the wheel and `PKG-INFO` inside the sdist; require matching Name/Version. Build a wheel from the sdist too, catching missing version inputs. Install into an isolated environment and assert `installed_version() == "0.1.0"`.

For SCM builds, reproduce from a clean exact tag with required history; report missing/shallow history instead of inventing a version. Test generated metadata outside the checkout to catch accidental source imports. Keep prerelease promotion consistent across PyPI and application metadata.

## Sources

[pyproject specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/), [version specification](https://packaging.python.org/en/latest/specifications/version-specifiers/), [setuptools-scm](https://setuptools-scm.readthedocs.io/en/latest/), [Hatch versioning](https://hatch.pypa.io/latest/version/), [uv projects](https://docs.astral.sh/uv/guides/projects/), [Poetry version](https://python-poetry.org/docs/cli/#version).
