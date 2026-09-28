# Semantic Versioning

Version 0.1.0 — development candidate, unavailable in the marketplace pending release validation.

Help agents assess changes throughout development, maintain native release intent, configure release PRs and verify publication. This package is independent: no MCP server, daemon, telemetry, hooks, or other plugin is required. Helpers require Python 3.11+; native build/release tools are needed only for the selected project.

## Start here

- [Assess code changes](skills/semantic-versioning/SKILL.md): release units, contracts, cumulative impact and correct version ownership.
- [Configure releases](skills/configure-releases/SKILL.md): native automation, CI examples and scoped migrations.
- [Verify or recover a release](skills/verify-release/SKILL.md): exact source/package identity, remote state and consumer checks.

Load the skill and only its relevant references. Each skill stays below 900 words. [Opt-in repository instructions](templates/agent-instructions.md) help make assessment part of coding work; installation alone cannot guarantee invocation.

## Read-only tools

From this package directory:

```sh
python3 scripts/inspect_repository.py /path/to/project --json
python3 scripts/inspect_repository.py /path/to/project --scope packages/library
python3 scripts/check_version.py validate 1.2.3 2.0.0-rc.1
python3 scripts/check_version.py compare 1.2.3 1.3.0
python3 scripts/check_version.py check 1.2.3 1.3.0 --impact minor --json
```

Both tools emit schema_version 1 JSON with `--json`. Exit 0 means success; 1 means a failed contract check; 2 means invalid input or an operational error. Discovery reports candidate evidence and unresolved dynamic configuration; it does not execute project files, fetch Git history, install dependencies, or decide semantic impact. Version checks implement SemVer arithmetic, not ecosystem range resolution or ABI analysis. A prerelease baseline permits only same-core iteration or promotion; assess new cumulative impact against the preceding stable baseline.

## Reference library

[Core rules](references/core.md), [release architectures](references/architectures.md), [recovery](references/recovery.md), and [policy worksheet](templates/release-policy.md) separate general decisions from ecosystem detail.

| Ecosystem | Guide | Examples |
|---|---|---|
| JS/TS | [JavaScript](references/ecosystems/javascript.md) | [Projects](examples/javascript/) |
| Python | [Python](references/ecosystems/python.md) | [Projects](examples/python/) |
| Rust | [Rust](references/ecosystems/rust.md) | [Workspace](examples/rust/) |
| Go | [Go](references/ecosystems/go.md) | [Module](examples/go/) |
| Java/Kotlin | [JVM](references/ecosystems/jvm.md) | [Projects](examples/jvm/) |
| .NET | [.NET](references/ecosystems/dotnet.md) | [Project](examples/dotnet/) |
| Swift/mobile | [Mobile](references/ecosystems/mobile.md) | [Definitions](examples/mobile/) |
| C/C++ | [C/C++](references/ecosystems/cpp.md) | [Definitions](examples/cpp/) |
| Ruby/PHP | [Ruby/PHP](references/ecosystems/ruby-php.md) | [Definitions](examples/ruby-php/) |
| OCI/Helm/plugins | [Distribution](references/ecosystems/containers-plugins.md) | [Definitions](examples/containers-plugins/) |

[GitHub CI guide](references/ci/README.md) explains inactive workflow templates and their prerequisites. Consumer workflows must be deliberately installed and configured under authority; nothing here publishes this marketplace automatically.

## Evidence and maintenance

Run repository plugin, distribution and marketplace validators and the semantic-versioning test suite. See the repository validation report for actual commands and limitations. Every template must distinguish static/native validation from hosted publication. Refresh source links, action pins and tool compatibility together when changing recipes. Never claim support for an untested tool version from a current URL alone.

The public contract includes skill responsibilities, helper CLI/JSON behavior, and documented template behavior. Follow SemVer for changes to that contract. Release identity is `semantic-versioning-v0.1.0`; no such release is created by this implementation. Catalog activation, signing, publication, installation and consumer verification are separate authorized steps.

Original code, prose and SVG artwork, copyright 2026 Andrew Cox, MIT licensed. Upstream references inform examples; no third-party implementation is bundled.
