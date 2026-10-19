# Reduce state and control-flow complexity

Use for interacting flags, redundant stored values, nested decisions, or unclear
transitions. Establish the accepted behavior before choosing a representation.
An enum, guard clause, or derived value is useful only when it removes concepts
and preserves a required distinction.

## Map decisions before editing

1. Identify each state writer, reader, transition trigger, and externally visible
   effect. Include persisted state, subscriptions, retries, task completion and
   cancellation callbacks. A local search cannot establish external consumers.
2. List reachable combinations and the required result for each consequential
   input. Separate impossible states proved by a contract from states merely
   absent in current tests. A timing-dependent combination can be rare and valid.
3. Distinguish facts from cached/derived values. A value is safely derived only
   if its source, observation time, consistency and cost satisfy the same
   contract. A snapshot and a live getter can intentionally disagree.
4. Choose the smallest useful change: remove a repeated condition, name one
   decision, derive one redundant field, flatten a branch, or represent mutually
   exclusive states directly. Do not introduce a state-machine framework for
   a few ordinary conditions.

For asynchronous ownership, a table like this can expose a missing distinction.
These are example states, not requirements to impose on every system:

| State | Resource ownership | Event | Required distinction |
| --- | --- | --- | --- |
| Idle | No operation owned | Start accepted | Establish one owner |
| Running | Task/handle still owned | Cancellation requested | Request cancellation once; do not report cleanup finished |
| Cancelling | Cleanup may still be pending | Completion/finally runs | Release resources before entering the terminal state |
| Cancelled | No operation remains owned | New start | Follow the accepted restart policy |

Replacing `is_running` and `cancel_requested` with a single `cancelled` flag can
erase the distinction between requested cancellation and completed cleanup.
Keep the transition or another explicit ownership mechanism until the required
release condition is established. Likewise, an error can coexist with stale
display data when the product permits it; do not force independent facts into
one mutually exclusive state.

## Flatten without moving effects

For each proposed guard clause, check:

- Does it preserve which expressions run, their order and evaluation count?
- Does it preserve lazy evaluation, including validation or I/O only reached
  after a prior condition succeeds?
- Does an early return cross a transaction, lock, deferred action or `finally`
  boundary whose behavior matters?
- Are absence, false, zero and an empty collection distinct accepted values?
- Can moving a read turn a snapshot into a later mutable observation?

For example, `ready and expensive_check()` does not call `expensive_check` when
`ready` is false. Hoisting the check before the guard changes behavior. A cached
empty result can also be valid: replacing `cached is not None` with `if cached`
changes the branch taken for empty results. Use the actual language's semantics
and current project version when assessing a concrete rewrite.

Avoid flattening into a long boolean expression that hides error policy or
resource ownership. Prefer a named local decision only when the name expresses
the domain rule; another forwarding helper need not improve the flow.

## Verify the transitions that matter

Exercise representative success, rejection, failure and interruption paths at
the stable boundary. For the ownership example, verify start → running → cancel
request → cleanup → terminal state, including completion racing with cancellation
when the contract permits it. Check that derived state is consistent at the
point consumers observe it.

Compare outputs, errors, effects and resource ownership before/after. Tests should
protect these behaviors, not pin the new enum names or branch structure. Report
unavailable timing/runtime evidence as a limit. A smaller decision table or fewer
stored flags supports a maintainability claim; it does not prove a speed gain.
