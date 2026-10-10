'''
This file contains the code for the quantum layer function that can be implemented into a classical torch nn.
'''
from ..circuits import basic_circuit
import torch
import torch.nn as nn
class BasicQuantumLayer(nn.Module):

    def __init__(
        self,
        qubits: int,
        encoding_gate: str = "Y",
        layers: int = 1,
    ):
        super().__init__()

        if qubits < 1:
            raise ValueError("qubits must be at least 1")
        if layers < 1:
            raise ValueError("layers must be at least 1")

        encoding_gate = encoding_gate.upper()
        if encoding_gate not in {"X", "Y", "Z"}:
            raise ValueError("encoding_gate must be 'X', 'Y', or 'Z'")

        self.qubits = qubits

        self.quantum_layer = basic_circuit(
            qubits=qubits,
            encoding_gate=encoding_gate,
            layers=layers,
        )

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        if X.ndim not in (1, 2) or X.shape[-1] != self.qubits:
            raise ValueError(
                f"Expected [{self.qubits}] or [batch, {self.qubits}], "
                f"got {tuple(X.shape)}"
            )

        return self.quantum_layer(X)