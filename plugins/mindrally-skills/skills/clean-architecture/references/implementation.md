# Clean Architecture: implementation guidance

## Dependency rule and tradeoffs

Dependencies point toward stable policy in a Clean Architecture design; dependency
inversion can place interfaces near the consuming policy and implementations in
outer adapters. This is a design approach, not a requirement for four directories
in every application. Avoid duplicate DTO/domain mappings or one-method use cases
unless they serve a present boundary. Testability alone does not require an
interface for every concrete dependency.

## Flutter and Go choices

Flutter may use UI/data separation, with a domain/use-case layer when complexity
or reuse justifies it. BLoC, Riverpod, ChangeNotifier, Freezed, get_it, and Dartz are
choices, not Clean Architecture dependencies. Preserve the project's error model;
Either is not the only correct way to express expected failures. In Go, keep
interfaces small and consumer-owned, wire dependencies with constructors, and
use internal packages for intended encapsulation. Do not create pkg automatically
or treat a particular folder tree as a correctness rule. Verify domain logic
independently and integration behavior with the actual persistence/transport.

## Primary documentation

- [Conditional domain layer and state-management choices](https://docs.flutter.dev/app-architecture/recommendations).
- [Go module/package organization](https://go.dev/doc/modules/layout).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
