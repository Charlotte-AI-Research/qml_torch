"""Loading and validation for the small documented ``train.py`` protocol."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from runpy import run_path
from typing import Any

import torch


@dataclass(frozen=True)
class DataBundle:
    """Validated binary-classification tensors used by one experiment."""

    x_train: torch.Tensor
    y_train: torch.Tensor
    x_test: torch.Tensor
    y_test: torch.Tensor

    @property
    def n_features(self) -> int:
        return int(self.x_train.shape[1])


def validate_data(values: Any) -> DataBundle:
    """Validate and normalize ``(x_train, y_train, x_test, y_test)``."""

    if not isinstance(values, (tuple, list)) or len(values) != 4:
        raise ValueError("get_data() must return (x_train, y_train, x_test, y_test)")
    x_train, y_train, x_test, y_test = values
    tensors = (x_train, y_train, x_test, y_test)
    if not all(isinstance(value, torch.Tensor) for value in tensors):
        raise TypeError("get_data() must return four PyTorch tensors")
    if any(value.is_complex() or value.layout != torch.strided for value in tensors):
        raise TypeError("data must contain dense, real-valued PyTorch tensors")
    if x_train.ndim != 2 or x_test.ndim != 2:
        raise ValueError("feature tensors must have shape [samples, features]")
    if x_train.shape[0] == 0 or x_test.shape[0] == 0:
        raise ValueError("training and test data cannot be empty")
    if x_train.shape[1] == 0:
        raise ValueError("the dataset must contain at least one feature")
    if x_train.shape[1] != x_test.shape[1]:
        raise ValueError("training and test data must have the same feature count")

    for labels in (y_train, y_test):
        if labels.ndim != 1 and not (labels.ndim == 2 and labels.shape[1] == 1):
            raise ValueError("labels must have shape [samples] or [samples, 1]")
        if not torch.all((labels == 0) | (labels == 1)):
            raise ValueError("labels must contain only 0 and 1")
    y_train = y_train.reshape(-1)
    y_test = y_test.reshape(-1)
    if y_train.numel() != x_train.shape[0]:
        raise ValueError("training labels must match the number of training samples")
    if y_test.numel() != x_test.shape[0]:
        raise ValueError("test labels must match the number of test samples")

    x_train = x_train.detach().to(dtype=torch.float32, device="cpu")
    x_test = x_test.detach().to(dtype=torch.float32, device="cpu")
    y_train = y_train.detach().to(dtype=torch.float32, device="cpu")
    y_test = y_test.detach().to(dtype=torch.float32, device="cpu")

    for name, tensor in (
        ("training features", x_train),
        ("test features", x_test),
        ("training labels", y_train),
        ("test labels", y_test),
    ):
        if not torch.isfinite(tensor).all():
            raise ValueError(f"{name} must contain only finite values")
    for name, labels in (("training labels", y_train), ("test labels", y_test)):
        if not torch.all((labels == 0) | (labels == 1)):
            raise ValueError(f"{name} must contain only 0 and 1")

    return DataBundle(x_train, y_train, x_test, y_test)


def load_training_script(script_path: Path) -> DataBundle:
    """Execute a trusted script and call its required ``get_data`` function."""

    script_path = script_path.expanduser().resolve()
    if not script_path.is_file():
        raise FileNotFoundError(f"training script not found: {script_path}")
    # Support local helper imports beside train.py without permanently modifying
    # the host process's import path (important for notebooks and library users).
    original_path = sys.path[:]
    try:
        sys.path.insert(0, str(script_path.parent))
        namespace = run_path(str(script_path), run_name="qml_torch_user_train")
        get_data = namespace.get("get_data")
        if not callable(get_data):
            raise ValueError(
                "training script must define get_data() returning "
                "(x_train, y_train, x_test, y_test)"
            )
        return validate_data(get_data())
    finally:
        sys.path[:] = original_path
