# PyTorch Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Model and evaluation state

- Register parameters and buffers deliberately and call the module to preserve hooks; forward defines the computation.
- model.eval changes module behavior and no_grad/inference_mode changes gradient recording; neither substitutes for the other.
- Keep loss normalization/zeroing/optimizer-step order correct under accumulation and checkpoint resume.

## Devices and scaling

- Current torch.amp/autocast APIs replace deprecated torch.cuda.amp recipes; device types and supported dtypes differ by backend.
- Prefer supported DistributedDataParallel/FSDP strategies when justified rather than recommending DataParallel as a universal multi-GPU default.
- CUDA-only optimizations must not be applied to CPU/MPS unconditionally; synchronize the backend when benchmarking async work.
- DataLoader workers/pinning, quantization/compile and model-specific Transformers/Diffusers integrations need actual platform testing.
- Evaluate data leakage, task metrics, relevant fairness/safety slices and human acceptance; demo UI success is not model qualification.

## Primary documentation

- [Primary documentation](https://docs.pytorch.org/docs/2.15/amp.html) — Current PyTorch AMP uses device-aware torch.amp/autocast and deprecates older CUDA-specific entrypoints.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
