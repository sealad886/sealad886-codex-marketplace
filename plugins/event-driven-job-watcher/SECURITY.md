# Security

The watcher runs the already authorized argument vector with the caller's
working directory, environment, and permissions. Use an existing private job
directory. Keep commands and callback paths free of credentials, and treat job
logs as sensitive. The helper creates receipts and logs exclusively, with
owner-only permissions, and does not read job log contents.

The optional Codex callback sends the receipt path to the authorized chat UUID
once. The helper records the submission outcome without retaining raw Codex
output. A callback failure leaves the job's own result available.

Report suspected vulnerabilities through the repository's
[private security reporting](https://github.com/sealad886/sealad886-codex-marketplace/security/advisories/new).
Use synthetic job output and avoid sending receipts or logs that contain
private paths or credentials.
