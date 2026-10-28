"""Tests for the beginner-facing configuration and data protocol."""

from pathlib import Path

import pytest
import torch

from qml_torch.config import ExperimentConfig
from qml_torch.validation import load_training_script, validate_data


def test_config_defaults_are_serializable() -> None:
    config = ExperimentConfig()
    assert config.to_dict()["mode"] == "both"
    assert config.to_dict()["shots"] is None


def test_config_rejects_invalid_shots() -> None:
    with pytest.raises(ValueError, match="shots"):
        ExperimentConfig(shots=0)


def test_data_protocol_normalizes_labels() -> None:
    bundle = validate_data(
        (
            torch.ones(2, 2),
            torch.tensor([[0], [1]]),
            torch.zeros(2, 2),
            torch.tensor([0, 1]),
        )
    )
    assert bundle.n_features == 2
    assert bundle.y_train.shape == (2,)


def test_example_script_loads() -> None:
    example = Path(__file__).parents[2] / "examples" / "train.py"
    bundle = load_training_script(example)
    assert bundle.x_train.shape[1] == 2
