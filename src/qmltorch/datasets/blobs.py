"""Tiny deterministic datasets for tutorials and smoke tests."""

from __future__ import annotations

from typing import Any


def make_binary_blobs(n_samples: int = 64, seed: int = 7) -> tuple[Any, Any]:
    """Return two balanced, two-feature Gaussian classes as NumPy arrays."""

    if n_samples < 2:
        raise ValueError("n_samples must be at least 2")
    try:
        import numpy as np
    except ImportError as exc:
        raise ImportError("NumPy is required to create the example dataset") from exc
    rng = np.random.default_rng(seed)
    per_class = n_samples // 2
    centers = np.array([[-1.0, -1.0], [1.0, 1.0]])
    x = np.vstack([rng.normal(center, 0.35, (per_class, 2)) for center in centers])
    y = np.concatenate([np.zeros(per_class, dtype=np.int64), np.ones(per_class, dtype=np.int64)])
    return x, y
