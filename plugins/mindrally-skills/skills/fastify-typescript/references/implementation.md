# Fastify TypeScript Development: implementation guidance

## Schemas and types

Fastify validates request data and serializes responses via different compiled
schema systems. A response schema is not the same thing as full runtime response
validation. Schemas are trusted application code; never compile arbitrary user
schemas. Match Ajv/TypeBox/type-provider versions, add complete supported schemas,
and do asynchronous database checks in suitable hooks rather than initial validation.
TypeScript declarations must match decorated properties; type assertions do not
create runtime decorators. Do not mix callback and async completion conventions.

## Encapsulation and errors

Register dependencies before consumers and respect plugin encapsulation; fastify-plugin
changes visibility deliberately. Own database clients and close them with onClose.
Prisma/repository classes/JWT are optional integrations. Prisma dates may not match
a string response interface without serialization; verify actual output schema.
Classify expected errors and mask unexpected 500 messages instead of returning every
error.message from the upstream handler. Choose appropriate structured logging,
redaction, body limits, CORS and rate limits for the trusted proxy topology.
Await ready/inject as needed and close each test app; benchmark the actual flow
instead of promising fastest framework performance.

## Primary documentation

- [Schema compilation, validation and serialization](https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/).
- [Plugin/decorator visibility](https://fastify.dev/docs/latest/Reference/Encapsulation/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
