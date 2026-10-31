# GCP Development Best Practices: implementation guidance

## Runtime and data services

Cloud Run containers must obey the current port/listen/startup/shutdown contract;
request-lifetime background work and concurrency need explicit policy. The upstream
Dockerfile never builds TypeScript before launching dist/index.js: include a real
build and only required runtime files. Select supported base/runtime versions,
not dated Node 20/provider pins by default. Firestore FieldValue is a separate
SDK export in current Node usage, not Firestore.FieldValue. Transactions may retry,
so keep external effects out of callbacks and enforce server-side authorization.
BigQuery parameters protect values, not arbitrary identifiers; bound scanned data
and review query plans/partitions. Storage signed URLs are temporary bearer access;
restrict scope/lifetime and validate upload content/ownership.

## Infrastructure, telemetry, and operations

Use existing IaC and locked providers with protected remote state; Terraform
workspaces alone are not complete environment/account isolation. Prefer workload
identity and scoped service accounts to keys. Missing secrets should fail clearly,
not silently become empty strings. Budgets/alerts are not hard spending caps, and
reservations are financial commitments. Cloud Debugger shut down in 2023; do not
recommend it for production debugging. OpenTelemetry processor setup depends on
installed SDK generation; initialize it before instrumented libraries and redact
traces. Deployments, traffic shifts, lifecycle deletions and settings need authority.

## Primary documentation

- [Cloud Debugger shutdown](https://docs.cloud.google.com/stackdriver/docs/deprecations/debugger-deprecation).
- [Cloud Run runtime contract](https://cloud.google.com/run/docs/container-contract).
- [Firestore SDK classes and transaction APIs](https://cloud.google.com/nodejs/docs/reference/firestore/latest).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
