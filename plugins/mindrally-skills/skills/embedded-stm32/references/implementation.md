# Embedded STM32 / HAL Development: implementation guidance

## DMA, UART, and concurrency

Use the target HAL's supported receive-to-idle DMA API/callback when available,
and understand half/transfer-complete/idle events and circular-buffer positions.
The upstream sample immediately rearms the same rx_buf while main reads it, so
its flag does not establish buffer ownership: DMA may overwrite data during parsing.
Use a proven ring buffer/double buffer or copy/transfer ownership before rearming,
and define overrun/backpressure behavior. Check every HAL result. Do not duplicate
Cube-generated IRQ handlers or skip unrelated UART error processing. Cache-equipped
cores need correct DMA-accessible memory, alignment, clean/invalidate operations,
and barriers as documented for that MCU.

## Interrupts, memory, and hardware evidence

volatile does not make a handoff atomic or synchronized. Use a safe critical section
that restores prior interrupt state, or suitable atomics/queues; blindly disabling
then enabling IRQs can violate nested state. Respect RTOS FromISR APIs and configured
priority ceilings. Bound blocking waits with a functioning time base, and keep them
out of ISRs. Inspect linker map/stack and watchdog refresh design; const alone does
not guarantee a specific memory placement. Host tests cannot prove electrical,
DMA/cache or timing correctness. Flashing, actuators and destructive operations
require explicit authorization and target identity checks.

## Primary documentation

- [HAL UART receive-to-idle, events and DMA lifecycle](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/master/Src/stm32f4xx_hal_uart.c).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
