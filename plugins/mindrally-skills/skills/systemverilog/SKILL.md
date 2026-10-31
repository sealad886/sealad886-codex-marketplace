---
name: systemverilog
description: "Use when implementing SystemVerilog modules, sequential/combinational logic, CDC, memory inference, assertions, or timing closure."
---

# SystemVerilog RTL and verification

## When to invoke

Use when implementing SystemVerilog modules, sequential/combinational logic, CDC, memory inference, assertions, or timing closure.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect target FPGA/ASIC technology, synthesis/simulator versions, clocks/resets, timing constraints, interfaces, and resource/latency goals.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define clock/reset domains and cycle-accurate interface behavior.
2. Implement synthesizable RTL with appropriate assignments, inference templates, and CDC structures.
3. Run lint/simulation/assertions and inspect synthesis, timing, CDC, and resource evidence.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run supported simulation/lint and relevant synthesis/timing/CDC checks; identify untested silicon/board behavior and unproven constraints.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
