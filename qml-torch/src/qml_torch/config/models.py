"""Typed, serializable settings for one QML Torch experiment."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite
from typing import Any, Literal

VALID_MODES = ("classical", "hybrid-vqc", "both")
VALID_ENCODINGS = ("angle",)
VALID_MEASUREMENTS = ("pauli-z",)

Mode = Literal["classical", "hybrid-vqc", "both"]
Encoding = Literal["angle"]
Measurement = Literal["pauli-z"]


def positive_integer(value: Any, name: str) -> None:
    """Reject booleans, fractions, and nonpositive counts before simulation."""

    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


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
        for name in ("n_qubits", "epochs", "layers"):
            positive_integer(getattr(self, name), name)
        if not 2 <= self.n_qubits <= 6:
            raise ValueError("n_qubits must be between 2 and 6 for the v0.1 simulator")
        if self.mode not in VALID_MODES:
            raise ValueError("mode must be 'classical', 'hybrid-vqc', or 'both'")
        if self.encoding not in VALID_ENCODINGS:
            raise ValueError("only 'angle' encoding is supported in v0.1")
        if self.measurement not in VALID_MEASUREMENTS:
            raise ValueError("only 'pauli-z' measurement is supported in v0.1")
        if self.shots is not None:
            positive_integer(self.shots, "shots")
        if (
            isinstance(self.learning_rate, bool)
            or not isinstance(self.learning_rate, (int, float))
            or not isfinite(self.learning_rate)
            or self.learning_rate <= 0
        ):
            raise ValueError("learning_rate must be a finite positive number")
        if type(self.seed) is not int or not 0 <= self.seed < 2**32:
            raise ValueError("seed must be an integer between 0 and 4294967295")

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-friendly settings."""

        return asdict(self)

    @classmethod
    def from_dict(cls, values: dict[str, Any]) -> ExperimentConfig:
        """Build settings from a JSON/config dictionary."""

        unknown = values.keys() - cls.__dataclass_fields__.keys()
        if unknown:
            raise ValueError(f"unknown configuration field(s): {', '.join(sorted(unknown))}")
        return cls(**values)
