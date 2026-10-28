"""Public API for the QML Torch beginner package."""

from .config import ExperimentConfig
from .nn import BasicQuantumLayer, QuantumLayer

__version__ = "0.1.0"

__all__ = ["BasicQuantumLayer", "ExperimentConfig", "QuantumLayer", "__version__"]
