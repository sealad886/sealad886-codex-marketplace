# C and C++

Read when native libraries combine package releases and ABI identities.

## Sources and ownership

CMake `project(... VERSION ...)` can own a release value and generate headers through configure_file. Shared-library `VERSION` describes the library version; `SOVERSION` tracks ABI compatibility and must follow the platform's loader rules. Package version and ABI version are related decisions, not interchangeable strings.

Conan recipes may own a package version, take it from command arguments, or derive it through set_version. vcpkg supports version, version-semver, version-date, and version-string schemes; preserve the selected scheme. vcpkg port-version is a packaging revision separate from the upstream release. Native headers, exported symbols, layout, calling conventions, and supported compilers belong in impact analysis.

## Examples and checks

[CMake library](../../examples/cpp/CMakeLists.txt) generates a version header and shared library. Run `cmake -S . -B build` and `cmake --build build`; inspect generated header and library identity with native tools (`otool -L` on macOS, `readelf -d` on ELF systems). ABI compatibility requires comparison with the released binary/API baseline.

The adjacent Conan and vcpkg files are independent configuration recipes, not a synchronized second owner. Adopt one packaging source policy; generate or explicitly update dependent metadata. The Conan fragment requires project-specific build/package methods before use. Run `conan inspect .` or vcpkg manifest validation in the selected packaging environment; do not claim those checks build a publishable library.

## Sources

[CMake project](https://cmake.org/cmake/help/latest/command/project.html), [SOVERSION](https://cmake.org/cmake/help/latest/prop_tgt/SOVERSION.html), [Conan version attribute](https://docs.conan.io/2/reference/conanfile/attributes.html#version), [vcpkg versioning](https://learn.microsoft.com/en-us/vcpkg/users/versioning).
