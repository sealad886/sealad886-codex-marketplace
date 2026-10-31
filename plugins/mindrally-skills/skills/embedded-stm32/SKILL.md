---
name: embedded-stm32
description: "Use when implementing STM32 HAL peripherals, DMA, interrupts, RTOS coordination, memory, or firmware diagnostics."
---

# Embedded STM32 / HAL Development

## When to invoke

Use when implementing STM32 HAL peripherals, DMA, interrupts, RTOS coordination, memory, or firmware diagnostics. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect exact MCU/board/HAL version, schematic/clock tree, CubeMX .ioc, IRQ priorities, DMA memory/cache ownership, and hardware access authority. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace peripheral ownership and generated/user-code boundaries; define timing and data-transfer invariants.
2. Implement bounded HAL operations and minimal ISRs with safe DMA/CPU handoff, error handling, and cache synchronization.
3. Build/link and test pure logic on host, then verify timing, overrun/recovery, reset/low-power and watchdog behavior on authorized hardware.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
