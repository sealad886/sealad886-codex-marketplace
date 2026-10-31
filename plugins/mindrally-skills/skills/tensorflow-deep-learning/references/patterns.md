# TensorFlow and Keras model workflows: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Choose APIs from the installed Keras generation; Keras 3 model.save and model.export produce different artifact contracts.

- Fit preprocessing only on training data and split by relevant subject/group/time to avoid leakage.

- Use tf.data parallelism, shuffle buffers, cache, batching, and prefetch according to determinism/memory requirements; AUTOTUNE is a tuning option rather than a universal mandate.

- A tiny overfit experiment can expose pipeline defects, but regularization/noise and task structure may prevent near-zero loss without a bug.

- Align best-checkpoint and early-stopping selection metrics or explicitly choose which artifact is evaluated; the source mixed val_accuracy saving with val_loss restoration.

- Mixed precision and determinism depend on device/operators; validate outputs, gradient scaling, dtype, and resource consumption rather than promising speed.

- Keep training and serving input schemas/preprocessing identical and reload the exact export before promoting it.

- Long training, artifact upload, model deployment, and paid compute require task authority; do not infer acceptance from a notebook run.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Keras 3 uses model.export for SavedModel export and changed persistence/loading behavior.](https://keras.io/guides/migrating_to_keras_3/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
