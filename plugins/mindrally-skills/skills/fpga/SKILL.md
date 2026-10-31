---
name: fpga
description: "Use when implementing FPGA RTL, clock/reset domains, timing constraints, AXI/DMA interfaces, or resource/power optimization."
---

# FPGA Development

## When to invoke

Use when implementing FPGA RTL, clock/reset domains, timing constraints, AXI/DMA interfaces, or resource/power optimization. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect target FPGA/tool version, clock/reset topology, XDC, interface timing/protocol, resource budgets, and board constraints. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define cycle/latency/throughput and CDC/reset invariants before RTL or constraints changes.
2. Implement synthesizable logic and valid handshakes using vendor-supported clocks, memory inference and synchronization.
3. Run self-checking simulation/assertions plus synthesis/implementation STA, CDC and resource reports; verify authorized hardware separately.

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
