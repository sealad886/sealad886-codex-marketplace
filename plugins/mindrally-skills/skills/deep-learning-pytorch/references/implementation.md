# Deep Learning and PyTorch Development: implementation guidance

## Training and device correctness

Use model.train for training and eval plus inference_mode/no_grad where appropriate
for inference. eval changes layer behavior but does not disable gradients. Choose
losses, normalization, augmentation, masks and sequence/box formats for the task.
Use supported torch.amp APIs instead of deprecated torch.cuda.amp entry points in
current releases. Autocast/GradScaler availability and dtype depend on CUDA/CPU/MPS
and installed versions; do not promise CUDA or mixed-precision speedups on every
machine. Scale accumulated losses correctly and unscale before clipping when using
a scaler. Accumulation does not always reproduce large-batch normalization behavior.

## Models, distributed work, and delivery

Prefer documented DistributedDataParallel over DataParallel for suitable multi-GPU
training; configure process groups, samplers, synchronization, and rank-specific
checkpointing. Seed generators/workers and report deterministic limitations.
Activation checkpointing trades compute for memory and needs version-correct API
and RNG handling. Save model, optimizer, scheduler/scaler, progress and RNG state
for meaningful resume. For Transformers/LoRA or Diffusers, verify tokenizer,
adapter targets, scheduler, weights, and model-specific preprocessing rather than
assuming every pipeline is interchangeable. Gradio demos need bounded inputs,
queues, authentication/network policy, and no unintended public sharing. Install
only task-required dependencies; never upload private datasets/metrics by default.

## Primary documentation

- [Current torch.amp and backend-specific precision](https://docs.pytorch.org/docs/stable/amp.html).
- [DistributedDataParallel semantics](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html).
- [Reproducibility limitations](https://docs.pytorch.org/docs/stable/notes/randomness.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
