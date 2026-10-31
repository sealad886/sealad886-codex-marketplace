# Flask Python Development: implementation guidance

## Flask core and contexts

Application factories and blueprints help appropriate projects, but Flask-RESTful,
SQLAlchemy, Migrate, Marshmallow and JWT extensions are optional. Choose supported
versions already in use rather than installing every named extension. Python does
not have JavaScript named-export rules or optional conditional curly braces.
Use request/app contexts for their scoped lifetime, not to share private request
state globally. Validate content type/body size, fields and output serialization;
protect cookie-authenticated state changes from CSRF and enforce resource ownership.

## Async, tasks, and deployment

Flask async support depends on its installed extras/extensions. Under normal WSGI,
an async view still occupies one worker; adding async does not automatically raise
request concurrency or make CPU work nonblocking. Spawned background tasks can be
cancelled when the request event loop ends; use the established durable task system
for required asynchronous work. Own database transactions and teardown without
hiding failures. Cache keys must respect users/permissions and invalidation.
Use an appropriate production server, not the development debugger/server, and
verify proxy, secret/session, logging and TLS configuration for the actual host.

## Primary documentation

- [Async support and background-task lifetime](https://flask.palletsprojects.com/en/stable/async-await/).
- [Application factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
