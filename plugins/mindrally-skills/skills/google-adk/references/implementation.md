# Google Agent Development Kit (ADK): implementation guidance

## Agent, tools, and output contracts

ADK API generations and model capabilities evolve; use the installed SDK and
matching docs rather than fixed Gemini 2.0 names. Sequential/parallel/loop agents
control orchestration order, not deterministic model output or safe side effects.
Tools require runtime input validation, resource authorization and idempotency
outside prompts. AgentTool and sub-agent delegation have different state/control
semantics. Built-in tool combination and structured-output restrictions depend
on provider/model/API generation. output_key saves an output to state; it does
not enforce output_schema. Bound loops and handle all event/error/cancellation states.

## State, artifacts, and operations

Update state through ToolContext/CallbackContext or appended event state_delta;
mutating a retrieved Session.state dictionary directly can bypass persistence.
Understand app/user/temp prefixes and prevent cross-user sharing. In-memory services
lose data on restart; production database/managed service choice needs schema and
concurrency validation. Memory is not automatically populated or permission-safe.
Artifacts require configured services, validated names/types/size and access scopes.
Evaluate response quality and necessary tool invariants rather than pinning every
internal call order. Redact events/traces and restrict local developer UI exposure.
Deployment, cloud resources, external calls and payments require task authority.

## Primary documentation

- [Managed context/event state updates](https://adk.dev/sessions/state/).
- [Version-matched agent/workflow capabilities](https://google.github.io/adk-docs/agents/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
