# gRPC Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Contracts and generation

- Use additive protobuf changes intentionally; never reuse deleted field numbers or names, and reserve removed enum identifiers.
- Use a zero enum default and explicit presence where the schema syntax supports it; choose oneof only for mutually exclusive alternatives.
- File organization and message reuse are design choices, not universal one-entity or one-RPC rules.

## Runtime and reliability

- Reuse channels; add pools only after measuring stream/concurrency limits. A channel need not map permanently to one connection.
- Python async APIs are in grpc.aio from grpcio; grpcio-tools provides code generation, not a separate grpcio-aio package.
- Set deadlines and cancellation propagation; retry only documented retryable outcomes within an idempotency and time budget.
- Use TLS or mTLS as required, authenticate metadata, and authorize each operation; redact request payloads in logs.
- Test generated serialization, real connections, stream cancellation, resource limits, health signals, and trace propagation.

## Primary documentation

- [gRPC Python tutorial](https://grpc.io/docs/languages/python/basics/) — grpcio-tools generates client/server interfaces from protobuf definitions.
- [gRPC AsyncIO API](https://grpc.github.io/grpc/python/grpc_asyncio.html) — grpc.aio exposes asynchronous channels and calls within gRPC Python.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
