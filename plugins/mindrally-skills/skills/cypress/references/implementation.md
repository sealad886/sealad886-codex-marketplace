# Cypress Testing Best Practices: implementation guidance

## Commands and synchronization

Cypress commands are queued and are not ordinary promises to await. Queries and
should assertions can retry; then callbacks run once. Keep retryable callbacks
free of side effects. Register intercepts before the request-triggering action,
wait on aliases when that request is part of the behavior, and assert the outcome.
Use stable test attributes or accessible role/text selectors appropriate to the
contract. Avoid arbitrary time sleeps and selectors coupled to styling.

## Isolation, sessions, and secrets

Keep tests independently runnable and reset relevant server data as well as the
browser state. cy.session caches/restores sessions, not the page; with test isolation
enabled visit the target page afterward. Provide a validate function that proves
the session remains usable. Use a non-secret session identifier instead of putting
passwords in the session ID shown in logs; type secrets with log:false and protect
screenshots/videos and request payloads too. Cross-origin behavior uses the
installed version's documented origin APIs. Distinguish application tests from
third-party provider tests, and do not disable isolation or broaden retries merely
to conceal a state leak.

## Primary documentation

- [Session validation, visible IDs, and post-session navigation](https://docs.cypress.io/api/commands/session).
- [Independent test state and storage scope](https://docs.cypress.io/app/core-concepts/test-isolation).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
