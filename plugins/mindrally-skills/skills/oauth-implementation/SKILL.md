---
name: oauth-implementation
description: "Use when implementing OAuth authorization-code and PKCE flows, OIDC sign-in, token exchange, scopes, or refresh behavior."
---

# OAuth Implementation

## When to invoke

Use for implementing OAuth authorization-code and PKCE flows, OIDC sign-in, token exchange, scopes, or refresh behavior.

## Inputs and evidence

Inspect provider discovery/profile, client type, redirect registration, library version, state/nonce/PKCE handling and token audience/storage policy. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Select the provider-supported current secure flow and distinguish authorization from authentication.
2. Generate and bind single-use transaction state and PKCE to the initiating client/session.
3. Use a maintained library to exchange/validate responses and enforce resource scopes/audience.
4. Test missing/mismatched/replayed state, bad issuer/redirect, denied consent and refresh failure.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Provider/library tests cover successful flow plus denial, injection, replay, token and transaction-binding rejection paths.

## Must not

Do not implement custom cryptographic/protocol validation where maintained supported libraries exist. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
