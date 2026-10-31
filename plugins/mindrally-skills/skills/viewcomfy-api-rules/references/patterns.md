# ViewComfy workflow API integration: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use the actual deployed endpoint and current official client/example; infer and infer_with_logs are helper functions in examples, not guaranteed distinct URL paths.

- Do not invent missing workflow parameters or silently change a seed merely to satisfy a claimed nonempty-params rule; validate the deployment’s actual schema.

- Keep client ID/secret server-side and redact logs; do not follow redirects that could forward credentials to an untrusted host.

- Handle cold starts with explicit connect/read/overall timeouts and cancellation; retries can duplicate costly generation unless the API supplies idempotency.

- Parse SSE event boundaries, multiline data, error events, and final result according to the provider’s stream contract.

- Treat returned filenames/content types/base64/size metadata as untrusted. Validate decoding and size, choose local names under an approved directory, and prevent traversal or overwrite.

- Check completed/status and optional outputs rather than assuming an HTTP response means generation succeeded.

- Creating deployments, calling billable generation, saving outputs over existing files, and publishing generated content require the corresponding task scope.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Official examples distinguish infer/infer_with_logs helpers and describe prompt result fields.](https://www.viewcomfy.com/blog/integrate-comfyui-workflows-into-your-apps-via-api)
- [Current provider material shows endpoint credentials and parameterized workflow requests.](https://www.viewcomfy.com/deploy-comfyui)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
