# Compile And Transforms

Use this reference for `mx.compile`, `mx.grad`, `mx.value_and_grad`, `mx.vmap`,
and `mx.checkpoint`.

## Compile Fit

Good candidates:

- Pure numerical functions with stable argument structure.
- Repeated hot functions where compile overhead is amortized.
- Training steps that avoid host-side side effects.

Compile triage should inspect `mx.compile` options such as `shapeless`,
`inputs`, and `outputs` before assuming defaults are enough.

Risky candidates:

- Functions that print, mutate global state, perform file I/O, or branch heavily
  on Python values.
- Functions whose shapes change constantly.
- Functions where one-off compile cost exceeds saved runtime.

## Training Transform Pattern

```python
import mlx.core as mx
import mlx.nn as nn

def loss_fn(model, batch):
    logits = model(batch["x"])
    return cross_entropy(logits, batch["y"])

loss_and_grad = nn.value_and_grad(model, loss_fn)
loss, grads = loss_and_grad(model, batch)
optimizer.update(model, grads)
mx.eval(model.parameters(), optimizer.state)
```

For `mlx.nn.Module` training, prefer `nn.value_and_grad(model, loss_fn)` so
gradients target the model's trainable parameters. Use
`mlx.core.value_and_grad(fun)` for parameter-tree or other pure core functions
where differentiable values are passed explicitly.

## Checkpointing

Use rematerialization when activation memory is the bottleneck and recomputation
is cheaper than storing intermediates. Verify with peak-memory and wall-time
measurements because checkpointing trades memory for compute.
