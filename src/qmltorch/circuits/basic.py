"""PennyLane circuit factories used by the learning examples."""

from __future__ import annotations

from typing import Any


def angle_embedding_qnode(n_qubits: int, n_layers: int = 1, **qnode_kwargs: Any) -> Any:
    """Create a trainable angle-embedding QNode.

    The returned QNode accepts ``inputs`` and ``weights`` and returns one Z
    expectation per qubit. PennyLane is imported lazily so ``qmltorch`` can
    still be imported when only documentation tooling is installed.
    """

    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1")
    if n_layers < 1:
        raise ValueError("n_layers must be at least 1")
    try:
        import pennylane as qml
    except ImportError as exc:
        raise ImportError("Install the 'qmltorch' dependencies to create a QNode") from exc

    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev, **qnode_kwargs)
    def circuit(inputs: Any, weights: Any) -> Any:
        qml.AngleEmbedding(inputs, wires=range(n_qubits), rotation="Y")
        for layer in range(n_layers):
            for wire in range(n_qubits):
                qml.RY(weights[layer, wire], wires=wire)
            for wire in range(n_qubits - 1):
                qml.CNOT(wires=[wire, wire + 1])
        return [qml.expval(qml.PauliZ(wire)) for wire in range(n_qubits)]

    return circuit


make_qnode = angle_embedding_qnode
