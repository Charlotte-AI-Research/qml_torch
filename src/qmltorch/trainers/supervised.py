"""Small training helpers kept separate from model definitions."""

from __future__ import annotations

from typing import Any


def train_classifier(
    model: Any, features: Any, labels: Any, epochs: int = 20, lr: float = 0.05
) -> list[float]:
    """Train a binary Torch model and return the loss at each epoch."""

    import torch

    if epochs < 1:
        raise ValueError("epochs must be at least 1")
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.BCEWithLogitsLoss()
    losses: list[float] = []
    for _ in range(epochs):
        optimizer.zero_grad()
        predictions = model(features).squeeze(-1)
        loss = criterion(predictions, labels.float())
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    return losses
