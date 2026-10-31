# Modern Fortran Development: implementation guidance

## Kinds and interfaces

Use iso_fortran_env or selected_*_kind for the required representation/precision,
checking availability; a named real64 kind is negative when unsupported. For C
interoperability use iso_c_binding kinds and bind(C), not a presumed int32 ABI.
implicit none and explicit module interfaces catch many errors but do not establish
all runtime preconditions. intent documents data use and can affect definability;
not every specialized dummy argument permits the same intent pattern. Fortran is
case-insensitive, so differing only by case names the same identifier.

## Numeric and memory behavior

The upstream mean divides by zero on an empty array, and sample standard deviation
for n<2 is undefined rather than universally zero. Define and test invalid-data
policy, finite values and numerical stability. Do not terminate a reusable library
with stop/error stop for routine input failure unless its public contract requires
it. Prefer allocatables when ownership fits, but automatic deallocation depends
on scope/SAVE/lifetime; do not assume every local allocation is released. Use
stat/iostat/iomsg where meaningful, check array conformability, and avoid unbounded
intermediates/hot-loop allocation. Compiler-specific flags and floating-point
optimization choices need explicit accuracy/reproducibility evidence.

## Primary documentation

- [Kind availability and storage sizes](https://gcc.gnu.org/onlinedocs/gfortran/ISO_005fFORTRAN_005fENV.html).
- [C interoperability kinds](https://gcc.gnu.org/onlinedocs/gfortran/ISO_005fC_005fBINDING.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
