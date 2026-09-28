# Ecosystem examples

Copy only the selected example into a disposable project before running its commands. These names are examples, not authorized publication targets. References in `../references/ecosystems/` define ownership, metadata checks, and variant choices.

| Directory | Status | Local validation |
|---|---|---|
| javascript | Minimal package plus separate workspace | `npm test`, `npm pack --ignore-scripts --dry-run --json` |
| python | Minimal Hatchling package; alternative owner recipes | `uv build`, inspect wheel METADATA and sdist PKG-INFO |
| rust | Two-crate fixed-version workspace | `cargo test --workspace`, `cargo package -p semver-example-core` |
| go | Minimal executable | `go test ./...`, `go build -ldflags '-X main.version=0.1.0'` |
| jvm | Maven package plus separate Gradle package | `mvn package`, `gradle jar generatePomFileForLibraryPublication` |
| dotnet | Minimal NuGet library | `dotnet pack --configuration Release` |
| mobile | Platform configuration fragments; buildable Swift library | `swift build --package-path swift`; native app builds need host project |
| cpp | Buildable CMake library; Conan/vcpkg configuration fragments | `cmake -S . -B build`, `cmake --build build` |
| ruby-php | Minimal gem and Composer library | `gem build semver_example.gemspec`, `composer validate --strict` |
| containers-plugins | Chart/data-image examples; plugin manifest fragment | `helm lint chart`, `helm template check chart`; image/plugin packaging needs host configuration |

Prerequisites: Node 22+, Python 3.11+/uv, Rust 1.85+, Go 1.22+, JDK 17+/Maven 3.9+, .NET SDK 8+. These are compatibility targets, not claims that all runtime checks have passed. Actual check results belong in the delivery report. Pin concrete tool versions in CI and refresh pins deliberately. No example publishes anything by itself.

Native tools may execute project configuration and create caches/build output. The plugin's inspection helpers do neither. Never install Python tools into system Python; use uv build isolation or a project environment.
