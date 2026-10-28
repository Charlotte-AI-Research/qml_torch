"""The hidden, versioned circuit preset used by ``QuantumLayer``."""

from __future__ import annotations

from ..backends import build_device, require_pennylane
from ..encodings import angle_encoding
from ..measurements import pauli_z_output


def basic_qnode(
    qubits: int,
    encoding_gate: str = "Y",
    layers: int = 1,
    shots: int | None = None,
):
    """Build the internal QNode without exposing device configuration to users."""

    if qubits < 1:
        raise ValueError("qubits must be at least 1")
    if layers < 1:
        raise ValueError("layers must be at least 1")
    qml = require_pennylane()
    dev = build_device(qubits, shots=shots)
    diff_method = "backprop" if shots is None else "parameter-shift"

    def circuit(inputs, weights):
        angle_encoding(inputs, qubits, encoding_gate)

        for layer in range(layers):
            for i in range(qubits):
                qml.RY(weights[layer, i, 0], wires=i)
                qml.RZ(weights[layer, i, 1], wires=i)
                qml.RY(weights[layer, i, 2], wires=i)
            if qubits > 1:
                for i in range(qubits):
                    qml.CNOT(wires=[i, (i + 1) % qubits])

        return pauli_z_output(qubits)

    qnode_options = {"interface": "torch", "diff_method": diff_method}
    if shots is not None:
        qnode_options["shots"] = shots
    return qml.qnode(dev, **qnode_options)(circuit)


def basic_circuit(
    qubits: int,
    encoding_gate: str = "Y",
    layers: int = 1,
    shots: int | None = None,
):
    """Return PennyLane's TorchLayer for the standard v0.1 circuit."""

    qml = require_pennylane()
    qnode = basic_qnode(qubits, encoding_gate, layers, shots)
    weight_shapes = {"weights": (layers, qubits, 3)}
    return qml.qnn.TorchLayer(qnode, weight_shapes)
