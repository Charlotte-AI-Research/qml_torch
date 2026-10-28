"""Checks that run before a potentially slow simulator training job."""

from __future__ import annotations

from pathlib import Path

from ..config import ExperimentConfig
from .data import DataBundle, load_training_script, validate_data


def preflight(
    script_path: Path | None,
    config: ExperimentConfig,
    data: DataBundle | None = None,
) -> DataBundle:
    """Validate the user script, data shape, and quantum feature contract."""

    if data is None:
        if script_path is None:
            raise ValueError("provide a training script or a DataBundle")
        data = load_training_script(script_path)
    data = validate_data((data.x_train, data.y_train, data.x_test, data.y_test))
    if config.mode in {"hybrid-vqc", "both"} and data.n_features != config.n_qubits:
        raise ValueError(
            "the number of features must equal n_qubits for the v0.1 quantum layer "
            f"(found {data.n_features} features and {config.n_qubits} qubits)"
        )
    return data
