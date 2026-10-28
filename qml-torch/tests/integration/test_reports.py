"""Verify real training, reproducibility, artifact safety, and failure behavior."""

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from qml_torch.config import ExperimentConfig
from qml_torch.reporting.html import render_html
from qml_torch.training import run_experiment
from qml_torch.training.demo import make_demo_data


@pytest.mark.parametrize("shots", [None, 30])
def test_experiment_repeats_and_preserves_rng(shots: int | None, tmp_path: Path) -> None:
    data = make_demo_data()
    # Small genuine gradients through a quantum layer, including finite shots.
    data = type(data)(data.x_train[:4], data.y_train[:4], data.x_test[:4], data.y_test[:4])
    config = ExperimentConfig(epochs=2, shots=shots)
    state = torch.random.get_rng_state().clone()
    numpy_state = np.random.get_state()
    first = run_experiment(None, config, tmp_path / "result.json", data=data)
    second = run_experiment(None, config, data=data)
    assert torch.equal(state, torch.random.get_rng_state())
    np.testing.assert_equal(numpy_state, np.random.get_state())
    assert first["data"] == second["data"]
    assert first["status"] == "completed"
    for name, metrics in first["models"].items():
        assert metrics["loss_history"] == second["models"][name]["loss_history"]
        assert metrics["test_accuracy"] == second["models"][name]["test_accuracy"]
        assert sum(map(sum, metrics["confusion_matrix"])) == len(data.y_test)
        assert len(metrics["loss_history"]) == config.epochs
    assert json.loads((tmp_path / "result.json").read_text())["status"] == "completed"
    html = (tmp_path / "result.html").read_text()
    assert "<svg" in html and "Training loss by epoch" in html
    first["circuit"] = '<script>alert("untrusted")</script>'
    assert "<script>" not in render_html(first)
    assert "&lt;script&gt;" in render_html(first)


def test_invalid_supplied_data_cannot_bypass_preflight() -> None:
    with pytest.raises(ValueError, match="features must equal"):
        run_experiment(None, ExperimentConfig(n_qubits=3), data=make_demo_data())


@pytest.mark.parametrize("error", [RuntimeError("training failed"), KeyboardInterrupt()])
def test_failure_artifacts_are_never_successful(monkeypatch, tmp_path: Path, error) -> None:
    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr("qml_torch.training.experiment.train_and_evaluate", fail)
    path = tmp_path / "failed.json"
    with pytest.raises(type(error)):
        run_experiment(None, ExperimentConfig(epochs=1), path, data=make_demo_data())
    report = json.loads(path.read_text())
    assert report["status"] == ("cancelled" if isinstance(error, KeyboardInterrupt) else "failed")
    assert "Run stopped" in path.with_suffix(".html").read_text()


def test_refuse_non_json_output_before_running(tmp_path: Path) -> None:
    script = tmp_path / "train.py"
    script.write_text("raise RuntimeError('must not execute')")
    with pytest.raises(ValueError, match="output must end"):
        run_experiment(script, ExperimentConfig(), script)
    assert script.read_text() == "raise RuntimeError('must not execute')"
