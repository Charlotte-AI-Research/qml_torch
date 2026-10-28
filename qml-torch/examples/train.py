"""Small two-feature dataset for the ``qml-torch run`` tutorial."""

from __future__ import annotations

import torch


def get_data() -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Return ``x_train, y_train, x_test, y_test`` for binary classification."""

    generator = torch.Generator().manual_seed(7)
    x_train = torch.tensor(
        [[-1.0, -0.8], [-0.8, -1.1], [-1.2, -0.9], [0.9, 1.0], [1.1, 0.8], [0.8, 1.2]],
        dtype=torch.float32,
    )
    y_train = torch.tensor([0, 0, 0, 1, 1, 1], dtype=torch.float32)
    noise = torch.randn((4, 2), generator=generator) * 0.08
    x_test = torch.tensor(
        [[-1.0, -1.0], [-0.9, -0.7], [1.0, 0.9], [0.7, 1.1]], dtype=torch.float32
    ) + noise
    y_test = torch.tensor([0, 0, 1, 1], dtype=torch.float32)
    return x_train, y_train, x_test, y_test
