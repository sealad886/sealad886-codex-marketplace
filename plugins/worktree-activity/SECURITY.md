# Security boundary

This is a cooperative local registry for processes running as the same OS user,
not authentication against hostile local code. Native environment values and
the coordinator assertion can be forged by such code. The helper coordinates
registry writes only, not source-file editing. Root identities are recovery
destinations; diagnostic assignee IDs never are.

Use local macOS/Linux filesystems with reliable advisory flock and atomic rename.
Do not use network filesystems, untrusted writable directory ancestors, or
unsupported platforms. Symlinks are rejected; this is not a hostile namespace
sandbox. Ordinary operations make no network requests. Install dependencies
separately in a dedicated virtual environment.

Records contain task descriptions and concise evidence only. Do not put secrets,
transcripts, access-bearing URLs, or personal data into them. Read-only recovery
plans may expose local paths and conversation IDs; share intentionally.

Malformed, unsupported, conflicting, or unsafe records must remain for owner
review. No age, shutdown, interrupted run, or background sweep authorizes deletion.
Report a security issue privately to the repository owner before public disclosure.
