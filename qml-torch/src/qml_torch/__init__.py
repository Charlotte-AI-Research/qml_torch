"""Public API for the QML Torch beginner package."""

from .config import ExperimentConfig

__version__ = "0.1.0a2"

__all__ = ["BasicQuantumLayer", "ExperimentConfig", "QuantumLayer", "__version__"]


def __getattr__(name: str):
    """Keep help and diagnostics available before optional ML imports succeed."""

    if name in {"BasicQuantumLayer", "QuantumLayer"}:
        from .nn import BasicQuantumLayer, QuantumLayer

        return {"BasicQuantumLayer": BasicQuantumLayer, "QuantumLayer": QuantumLayer}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
