# SystemVerilog RTL and verification: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use always_comb with complete assignments for intended combinational logic and always_ff/nonblocking assignments for appropriate sequential logic.

- Choose reset strategy from target resources, startup, and CDC requirements; synchronous reset is not universally correct for every technology.

- FPGA fabric clock gating can introduce skew/glitches. Prefer target-supported clock enables or dedicated clock-buffer primitives; ASIC gating uses characterized cells and methodology.

- A declaration such as reg[] does not guarantee RAM inference; port count, read latency, reset pattern, and synthesis templates determine mapping.

- Synchronizers suit appropriate single-bit control signals; multi-bit coherent data needs handshakes, Gray-code schemes, or asynchronous FIFOs as appropriate.

- Use vendor/flow-specific timing constraints; XDC is not universal for ASIC or every FPGA tool. Do not hide real violations with false paths.

- Pipeline changes alter latency and protocol behavior; preserve throughput/backpressure and reset/flush semantics.

- ILA is vendor-specific hardware debug, while simulation and formal assertions establish different evidence; neither replaces timing closure.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [AMD FPGA clocking guidance discourages gated fabric clocks and recommends dedicated resources/enables.](https://docs.amd.com/r/en-US/conversion-methodology/Clocking-RTL-Best-Practices)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
