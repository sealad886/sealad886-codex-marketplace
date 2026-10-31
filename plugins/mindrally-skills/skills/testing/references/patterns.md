# Behavioral regression testing: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Test observable behavior and stable contracts rather than every exported function or private implementation detail.

- Choose unit, integration, or end-to-end layers by the failure being prevented; excessive mocks can hide broken interactions.

- Use factories, fixtures, or inline data according to the task and existing tools; no single data-generation method is universally better.

- Control time, randomness, files, and network where determinism matters; keep independent tests isolated and release owned resources.

- Parallel tests require isolated databases, ports, users, and global state; do not enable concurrency merely to shorten reported runtime.

- Use clear framework assertions that explain the invariant; generic assertions remain appropriate where they are the framework idiom.

- Coverage measures executed code, not correctness. Add tests for requirements and known failure modes rather than percentage alone.

- Keep broad snapshots only for intentional representation contracts; prefer focused assertions that survive reasonable refactoring.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Tests should resemble real usage and focus on user-observable behavior.](https://testing-library.com/docs/guiding-principles/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
