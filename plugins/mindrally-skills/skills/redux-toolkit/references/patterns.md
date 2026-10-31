# Redux Toolkit state ownership: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use `configureStore` defaults unless a requirement justifies changes; avoid disabling serializable/immutability checks merely to suppress a defect.

- `createSlice` reducers can use Immer draft mutation; do not mutate the original state outside reducer execution.

- Derive RootState and AppDispatch from the store, and use the installed React Redux typed-hook support rather than hand-maintained duplicate types.

- RTK Query supports endpoint caching and tag invalidation; do not duplicate its response data in ordinary slices without a specific ownership need.

- Use createAsyncThunk for workflows that fit it; narrow unknown thrown values before reading fields such as message and model rejected payload types.

- Keep selectors pure and memoize expensive derived output or unstable object results where it matters.

- For SSR, use request-scoped stores and explicit hydration; avoid cross-request user state leakage.

- Test reducers and selectors where useful, but use integration tests with a real store for connected behavior. Inline callbacks are not intrinsically incorrect or slow.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [configureStore, slices, async logic, and cache utilities have distinct responsibilities.](https://redux-toolkit.js.org/usage/usage-guide)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
