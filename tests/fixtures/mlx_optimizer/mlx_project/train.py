import time

import mlx.core as mx


def train_epoch(batches):
    losses = []
    for batch in batches:
        loss = mx.sum(batch)
        print(loss.item())
        mx.eval(loss)
        losses.append(loss)
    return losses


def benchmark(batch):
    start = time.perf_counter()
    value = mx.sum(batch)
    end = time.perf_counter()
    return end - start, value
