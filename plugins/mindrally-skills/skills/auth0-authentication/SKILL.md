---
name: auth0-authentication
description: "Use when integrating Auth0 login, API token validation, sessions, Actions, refresh rotation, or MFA."
---

# Auth0 Authentication

## When to invoke

Use when integrating Auth0 login, API token validation, sessions, Actions, refresh rotation, or MFA. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect application type and SDK version, tenant settings, callback allowlist, API audience/scopes, and session policy. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Choose the application-appropriate OIDC/OAuth flow and keep public and confidential client configuration separate.
2. Implement SDK-managed login/session/token handling and server-side resource authorization with approved tenant changes.
3. Check redirect rejection, token issuer/audience/signature/expiry, denied scopes, logout, refresh reuse, and MFA failures.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
