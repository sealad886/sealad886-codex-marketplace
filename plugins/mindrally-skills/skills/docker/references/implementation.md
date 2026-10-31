# Docker Development: implementation guidance

## Images and secrets

Multi-stage builds can keep compilers and unused files out of runtime images.
Pin reviewed versions/digests with an update policy; Alpine/musl or distroless may
break native dependencies or debugging assumptions. .dockerignore limits context,
but build args and ordinary ENV are not secret channels. Use BuildKit secret/SSH
mounts where needed and verify secrets never reach layers/artifacts. Run non-root
when supported, drop unneeded capabilities, and define ownership/read-only paths.
One concern per container is a useful heuristic, not an absolute process count.

## Compose and operations

Modern Compose follows the Compose Specification; the top-level version field is
obsolete rather than requiring version 3+. depends_on alone gives order, while
service_healthy waits for configured healthchecks; neither guarantees ongoing
application reconnection or recovery. Mount volumes deliberately and test backup/
restore before data cleanup. EXPOSE does not publish a port; review host bindings
and container DNS/network boundaries. Use exec-form entrypoints/signal handling
and bounded resource limits. Image scans, signatures, and healthchecks provide
specific evidence, not proof of safe deployment or external publication authority.

## Primary documentation

- [Obsolete Compose version field](https://docs.docker.com/compose/compose-file/04-version-and-name/).
- [Dependency health and startup order](https://docs.docker.com/compose/how-tos/startup-order/).
- [Build secret mounts](https://docs.docker.com/build/building/secrets/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
