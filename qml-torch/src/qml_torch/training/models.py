"""The two v0.1 models used in the comparison report."""

from __future__ import annotations

import torch
from torch import nn

from ..nn import QuantumLayer


class ClassicalModel(nn.Module):
    """A single linear logit baseline."""

    def __init__(self, n_features: int) -> None:
        super().__init__()
        if n_features < 1:
            raise ValueError("n_features must be at least 1")
        self.linear = nn.Linear(n_features, 1)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.linear(inputs)


class HybridVQCModel(nn.Module):
    """A quantum layer followed by a small classical output layer."""

    def __init__(self, n_qubits: int, shots: int | None = None, layers: int = 1) -> None:
        super().__init__()
        self.quantum = QuantumLayer(n_qubits, layers=layers, shots=shots)
        self.output = nn.Linear(n_qubits, 1)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.output(self.quantum(inputs))
