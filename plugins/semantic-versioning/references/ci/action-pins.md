# Action pin evidence

Read when maintaining workflow dependencies. Resolved using GitHub REST `repos/{owner}/{repo}/commits/{ref}` on 2026-09-28. These are immutable snapshots of the named upstream compatibility lines, not a guarantee of newest release or a hosted security audit. Review changes and re-run workflow checks before updating.

| Action | Upstream ref | Resolved commit |
|---|---|---|
| [actions/checkout](https://github.com/actions/checkout) | `v4` | [`11d5960a326750d5838078e36cf38b85af677262`](https://github.com/actions/checkout/commit/11d5960a326750d5838078e36cf38b85af677262) |
| [actions/setup-dotnet](https://github.com/actions/setup-dotnet) | `v4` | [`67a3573c9a986a3f9c594539f4ab511d57bb3ce9`](https://github.com/actions/setup-dotnet/commit/67a3573c9a986a3f9c594539f4ab511d57bb3ce9) |
| [actions/setup-go](https://github.com/actions/setup-go) | `v5` | [`40f1582b2485089dde7abd97c1529aa768e1baff`](https://github.com/actions/setup-go/commit/40f1582b2485089dde7abd97c1529aa768e1baff) |
| [actions/setup-java](https://github.com/actions/setup-java) | `v4` | [`cf277c60eb25467037889841efdb72551f06f6c3`](https://github.com/actions/setup-java/commit/cf277c60eb25467037889841efdb72551f06f6c3) |
| [actions/setup-node](https://github.com/actions/setup-node) | `v4` | [`49933ea5288caeca8642d1e84afbd3f7d6820020`](https://github.com/actions/setup-node/commit/49933ea5288caeca8642d1e84afbd3f7d6820020) |
| [actions/setup-python](https://github.com/actions/setup-python) | `v5` | [`a26af69be951a213d495a4c3e4e4022e16d87065`](https://github.com/actions/setup-python/commit/a26af69be951a213d495a4c3e4e4022e16d87065) |
| [actions/upload-artifact](https://github.com/actions/upload-artifact) | `v4` | [`ea165f8d65b6e75b540449e92b4886f43607fa02`](https://github.com/actions/upload-artifact/commit/ea165f8d65b6e75b540449e92b4886f43607fa02) |
| [azure/setup-helm](https://github.com/azure/setup-helm) | `v4.3.0` | [`b9e51907a09c216f16ebe8536097933489208112`](https://github.com/azure/setup-helm/commit/b9e51907a09c216f16ebe8536097933489208112) |
| [changesets/action](https://github.com/changesets/action) | `v1` | [`a45c4d594aa4e2c509dc14a9f2b3b67ba3780d0d`](https://github.com/changesets/action/commit/a45c4d594aa4e2c509dc14a9f2b3b67ba3780d0d) |
| [googleapis/release-please-action](https://github.com/googleapis/release-please-action) | `v4` | [`5c625bfb5d1ff62eadeeb3772007f7f66fdcf071`](https://github.com/googleapis/release-please-action/commit/5c625bfb5d1ff62eadeeb3772007f7f66fdcf071) |
| [goreleaser/goreleaser-action](https://github.com/goreleaser/goreleaser-action) | `v6` | [`e435ccd777264be153ace6237001ef4d979d3a7a`](https://github.com/goreleaser/goreleaser-action/commit/e435ccd777264be153ace6237001ef4d979d3a7a) |
| [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) | `release/v1` | [`dc37677b2e1c63e2034f94d8a5b11f265b73ba33`](https://github.com/pypa/gh-action-pypi-publish/commit/dc37677b2e1c63e2034f94d8a5b11f265b73ba33) |

Validation performed during development: every template materialized as `.yml` in a temporary directory; coordinator separately paired with each of the eight reusable publishers; actionlint 1.7.12 passed for all eight pairs and both standalone alternatives. No credentialed publication, deployment, registry setup, or GitHub release was performed.
