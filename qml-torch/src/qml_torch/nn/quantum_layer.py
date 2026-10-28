"""PyTorch module wrapping the hidden PennyLane circuit preset."""

from __future__ import annotations

import torch
from torch import nn

from ..circuits import basic_circuit
from ..config.models import positive_integer


class BasicQuantumLayer(nn.Module):
    """A beginner-friendly quantum layer with one output per qubit."""

    def __init__(
        self,
        qubits: int,
        encoding_gate: str = "Y",
        layers: int = 1,
        shots: int | None = None,
        seed: int | None = None,
    ) -> None:
        super().__init__()

        if type(qubits) is int and qubits < 1:
            raise ValueError("qubits must be at least 1")
        if type(layers) is int and layers < 1:
            raise ValueError("layers must be at least 1")
        positive_integer(qubits, "qubits")
        positive_integer(layers, "layers")
        if shots is not None:
            positive_integer(shots, "shots")

        encoding_gate = encoding_gate.upper()
        if encoding_gate not in {"X", "Y", "Z"}:
            raise ValueError("encoding_gate must be 'X', 'Y', or 'Z'")

        self.qubits = qubits
        self.layers = layers
        self.shots = shots
        self.encoding_gate = encoding_gate
        self.quantum_layer = basic_circuit(
            qubits=qubits,
            encoding_gate=encoding_gate,
            layers=layers,
            shots=shots,
            seed=seed,
        )

    @property
    def circuit(self):
        """Return the underlying QNode for report/diagram generation."""

        return self.quantum_layer.qnode

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """Run the circuit for one sample or a batch of samples."""

        if not isinstance(inputs, torch.Tensor):
            raise TypeError("QuantumLayer input must be a torch.Tensor")
        if inputs.ndim not in (1, 2) or inputs.shape[-1] != self.qubits:
            raise ValueError(
                f"Expected [{self.qubits}] or [batch, {self.qubits}], got {tuple(inputs.shape)}"
            )
        if not inputs.is_floating_point():
            if inputs.is_complex():
                raise TypeError("QuantumLayer expects real-valued features")
            inputs = inputs.to(dtype=torch.get_default_dtype())
        if inputs.device.type != "cpu":
            raise ValueError("The v0.1 simulator uses CPU tensors; move the input to .cpu()")
        if inputs.numel() == 0:
            raise ValueError("QuantumLayer input cannot be empty")
        if not torch.isfinite(inputs).all():
            raise ValueError("QuantumLayer input must contain only finite values")
        # Parameter-shift cannot differentiate broadcasted input angles on every
        # supported PennyLane version. Individual samples also support gradients
        # flowing through an upstream classical layer in finite-shot mode.
        if self.shots is not None and inputs.ndim == 2:
            return torch.stack([self.quantum_layer(sample) for sample in inputs])
        return self.quantum_layer(inputs)


QuantumLayer = BasicQuantumLayer

__all__ = ["BasicQuantumLayer", "QuantumLayer"]
