# Python: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Language and interfaces

- Type hints document/check static contracts but do not validate arbitrary runtime input. Use classes/functions according to lifecycle/data needs.
- Async def does not make blocking operations non-blocking; use genuinely async libraries or an appropriate bounded worker boundary.
- Structured tasks need cancellation/timeouts and cleanup; avoid unawaited background work and broad exception swallowing.

## Framework and performance selection

- Django CBV/FBV, FastAPI/Pydantic and Flask factory choices depend on installed versions and app conventions.
- Raw SQL can be appropriate when parameterized and required; ORM use is not a universal correctness proof.
- NumPy/pandas/vectorization/caching are optional workload tools; measure time, memory and invalidation behavior.
- Keep secrets outside source/logs, close files/connections through owned contexts, and test observable success/failure boundaries.

## Primary documentation

- [Primary documentation](https://docs.python.org/3/library/asyncio-task.html) — Python asyncio requires explicit task/cancellation/timeout ownership and does not automatically offload blocking work.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
