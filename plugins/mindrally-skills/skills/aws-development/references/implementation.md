# AWS Development Best Practices: implementation guidance

## Compute and storage

Choose ARM64 only after dependencies and workload benchmarks support it; TypeScript
is optional. Confirm supported runtime lifecycle instead of copying nodejs20.x.
Use SDK clients outside repeated handler work where safe, but never retain private
request state across invocations. Match API Gateway event versions to handler types.
For duplicate events, use durable idempotency keys and safe state transitions.
Design DynamoDB keys/GSIs around actual access patterns; single-table design is a
choice. Handle pagination, unprocessed batch items, conditional writes, and index
consistency. Confirm backup/restore requirements before changing table settings.

## Infrastructure and operations

Import CDK Construct from constructs; aws-cdk-lib subpaths use documented hyphens
(e.g. aws-lambda), not the upstream aws_lambda spelling. Review synth/diff and
SAM validation without treating them as deployment permission. IAM resources
should use the narrow account, region, table/index ARNs required. API Gateway
API keys/usage plans are not authentication or reliable hard spending limits.
Use workload roles and approved secret stores. Step Functions retry behavior and
Standard/Express execution semantics differ; bound retries and compensate side
effects. Mock SDK tests are unit tests, not real AWS integration evidence.

## Primary documentation

- [Lambda runtime and idempotency practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html).
- [CDK v2 modules and Construct ownership](https://docs.aws.amazon.com/cdk/api/v2/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
