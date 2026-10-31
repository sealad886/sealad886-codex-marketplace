---
name: php-development
description: "Use when implementing PHP application modules, types, Composer autoloading, data access, validation, or error handling."
---

# PHP Development

## When to invoke

Use for implementing PHP application modules, types, Composer autoloading, data access, validation, or error handling.

## Inputs and evidence

Inspect composer/runtime version constraints, extensions, coding standards, autoload rules, framework boundaries and trust inputs. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose language features supported by configured PHP versions.
2. Implement cohesive interfaces with appropriate type declarations and runtime validation.
3. Use parameterized persistence, context-appropriate output encoding and scoped exception handling.
4. Run syntax/static analysis and behavior/security boundary tests in the project environment.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Declared PHP targets pass syntax/static and meaningful behavior/error/authorization tests.

## Must not

Do not equate strict_types or input sanitization with complete security validation. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
