# Microsoft Dynamics 365 Business Central Development: implementation guidance

## AL language and data

AL is object-based; it does not provide ordinary C#/Java try-catch syntax. Use
Error/ErrorInfo and documented TryFunction behavior when appropriate, checking
return values deliberately. Database writes inside try methods have special
limitations and rollback behavior; never assume a caught error rolls back all
writes. Keep transactions and commits explicit. Use table/page extensions and
events rather than altering base application objects. Permission sets and data
classification are part of the application contract.

## Performance and validation

Use filters, appropriate keys, partial records, query objects, and set-based
operations where their semantics fit. Table relations are integrity/lookup
metadata, not a generic query optimization. FlowFields/FlowFilters need correct
CalcFields/CalcFormula behavior and can still be expensive. Background job queues
have separate session and retry constraints; UI Confirm/Message calls may be
invalid in background/web-service contexts. Test codeunits use platform test
libraries/assertions; do not assume a universal built-in assertion language.
Validate upgrade code/data migrations, extension dependencies, and assigned ID
ranges before any authorized publishing or tenant change.

## Primary documentation

- [TryFunction and database-write semantics](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-handling-errors-using-try-methods).
- [AL language/object model](https://learn.microsoft.com/dynamics365/business-central/dev-itpro/developer/devenv-programming-in-al).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
