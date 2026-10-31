---
name: viewcomfy-api-rules
description: "Use when integrating an existing ViewComfy workflow endpoint, parameter schema, streamed logs, or generated outputs."
---

# ViewComfy workflow API integration

## When to invoke

Use when integrating an existing ViewComfy workflow endpoint, parameter schema, streamed logs, or generated outputs.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect the deployed workflow/API schema, official sample version, endpoint identity, credentials destination, output contract, and cost/time limits.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Confirm the existing deployment’s parameter and response schema before making requests.
2. Implement server-side credentials, bounded HTTP/SSE handling, and explicit generation state.
3. Validate output identities and safe file handling with synthetic responses before authorized live inference.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test fixture responses for malformed/SSE/error/timeout/path-traversal cases; run a small live generation only with endpoint, credentials, and cost authority.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
