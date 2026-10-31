# Phoenix Framework Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Web and persistence

- Use current HEEx/components or existing generation’s views; LiveView is optional for interactions that benefit from its process model.
- Ecto changesets validate data but do not replace authorization or database constraints.
- Preload/join/select according to query use and verify N+1 and transaction behavior.

## Processes and security

- Let-it-crash means supervised recovery for unexpected process failures, not ignoring invalid input or losing untracked tasks.
- Use Task/Supervisor/GenServer only for a required lifetime/state/concurrency boundary; plain functions remain appropriate.
- LiveView mount and subsequent events need authorization as state/permissions change, not just router authentication.
- Use the app’s supported auth implementation rather than requiring Guardian/Pow; handle reconnect, flash/error and form states accessibly.

## Primary documentation

- [Primary documentation](https://phoenix.hexdocs.pm/live_view.html) — Phoenix LiveView provides server-owned interactive rendering with its own connection/lifecycle behavior.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
