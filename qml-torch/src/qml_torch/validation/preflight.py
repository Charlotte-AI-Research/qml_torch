"""Checks that run before a potentially slow simulator training job."""

from __future__ import annotations

from pathlib import Path

from ..config import ExperimentConfig
from .data import DataBundle, load_training_script


def preflight(
    script_path: Path,
    config: ExperimentConfig,
    data: DataBundle | None = None,
) -> DataBundle:
    """Validate the user script, data shape, and quantum feature contract."""

    data = data or load_training_script(script_path)
    if config.mode in {"hybrid-vqc", "both"} and data.n_features != config.n_qubits:
        raise ValueError(
            "the number of features must equal n_qubits for the v0.1 quantum layer "
            f"(found {data.n_features} features and {config.n_qubits} qubits)"
        )
    return data
