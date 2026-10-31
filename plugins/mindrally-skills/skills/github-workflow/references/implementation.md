# GitHub Workflow Best Practices: implementation guidance

## Reviews and metadata

Use focused PRs and the repository template; fixed line counts or one universal
approval count are not correctness gates. Bind reviews, statuses and test-merge/
merge-group checks to their exact revisions. Silence, skipped reviews or old green
checks do not prove approval of new content. CODEOWNERS requests depend on actual
configuration and ownership; do not invent teams/assignees. Issue-closing keywords
have branch/context semantics and externally change issue state when effective.
Posting comments, requesting reviews, changing settings or merging needs task authority.

## Actions and release automation

Pin reviewed actions to verified full SHAs, choose supported toolchains, set timeouts,
and minimize GITHUB_TOKEN/secrets scope. Do not execute untrusted PR checkout or
artifacts in a privileged pull_request_target/workflow_run context. Treat event
strings as untrusted data and pass them through safe arguments/env. Validate cache
and artifact trust and prefer scoped OIDC when configured. The upstream Dependabot
example says minor updates but checks only actor, so it could auto-merge major
updates: verify package/update metadata plus existing gates, and never enable
blanket auto-merge implicitly. Release tools/settings are optional and need authority.

## Primary documentation

- [Actions trust, SHA pinning and token scope](https://docs.github.com/en/actions/reference/security/secure-use).
- [Dependabot metadata and automation](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/automating-dependabot-with-github-actions).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
