"""Angle encoding for the first supported feature-to-qubit mapping."""

from __future__ import annotations

from typing import Any

from ..backends import require_pennylane


def angle_encoding(inputs: Any, qubits: int, selected_gate: str = "Y") -> None:
    """Apply one angle rotation per feature/qubit.

    The layer validates the feature count before entering the QNode. PennyLane
    handles a leading batch dimension when this operation is called by a
    ``TorchLayer``.
    """

    if qubits < 1:
        raise ValueError("qubits must be at least 1")
    rotation = selected_gate.upper()
    if rotation not in {"X", "Y", "Z"}:
        raise ValueError("selected_gate must be 'X', 'Y', or 'Z'")
    qml = require_pennylane()
    qml.AngleEmbedding(inputs, wires=range(qubits), rotation=rotation)
