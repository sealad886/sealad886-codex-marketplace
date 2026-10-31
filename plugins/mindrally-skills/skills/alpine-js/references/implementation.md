# Alpine.js Development: implementation guidance

## Directives and state

Use `x-data` for local state, `x-bind` for attributes, `x-on` for events, and
`x-model` for appropriate form inputs. Extract reused logic with `Alpine.data()`;
use `Alpine.store()` for intentionally shared state. Register before Alpine starts.
`x-show` retains DOM and state while toggling visibility; `x-if` creates/removes
a template subtree. Choose based on lifecycle and cost rather than treating one
as universally faster. Give `x-for` a stable key on its template.

## Integration and safety

Use `x-text` for untrusted text. `x-html` requires trusted or correctly sanitized
HTML. For outside-click dismissal use current `.outside` semantics, and restore
focus appropriately. A visual dropdown is not automatically an ARIA menu.
Keep Tailwind optional. For Livewire, inspect its version and bundled Alpine
first; avoid starting Alpine twice. Prefer the documented `$wire` integration;
do not introduce `@entangle` as a universal binding pattern. Define every referenced
submit/validation method and use native form validation where suitable.

## Primary documentation

- [Outside event modifier and event handling](https://alpinejs.dev/directives/on).
- [Conditional DOM lifecycle](https://alpinejs.dev/directives/if).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
