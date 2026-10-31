# FPGA Development: implementation guidance

## Clocks, resets, and constraints

Prefer appropriate clock enables and dedicated clock-control primitives; do not
implement fabric combinational clock gating to save power. Reset style depends on
architecture and requirements, with safe deassertion per clock domain when needed.
A double-flop synchronizer suits eligible single-bit controls, not coherent multi-bit
buses or arbitrary pulses; use reviewed handshakes/async FIFOs and constraints.
False/multicycle paths must express real design behavior, not hide timing failures.
Check all clocks, generated clocks, I/O delays, exceptions and unconstrained paths.

## Datapaths and verification

Use always_ff/always_comb and assignments appropriate to the language/tool, prevent
unintended latches, and inspect inferred RAM/DSP rather than prescribing reg arrays
as sufficient for BRAM. Pipeline only with a verified latency/handshake contract.
AXI channels require stable payload under backpressure and correct burst/reset
handling; larger DMA bursts are not always optimal. Use assertions, randomized
backpressure and CDC analysis in addition to functional simulation. Post-synthesis
simulation and an ILA do not replace routed static timing/electrical validation.
Board programming and attached device actions require explicit target authority.

## Primary documentation

- [CDC timing constraints and exception priority](https://docs.amd.com/r/en-US/ug903-vivado-using-constraints/Constraining-Asynchronous-Signals).
- [FPGA methodology, clocks and implementation checks](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
