---
name: jwt-security
description: "Use when implementing JWT issuance, validation, key rotation, refresh tokens, or token storage."
---

# JWT Security

## When to invoke

Use for implementing JWT issuance, validation, key rotation, refresh tokens, or token storage.

## Inputs and evidence

Inspect token purpose/profile, issuer and audience, trusted algorithms/keys, library versions, required claims, clock policy, and revocation model. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define a token-specific validation policy and trusted key source before parsing untrusted inputs.
2. Use the maintained verifier with explicit algorithm/key constraints and required-claim checks.
3. Implement bounded lifetimes, secure transport/storage, and atomic refresh/revocation behavior.
4. Test missing, malformed, expired, wrong-audience, wrong-key, and replayed tokens.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Tests cover the profile’s accepted token and each rejection/rotation boundary with no sensitive token output.

## Must not

Do not accept an unverified decoded payload as identity or authorization. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
