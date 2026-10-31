# C++ Development Guidelines: implementation guidance

## Ownership and language semantics

Prefer values/containers and RAII; use unique_ptr for exclusive ownership,
shared_ptr only for shared lifetime, weak_ptr for appropriate cycle breaking,
and references/raw pointers for non-owning access with valid lifetimes.
string_view/span do not extend the storage lifetime. vector operator[] is not
bounds checking: use at or prove/check an index before access. noexcept is a
contract; an escaping exception terminates the process. Match concepts/ranges,
coroutines, modules, and jthread to actual compiler/library support.

## Performance and concurrency

std::move does not guarantee movement, and applying it to local returns can
prevent copy elision. inline mainly affects linkage/ODR semantics; compilers choose
inlining. Perfect forwarding applies to forwarding references, not every argument.
Atomic operations are not necessarily lock-free, and lock-free does not imply
race-free correctness for a whole algorithm. std::async may defer execution under
its default policy; choose scheduling/lifetime deliberately. jthread supports
joining/cancellation patterns but does not stop unsafe work automatically. Test
resource/error paths and run compatible ASan/UBSan/TSan configurations separately.
Use the project's build/dependency tools rather than imposing CMake/Conan/vcpkg.

## Primary documentation

- [Ownership, bounds, lifetime and concurrency guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
