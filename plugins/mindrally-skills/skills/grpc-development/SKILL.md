---
name: grpc-development
description: "Use when defining protobuf contracts, implementing gRPC unary or streaming services, deadlines, authentication, or observability."
---

# gRPC Development

## When to invoke

Use for gRPC clients and services across supported languages.

## Inputs and evidence

Inspect .proto files, protoc/plugins and generated-code versions, transport credentials, RPC semantics, retry policy, and message limits. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose unary, server, client, or bidirectional streaming from the actual interaction contract.
2. Update protobuf definitions and regenerate with the repository toolchain; reserve removed field identifiers.
3. Implement bounded deadlines, cancellation, credentials, and status mapping on both sides.
4. Exercise real RPC transport and streaming teardown before proposing deployment.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Generated stubs build, RPC success/error paths pass, and deadline, cancellation, stream backpressure, and authorization behavior are checked.

## Must not

Do not retry non-idempotent writes blindly or present illustrative insecure servers as production configurations. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
