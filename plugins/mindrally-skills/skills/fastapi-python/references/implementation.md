# FastAPI Python: implementation guidance

## Validation and execution

Use Pydantic models and constraints compatible with the installed version; Python
type hints alone do not validate arbitrary helper calls. Response models can filter
output but do not replace resource authorization. Use HTTPException for intended
HTTP failures and safe exception handling for internal failures. Python conditionals
have no optional curly braces: the upstream instruction was imported from another
language. Do not force one-line conditionals or RO-RO on idiomatic Python.

## Async and lifetime

A normal def path operation/dependency is dispatched through the documented thread
pool; calling a blocking helper directly inside async def still blocks the event
loop. Choose async clients or an appropriate offload boundary instead of a blanket
all-database-calls-async mandate. Lifespan context managers own startup/shutdown
resources; yield dependencies have version-specific cleanup timing. In-process
background tasks are suitable only for their supported lifetime/reliability scope.
Avoid unbounded list loading, user-shared caches and secret-bearing logs. SQLAlchemy,
asyncpg, Redis and MySQL drivers are task choices, not required FastAPI dependencies.

## Primary documentation

- [Threadpool and awaited coroutine execution](https://fastapi.tiangolo.com/async/).
- [Lifespan context management](https://fastapi.tiangolo.com/advanced/events/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
