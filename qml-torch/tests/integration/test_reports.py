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
from qml_torch.training.experiment import train_and_evaluate
from qml_torch.validation import DataBundle


class ControlledModel(torch.nn.Module):
    """Model that produces predictable logits for metric testing."""

    def __init__(self):
        super().__init__()
        self.anchor = torch.nn.Parameter(torch.tensor(0.0))

    def forward(self, x):
        return x[:, 0] + self.anchor * 0


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
    html = (tmp_path / "result.html").read_text(encoding="utf-8")
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

def test_training_metrics_with_correct_and_incorrect_predictions():
    '''
    Binary classification metrics:
    Accuracy = (TP + TN) / (TP + TN + FP + FN)
    Precision = TP / (TP + FP)
    Recall = TP / (TP + FN)
    F1 = 2 * Precision * Recall / (Precision + Recall)
    
    Confusion matrix layout: [[TN, FP], [FN, TP]]
    '''
    data = DataBundle(
        x_train=torch.tensor([[-1.0], [1.0], [1.0], [-1.0]]),
        y_train=torch.tensor([0.0, 1.0, 1.0, 0.0]),
        x_test=torch.tensor([[-1.0], [1.0], [1.0], [-1.0]]),
        y_test=torch.tensor([1.0, 1.0, 0.0, 0.0]),
    )

    config = ExperimentConfig(mode="classical", epochs=2, seed=42)

    metrics = train_and_evaluate(
        ControlledModel(),
        data,
        config,
    )

    assert metrics["confusion_matrix"] == [[1, 1], [1, 1]]
    assert metrics["test_accuracy"] == pytest.approx(0.5)
    assert metrics["precision"] == pytest.approx(0.5)
    assert metrics["recall"] == pytest.approx(0.5)
    assert metrics["f1"] == pytest.approx(0.5)


def test_training_metrics_with_no_positive_predictions():
    data = DataBundle(
        x_train=torch.tensor([[-1.0], [-1.0], [-1.0], [-1.0]]),
        y_train=torch.tensor([0.0, 0.0, 1.0, 1.0]),
        x_test=torch.tensor([[-1.0], [-1.0], [-1.0], [-1.0]]),
        y_test=torch.tensor([1.0, 1.0, 0.0, 0.0]),
    )

    config = ExperimentConfig(mode="classical", epochs=1, seed=42)

    metrics = train_and_evaluate(
        ControlledModel(),
        data,
        config,
    )

    assert metrics["confusion_matrix"] == [[2, 0], [2, 0]]
    assert metrics["test_accuracy"] == pytest.approx(0.5)
    assert metrics["precision"] == pytest.approx(0.0)
    assert metrics["recall"] == pytest.approx(0.0)
    assert metrics["f1"] == pytest.approx(0.0)
