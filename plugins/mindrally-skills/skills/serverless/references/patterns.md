# Serverless execution contracts: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- FastAPI requires an appropriate platform adapter or container/runtime entrypoint; it is not automatically a Lambda binary.

- Keep durable state external while safely reusing connections/clients across warm invocations; never retain user-specific request data globally.

- Assume duplicates according to the event source; make writes idempotent and use supported partial-batch failure semantics.

- Do not launch background tasks that must outlive function completion; use durable queues/workflows and bounded retries/dead letters.

- Async handlers only help when downstream APIs are nonblocking and the platform supports them.

- Scale-out can exhaust database pools or third-party quotas; bound concurrency and use supported connection management.

- Gateways, service meshes, Redis, Celery, Kafka, CQRS, and microservices are optional architectural choices, not serverless prerequisites.

- Separate configuration/build validation from cloud deployment, provisioning, billable load tests, and IAM changes requiring authority.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Lambda guidance requires duplicate-aware idempotent handlers and resource-aware implementation.](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
