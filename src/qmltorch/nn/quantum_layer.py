"""PyTorch modules for the supported hybrid layer."""

from __future__ import annotations

from typing import Any

from ..circuits import angle_embedding_qnode


def quantum_layer(n_qubits: int, n_layers: int = 1, **kwargs: Any) -> Any:
    """Return PennyLane's TorchLayer for the standard circuit."""

    try:
        import pennylane as qml
    except ImportError as exc:
        raise ImportError("Install PennyLane and PyTorch to use QuantumLayer") from exc

    circuit = angle_embedding_qnode(n_qubits, n_layers, interface="torch")
    return qml.qnn.TorchLayer(circuit, {"weights": (n_layers, n_qubits)}, **kwargs)


QuantumLayer = quantum_layer
TorchQuantumLayer = quantum_layer

__all__ = ["QuantumLayer", "TorchQuantumLayer", "quantum_layer"]
