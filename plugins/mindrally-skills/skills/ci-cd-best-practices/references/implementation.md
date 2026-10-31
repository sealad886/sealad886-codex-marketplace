# CI/CD Best Practices: implementation guidance

## Pipelines and artifacts

Provider YAML is not portable: GitLab stages/matrix/rules cannot be pasted into
GitHub or Bitbucket. Declare stages and referenced scripts that actually exist.
Cache package downloads with lockfile/toolchain/OS keys; npm ci recreates
node_modules, so caching that directory may not help. Artifact promotion must bind
the built digest to the verified revision; a branch name alone is insufficient.
Keep untrusted PR code away from privileged credentials, protected caches, and
release artifacts. Prefer short-lived federated identity over encoded keys on disk.
Base64 is not encryption and masking cannot prevent deliberate exfiltration.

## Deployment and failure handling

Blue/green, canary, rolling, and feature flags require application/data compatibility,
health criteria, and a bounded rollback decision. kubectl rollout restart restarts
the current template; it does not select a new version. Kubernetes reports stalled
Deployments but does not automatically roll them back. Implement approved recovery
explicitly and preserve failed status even if rollback succeeds. Database down
migrations can lose data; prefer tested forward/expand-contract recovery where
appropriate. Retries or quarantine cannot silently waive required tests/gates.
Record measured costs and outcomes separately from estimates.

## Primary documentation

- [Deployment progress conditions and explicit rollback](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
- [GitLab provider-specific pipeline schema](https://docs.gitlab.com/ci/yaml/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
