---
name: rspec
description: "Use when designing or maintaining RSpec examples, test data, shared behaviors, doubles, or Ruby/Rails regression coverage."
---

# RSpec behavioral tests

## When to invoke

Use when designing or maintaining RSpec examples, test data, shared behaviors, doubles, or Ruby/Rails regression coverage.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect RSpec/Ruby versions, spec helpers, database isolation, existing factories/fixtures, and the requirement under test.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. State the observable behavior and smallest reliable test boundary.
2. Create minimal independent data and clear examples using project conventions.
3. Run focused examples, then relevant wider tests and order/random-seed checks when isolation is affected.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run the changed examples and relevant suite, reporting actual failures and any seed or database-isolation evidence.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
