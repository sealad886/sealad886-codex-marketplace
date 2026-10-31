# Python Testing: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Test meaning and isolation

- Signatures/docstrings are evidence, but tests must follow requirements and real behavior rather than merely mirror implementation.
- Use fixture scopes intentionally and teardown owned resources even after setup/test failure.
- Mock where looked up and use interface-aware specs when useful; excessive mocks can hide integration defects.

## Data and coverage

- Use parametrize for distinct behavior cases and Hypothesis when a meaningful invariant benefits from generated counterexamples.
- Control time/randomness/network or record nondeterministic evidence; do not mistake random diversity for useful coverage.
- Coverage locates unexecuted paths but is not a completion target; assertions should fail for the defect or violated invariant.
- Use real-provider integration when semantics matter and clearly report unavailable environments.

## Primary documentation

- [Primary documentation](https://docs.pytest.org/en/stable/how-to/fixtures.html) — pytest fixtures have explicit scopes, dependencies and teardown behavior that determine test isolation.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
