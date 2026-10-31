# GraalVM: implementation guidance

## Metadata and initialization

Native Image static analysis cannot infer every dynamic access. Use current
reachability metadata/framework hints and inspect tracing-agent output; an exercised
trace is not proof of complete coverage. Build-time class initialization may capture
secrets, host state, randomness or environment into the image heap; use it only after
review, not as a blanket startup optimization. Runtime initialization is needed for
appropriate dynamic resources. JVM JIT/polyglot capabilities are separate from what
a specific native image includes. Match JDK language features and framework versions.

## Frameworks and native acceptance

Modern Spring Boot native support uses Spring AOT/RuntimeHints; experimental Spring
Native/@NativeHint is obsolete for current Boot. Quarkus/Micronaut have their own
versioned extensions/metadata. JVM tests do not prove native behavior: exercise
reflection, files, certificates, locale/time zones, databases, proxies and serialization
in the binary. Native GC/heap flags depend on distribution and build; do not blindly
copy JVM flags or assume fallback images remain available. Native binaries are
platform/ABI specific and need actual packaging/signing/runtime validation. Compare
performance under representative load; native startup improvements can trade build
time or throughput. Publication and deployment require explicit authority.

## Primary documentation

- [Reachability metadata and dynamic features](https://www.graalvm.org/latest/reference-manual/native-image/metadata/).
- [Spring AOT RuntimeHints](https://docs.spring.io/spring-framework/reference/core/aot.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
