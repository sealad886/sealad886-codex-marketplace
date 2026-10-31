# Storybook component evidence: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use framework-specific Meta/StoryObj imports and supported CSF syntax for the installed major; do not mix addon APIs from several generations.

- Current Storybook interaction utilities come from storybook/test; older @storybook/jest and @storybook/testing-library examples are version-specific.

- Use explicit callback spies such as fn() for assertions; an action logger is not always an assertable spy.

- Use accessible role/label queries and await user interactions/expectations where supported. A click does not guarantee focus on every platform/control.

- Provide real providers/router fixtures through decorators without network writes or shared cross-story state.

- Represent loading, error, empty, disabled, long-content, and supported theme/viewport states that matter to the contract.

- Addon packaging/background/viewport configuration changes by major; retain only installed supported addons rather than copying an essential-addons list.

- Automated accessibility checks and visual snapshots have limits; verify keyboard/focus and critical integration behavior separately.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Current interaction examples use storybook/test utilities and explicit fn callback spies.](https://storybook.js.org/docs/writing-tests/interaction-testing)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
