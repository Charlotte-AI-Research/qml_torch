"""Pauli-Z measurement used by the v0.1 output contract."""

from __future__ import annotations

from ..backends import require_pennylane


def pauli_z_output(qubits: int):
    """Return one Pauli-Z expectation measurement for every qubit."""

    if qubits < 1:
        raise ValueError("qubits must be at least 1")
    qml = require_pennylane()
    return [qml.expval(qml.PauliZ(index)) for index in range(qubits)]
