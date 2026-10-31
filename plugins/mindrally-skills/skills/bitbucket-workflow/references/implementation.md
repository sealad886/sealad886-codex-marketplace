# Bitbucket Workflow Best Practices: implementation guidance

## Pull requests and pipelines

Follow the repository branch and title convention rather than imposing Gitflow
or Jira. Bitbucket Cloud Pipelines uses bitbucket-pipelines.yml; Data Center does
not have identical features. Every step needs its own runtime/dependencies and
can consume declared artifacts/services. npm scripts use npm run for custom
names; npm test:unit in the upstream parallel sample is not that syntax.
Include lockfiles and configuration in relevant changeset rules so dependency
changes do not silently skip validation. Use supported images and pinned reviewed
pipes; old example tags are not current recommendations.

## Identity, integrations, and gates

Prefer scoped short-lived OIDC credentials where the configured provider supports
them; validate issuer/audience/subject restrictions. Secured variables mask some
logs but are not protection against untrusted pipeline code or process-argument
exposure. Production environment restrictions and merge checks depend on actual
product/plan settings. Jira Smart Commits and automation require configured links
and explicit authority; a key in a branch name does not prove issue state changed.
Do not assume CODEOWNERS-style patterns or third-party ecosystem automation are
native features. Settings, messages, approvals, and deployments require task authority.

## Primary documentation

- [Pipeline step services, runtime and OIDC options](https://support.atlassian.com/bitbucket-cloud/docs/step-options/).
- [OIDC integration and claims](https://support.atlassian.com/bitbucket-cloud/docs/integrate-pipelines-with-resource-servers-using-oidc/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
