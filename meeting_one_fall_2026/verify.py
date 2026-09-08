"""Checks for the Meeting 1 deliverable."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_starter():
    spec = importlib.util.spec_from_file_location(
        "meeting_one_starter", Path(__file__).with_name("starter_experiment.py")
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load starter_experiment.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    starter = load_starter()
    x_train, x_test, y_train, _y_test = starter.make_dataset()
    assert x_train.shape == (90, 2)
    assert x_test.shape == (30, 2)
    assert str(y_train.dtype) == "torch.float32"
    baseline = starter.run_baseline()
    assert 0.0 <= baseline["accuracy"] <= 1.0
    print("Environment and baseline checks passed.")
    print("Next: implement build_quantum_layer, then rerun this check and --quantum.")


if __name__ == "__main__":
    main()
