# Jest Testing Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Mocks and module systems

- jest.fn creates mocks, spyOn wraps existing methods unless reconfigured, and jest.mock behavior depends on module/transform setup.
- clearAllMocks clears usage history; resetAllMocks also resets mock implementations; restoreAllMocks restores supported spies/replaced properties.
- Restore owned spies after tests and use the configured ESM mocking approach rather than assuming CommonJS hoisting.

## Async and assertions

- Return or await promises, including rejects/resolves assertions; use expect.assertions when it proves an otherwise skipped callback path.
- Choose fake timers only for time-controlled behavior and restore real timers after use; flush pending async work deliberately.
- Assert observable outputs and important boundary interactions; keep snapshots small and intentional.
- Meaningful success, failure and boundary cases matter more than raw coverage percentages.

## Primary documentation

- [Jest object API](https://jestjs.io/docs/jest-object) — clearAllMocks, resetAllMocks, and restoreAllMocks have different effects.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
