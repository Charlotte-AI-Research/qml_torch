"""Typed, serializable settings for one QML Torch experiment."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

VALID_MODES = ("classical", "hybrid-vqc", "both")
VALID_ENCODINGS = ("angle",)
VALID_MEASUREMENTS = ("pauli-z",)

Mode = Literal["classical", "hybrid-vqc", "both"]
Encoding = Literal["angle"]
Measurement = Literal["pauli-z"]


@dataclass(frozen=True)
class ExperimentConfig:
    """Settings a beginner may choose, plus small reproducibility controls."""

    n_qubits: int = 2
    mode: Mode = "both"
    encoding: Encoding = "angle"
    shots: int | None = None
    measurement: Measurement = "pauli-z"
    epochs: int = 10
    learning_rate: float = 0.03
    seed: int = 7
    layers: int = 1

    def __post_init__(self) -> None:
        if not 2 <= self.n_qubits <= 6:
            raise ValueError("n_qubits must be between 2 and 6 for the v0.1 simulator")
        if self.mode not in VALID_MODES:
            raise ValueError("mode must be 'classical', 'hybrid-vqc', or 'both'")
        if self.encoding not in VALID_ENCODINGS:
            raise ValueError("only 'angle' encoding is supported in v0.1")
        if self.measurement not in VALID_MEASUREMENTS:
            raise ValueError("only 'pauli-z' measurement is supported in v0.1")
        if self.shots is not None and self.shots < 1:
            raise ValueError("shots must be None (analytic mode) or a positive integer")
        if self.epochs < 1:
            raise ValueError("epochs must be at least 1")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.layers < 1:
            raise ValueError("layers must be at least 1")

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-friendly settings."""

        return asdict(self)

    @classmethod
    def from_dict(cls, values: dict[str, Any]) -> ExperimentConfig:
        """Build settings from a JSON/config dictionary."""

        allowed = {field for field in cls.__dataclass_fields__}
        return cls(**{key: value for key, value in values.items() if key in allowed})
