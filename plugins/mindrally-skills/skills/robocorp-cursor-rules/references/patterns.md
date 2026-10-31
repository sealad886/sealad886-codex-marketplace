# Robocorp Python automation: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- The documented robocorp-tasks entrypoint is a function decorated with `@task`; use runner-supported signatures rather than inventing a generic dependency-injection contract.

- Use synchronous or asynchronous APIs according to the actual library; declaring async does not make a blocking RPA/database operation nonblocking.

- Use Python functions, classes, and context managers where useful. React-style functional components, middleware, and named exports are not Robocorp requirements.

- Validate work item inputs and keep output files and artifact paths predictable; use Pydantic only when already present or justified.

- Resolve secrets through the supported vault/configuration mechanism and prevent logging of credentials and personal work-item contents.

- Browser/UI tasks need selectors, bounded waits, screenshots appropriate to privacy, and explicit failure reporting.

- Make externally visible actions idempotent or detect already-completed steps before retrying; distinguish read-only inspection from form submission or messages.

- Run the project’s configured task command in its environment and report runner/library differences instead of assuming an exception type exists.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [robocorp-tasks uses decorated Python task functions and a task runner.](https://sema4.ai/docs/automation/python/robocorp/robocorp-tasks)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
