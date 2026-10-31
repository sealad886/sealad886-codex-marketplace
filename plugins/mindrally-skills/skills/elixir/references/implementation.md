# Elixir: implementation guidance

## Data and process design

Use binaries for ordinary UTF-8 strings and ~c sigils for charlists in current
Elixir; old single-quoted charlist syntax is version-dependent/deprecated guidance.
Prefer small cohesive functions, pattern matches/guards and explicit tagged errors.
Supervision handles unexpected process failure; let-it-crash does not excuse
unvalidated input, lost work, or repeated external effects. GenServer is for stateful
process responsibilities, not an automatic wrapper for every module or function.
Set timeouts and backpressure for calls, tasks, pools and message queues.

## Phoenix and persistence

Contexts expose domain behavior; Ecto changesets cast/validate input while database
constraints and authorization remain necessary. Use preload/query planning to
address actual N+1, and verify transaction/error semantics. ETS/Redis caches need
ownership, lifetime, concurrency and invalidation design. LiveView and Tailwind
are optional project choices, not language requirements. Use the application's
existing supported authentication approach instead of introducing Guardian/Pow
by default. Test supervision/restarts, resource cleanup and meaningful client state,
with a clear distinction between unit and live integration evidence.

## Primary documentation

- [Binaries and current charlist syntax](https://elixir.hexdocs.pm/binaries-strings-and-charlists.html).
- [Supervision behavior](https://hexdocs.pm/elixir/Supervisor.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
