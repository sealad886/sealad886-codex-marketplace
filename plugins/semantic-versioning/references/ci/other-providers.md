# Other CI providers and additional packaging recipes

Read only when GitHub Actions is not the target or the package family has no full hosted template. These are adaptation recipes, not validated provider deployments.

Preserve the same invariant on GitLab CI, Azure Pipelines, CircleCI, Buildkite or Forgejo: approved source SHA and release unit enter a protected publishing job; that job verifies native package metadata, writes immutable artifacts, and records registry evidence. Map protected branches/environments, manual gates, concurrency/resource locks, artifacts, and identity to the provider's native features. Do not copy GitHub token names or assume OIDC is supported by every registry/provider pair. Separate untrusted PR checks from credentialed jobs.

- **GitLab:** use protected environments/variables and resource groups; check registry-specific OIDC audience and claims. [GitLab deployment safety](https://docs.gitlab.com/ci/environments/deployment_safety/).
- **Azure Pipelines:** use protected service connections and environment approvals; scope secrets to deployment jobs. [Azure approvals](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals).
- **CircleCI:** restrict contexts and release workflows; check registry trust requirements. [CircleCI contexts](https://circleci.com/docs/contexts/).
- **Buildkite/Forgejo:** confirm the installed server/runner version and provider documentation before relying on GitHub-compatible syntax or identity semantics.

## Additional recipes

| Family | Native validation and packaging | Publication boundary |
|---|---|---|
| Swift package | Tag the exact tested commit; run `swift test`; inspect tools-version and public API impact. | Immutable Git tag is the package release. |
| Apple application | Validate marketing version separately from monotonic build number; archive with pinned Xcode; inspect embedded metadata/signing. | Signing, notarization, TestFlight/App Store upload and rollout require their own authority. |
| Android / Flutter | Verify versionName/versionCode or Flutter `version: x.y.z+build`; build signed bundles through existing Gradle/Flutter pipeline. | Store credentials, upload, review and rollout remain separate from version calculation. |
| Ruby | Run tests and `gem build`; read gem metadata; retain checksum; prefer supported RubyGems trusted publishing. | Publish exact `.gem`, then read back gem/version/platform. [RubyGems publishing](https://guides.rubygems.org/publishing/). |
| PHP | `composer validate --strict`; test supported PHP constraints; verify package name and immutable source tag. | Packagist synchronization is distinct from creating a Git tag. [Composer libraries](https://getcomposer.org/doc/02-libraries.md). |
| C/C++ | Build/test supported ABI targets; compare library ABI/SOVERSION separately; generate Conan/vcpkg/native archives from the approved source. | Package recipe/version/revision and binary ABI are separate identities. |
| Codex plugin | Validate manifest, skills, package archive, root-relative references and catalog source. | Publish immutable artifact first; activate catalog only after artifact readback. Plugin runtime compatibility and marketplace cache identity are separate from SemVer. |

Every recipe needs the project's actual account, package identifiers, supported compiler/tool versions, authentication method, artifact checks and rollback policy before becoming a complete deployment workflow.
