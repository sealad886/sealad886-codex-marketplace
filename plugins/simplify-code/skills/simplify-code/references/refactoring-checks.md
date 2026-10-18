# Refactoring checks

Use relevant checks, not every item mechanically. Establish the accepted contract
and language/framework semantics before deciding that a layer is redundant.

## Callers and consumers

| Surface | Evidence to inspect | Why text search alone can miss it |
| --- | --- | --- |
| Direct calls and imports | References, imports/re-exports, symbol graph, tests | Aliases or generated callsites may hide the name |
| Package/public exports | Export maps, public headers, package docs, API examples | Consumers may live outside the repository |
| CLI and service dispatch | Manifest entrypoints, command tables, route registration | Invocation may use a string or configured path |
| Framework callbacks | Required protocol/interface methods, decorators, lifecycle hooks | Framework invokes code implicitly |
| Plugins and registries | Registration/config, discovery conventions, entrypoint metadata | Dynamic lookup often has no direct call |
| Reflection and serialization | String lookup, schema mappings, hooks, persisted type names | Runtime values can refer to symbols |
| Generated bindings | Generator inputs, templates, build rules, generated API | Editing output alone is temporary or misleading |
| External integration | Public contract, provider configuration, owned consumers | Local tests cannot inventory all external use |

If a path is only needed by an obsolete feature, verify the feature is within
removal scope and inspect all associated callers/config/dependencies. Do not keep
the path solely because it once had users. Conversely, absence of local consumers
does not establish absence of a required public contract.

## Semantics before inlining

- Error type, context, stack behavior, retries, and exception/cancellation propagation.
- Eager versus lazy evaluation, sync versus async timing, and event-loop/task ownership.
- Cleanup on success, failure, interruption, generator close, and partial consumption.
- Transaction, lock, handle, and resource lifetimes, including borrowed versus owned data.
- Side-effect ordering, mutability/aliasing, identity, ordering guarantees, and concurrency.
- Framework dispatch, override behavior, dependency direction, and explicit domain policy.

An async wrapper can change when work runs or where cleanup happens. A catch block
can add context or restore state. A class can own lifetime despite having one
method. Remove only the layer whose responsibility has been shown unnecessary.

## Consolidation boundary

Compare behavior across copies: inputs, outputs, errors, units, defaults, resource
ownership, and caller policy. Prefer an existing owner. Otherwise create one
small helper in the closest shared module with explicit inputs/outputs.

Keep distinct policies explicit. If a proposed helper requires a boolean for
each former branch, configurable hooks, or a new dependency cycle, the extraction
probably merged different reasons to change. Similar code can remain separate.

## Residue and proof

Recheck imports, exports, manifests/lockfiles, flags, routes, registration, assets,
comments, docs, and tests after deletion. Remove only dependencies demonstrated
unused across their owning package, using the repository's normal lockfile flow.

Protect required behavior at a stable public boundary, plus meaningful caller
differences. Avoid snapshots of the architecture being removed. A targeted
characterization test is useful when it establishes a required error, ordering,
cleanup, or output contract; a test of a private delegation sequence is not.

Review both the diff and representative path. Report static, runtime, integration,
and external-consumer checks separately, including what could not be established.
