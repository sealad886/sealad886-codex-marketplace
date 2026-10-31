# GitLab Workflow Best Practices: implementation guidance

## Pipelines and rules

Use workflow:rules and job rules to control push/MR/schedule sources without
unintended duplicate pipelines. Rules evaluate before jobs, so later dotenv values
cannot choose whether a job exists. Jobs have isolated runtimes; declare dependencies,
services and artifacts. npm ci rebuilds node_modules, so use a useful lockfile-bound
package cache rather than assuming that folder saves work. Test sharding syntax
belongs to the selected runner. Security templates and job names depend on GitLab
version/tier; inspect expanded includes rather than creating empty jobs with guessed
names or putting inherited test-stage jobs in an undeclared stage.

## Credentials, environments and reviews

Masked/protected variables have precise scope and masking limits; the upstream YAML
empty variable declaration does not configure secret masking/protection. Avoid
secrets in untrusted MR/fork jobs, use narrow job tokens/OIDC where supported, and
verify protected environment approvals. Auto DevOps may build, provision and deploy;
do not enable it as a harmless local setup step. Bind review and pipeline results
to MR-head/merged-result/merge-train identities, and preserve required gates. Issue
commands, labels, settings, deploys and deletion need user authority. Hosted scans
and plan-specific features are not supplied by this skill.

## Primary documentation

- [Rule timing and duplicate pipelines](https://docs.gitlab.com/ci/jobs/job_rules/).
- [Variable protection/masking and trust boundaries](https://docs.gitlab.com/ci/variables/).
- [Expanded CI schema and includes](https://docs.gitlab.com/ci/yaml/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
