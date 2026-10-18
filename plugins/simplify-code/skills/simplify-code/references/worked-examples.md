# Worked simplification examples

These illustrate decisions, not automatic rewriting rules.

## Remove a forwarding wrapper

```python
def load_settings(path):
    return parse_settings(path)
```

If `load_settings` is internal, has no distinct contract, and registration/export
checks show all callers can use `parse_settings`, redirect them and delete the
wrapper. Verify required outputs and errors at the surviving public boundary.

Retain or deliberately migrate the name if it is a documented external API,
framework callback, CLI entrypoint, or meaningful domain boundary. One line does
not establish redundancy; ownership and contract do.

## Keep a resource boundary

```python
def read_record(path):
    with open(path, "rb") as stream:
        return decode_record(stream)
```

This function owns opening and closing the file. Replacing it with scattered
caller-side opens or returning a lazy decoder after the handle closes can change
behavior and leak resources. Keep this lifetime boundary or move ownership
deliberately to one appropriate caller. A useful proof exercises success and a
decode failure, including required cleanup behavior.

Likewise, an async wrapper that establishes a timeout, joins children, or runs
cleanup in `finally` owns cancellation/lifetime policy. It is not equivalent to
forwarding a coroutine. Inspect actual runtime semantics before removing it.

## Keep similar code with different semantics

Two functions both round a number, but one implements a billing currency rule and
the other rounds display coordinates. Their precision, tie-breaking, errors,
units, and reasons to change differ. A generic `round_value(mode=...)` can make
ownership less clear. Keep explicit functions unless a real shared rule exists.

## Centralize a shared invariant

Two import entrypoints normalize the same record identifier and must reject the
same invalid values. Confirm equivalent requirements, find the canonical domain
owner, and give it one normalization operation. Migrate both callers, remove the
old copies, test normalization at its public boundary, and test meaningful
caller-specific handling separately.

If a third consumer outside the requested module requires a different contract,
classify that difference before extracting. Global search informs the decision;
it does not authorize changing every result.
