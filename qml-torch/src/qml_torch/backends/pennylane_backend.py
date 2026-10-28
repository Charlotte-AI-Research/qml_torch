"""Small PennyLane adapter used by the v0.1 simulator layer."""

from __future__ import annotations

from typing import Any


def require_pennylane() -> Any:
    """Import PennyLane with an actionable installation message."""

    try:
        import pennylane as qml
    except ImportError as exc:  # pragma: no cover - depends on the user's environment
        raise ImportError(
            "PennyLane is required for the quantum layer. Install with "
            "pip install 'qml-torch[dev]' or pip install pennylane."
        ) from exc
    return qml


def build_device(n_qubits: int, shots: int | None = None) -> Any:
    """Build the hidden local simulator used by the first release."""

    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1")
    qml = require_pennylane()
    # Shots belong to the QNode in current PennyLane releases. Keeping this
    # device analytic also avoids the device-level deprecation warning while
    # retaining compatibility with older PennyLane versions.
    return qml.device("default.qubit", wires=n_qubits)
