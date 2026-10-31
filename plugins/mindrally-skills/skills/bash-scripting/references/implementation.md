# Bash Scripting: implementation guidance

## Shell and error semantics

A Bash shebang permits Bash features; POSIX sh portability is a different target.
Use getopts within its supported short-option semantics or a reviewed parser.
Quote expansions and use arrays for argument lists; do not build commands with
eval. Separate data from code and use -- for operands when the command supports it.
set -e has exceptions in conditionals, lists, pipelines, and command substitutions;
pipefail changes pipeline status. Neither is a substitute for checking meaningful
failures. Under set -e the upstream validate_input function returns status 1 for
valid arguments because its final conditional is false; use an explicit successful
return. Do not present that sample as working automation.

## Cleanup and unattended work

Create private temporary files/directories with mktemp and trap only resources
owned by this invocation. Preserve the original failure status and handle unset
variables deliberately. Validate deletion targets; never delete a caller-supplied
path by default. Locking needs atomic ownership and a documented stale-lock policy.
Cron has a minimal environment: use explicit paths, timeouts, logging separation,
and credentials from approved stores. Syntax/lint cannot prove remote transfers,
backup restoration, or deployment recovery.

## Primary documentation

- [errexit, pipefail, quoting, traps, and arrays](https://www.gnu.org/software/bash/manual/bash.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
