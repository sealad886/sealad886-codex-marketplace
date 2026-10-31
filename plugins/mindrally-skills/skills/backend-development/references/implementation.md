# Backend Development: implementation guidance

## C++ path

Use values and RAII for owned resources. unique_ptr represents exclusive heap
ownership, shared_ptr only genuine shared lifetime, and raw pointers/references
can be non-owning observers. Prefer const-correct APIs and avoid unnecessary heap
allocation. Use optional/variant and language features supported by the target
standard. std::move is a cast enabling moves; it does not guarantee movement and
can harm return-value optimization when added indiscriminately. Follow the existing
exception/status policy and preserve exception safety at external boundaries.

## Elixir/Phoenix path

Group domain APIs in contexts without automatically imposing domain-driven layers.
Use tagged tuples and with for expected failures; supervise processes for fault
recovery. Let-it-crash is not permission to ignore invalid user input or retry
non-idempotent effects. Ecto changesets model validation/casting but authorization
and database constraints remain separate. LiveView/function components suit some
UIs; do not replace an established API or client architecture merely to adopt them.
Test context contracts, transactions, process recovery, and user-facing errors.

## Primary documentation

- [Resource ownership and RAII](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).
- [Phoenix context boundaries](https://hexdocs.pm/phoenix/contexts.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
