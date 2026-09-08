"""Public API for the QML Torch student project."""

from .core import hello

try:
    from .nn import QuantumLayer, TorchQuantumLayer
except ImportError:  # Keep metadata and docs importable without optional ML dependencies.
    QuantumLayer = None  # type: ignore[assignment,misc]
    TorchQuantumLayer = None  # type: ignore[assignment,misc]


__all__ = ["QuantumLayer", "TorchQuantumLayer", "hello"]
