"""Exercise malformed settings and tensors before a simulator run starts."""

import pytest
import torch

from qml_torch.config import ExperimentConfig
from qml_torch.validation import validate_data


@pytest.mark.parametrize(
    "values",
    [
        {"shots": 1.5},
        {"shots": True},
        {"n_qubits": 2.5},
        {"epochs": False},
        {"layers": 1.2},
        {"learning_rate": float("nan")},
        {"learning_rate": float("inf")},
        {"seed": -1},
        {"seed": 2**32},
        {"seed": True},
        {"learning_rate": "fast"},
    ],
)
def test_reject_invalid_settings(values) -> None:
    with pytest.raises(ValueError):
        ExperimentConfig(**values)


def test_misspelled_config_keys_are_not_ignored() -> None:
    with pytest.raises(ValueError, match="unknown configuration.*qubits"):
        ExperimentConfig.from_dict({"qubits": 4})


@pytest.mark.parametrize(
    "labels",
    [
        torch.tensor([0.0, 1.0000000001], dtype=torch.float64),
        torch.tensor([0.0, float("nan")]),
        torch.tensor([0.0 + 1j, 1.0 + 0j]),
        torch.zeros(1, 2),
    ],
)
def test_reject_invalid_labels_before_conversion(labels) -> None:
    with pytest.raises((TypeError, ValueError)):
        validate_data((torch.ones(2, 2), labels, torch.ones(2, 2), torch.tensor([0, 1])))
