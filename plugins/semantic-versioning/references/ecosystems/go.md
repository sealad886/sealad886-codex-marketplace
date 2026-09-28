# Go

Read when module tags or Go binary releases establish versions.

## Sources and ownership

`go.mod` declares module identity and minimum toolchain expectations, not the module release version. Git tags own ordinary module versions. A module at repository root normally uses `v1.2.3`; a module in `tools/widget` uses `tools/widget/v1.2.3`. Validate tags against that module and reachable branch ancestry.

From v2 onward, the module path and consuming imports normally include `/v2` (and subsequent majors). A new major therefore changes more than a tag. Nested modules are separate release units. Shared files and generated code can still affect several modules.

## Example and checks

[Minimal executable](../../examples/go/go.mod). Run `go test ./...`, then `go build -trimpath -ldflags '-X main.version=0.1.0' -o semver-example .`; invoking the binary must print `0.1.0`. This injected display value must derive from the verified release tag rather than becoming a second source.

Inspect `go version -m semver-example`; built binary identity and module tag identity need separate evidence. For GoReleaser, run its native config check and snapshot build before authorized release. Snapshot artifacts are not tagged release evidence. Library consumers should resolve the intended module version and import path in a disposable downstream module.

Private proxies, vendoring, and replace directives affect resolution. Do not mistake a local `replace` for proof a published dependency can be fetched.

## Sources

[Major-version updates](https://go.dev/doc/modules/major-version), [module versions](https://go.dev/doc/modules/version-numbers), [multi-module source](https://go.dev/doc/modules/managing-source), [GoReleaser configuration](https://goreleaser.com/customization/).
