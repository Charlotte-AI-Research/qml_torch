"""Train comparable models and preserve enough evidence to explain each result."""

from __future__ import annotations

import hashlib
import platform
import random
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from importlib.metadata import version
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn

from ..config import ExperimentConfig
from ..validation import DataBundle, preflight
from .models import ClassicalModel, HybridVQCModel

EpochCallback = Callable[[str, int, float], None]
CIRCUIT_PRESET = "ry-rz-ry-ring-v1"


def set_seed(seed: int) -> None:
    """Seed Python, NumPy, and Torch before model initialization."""

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


@contextmanager
def isolated_seed(seed: int) -> Iterator[None]:
    """Reproduce experiments without changing a caller's random-number streams."""

    python_state, numpy_state = random.getstate(), np.random.get_state()
    try:
        with torch.random.fork_rng(devices=[]):
            set_seed(seed)
            yield
    finally:
        random.setstate(python_state)
        np.random.set_state(numpy_state)


def train_and_evaluate(
    model: nn.Module,
    data: DataBundle,
    config: ExperimentConfig,
    on_epoch: Callable[[int, float], None] | None = None,
) -> dict[str, Any]:
    """Train full-batch binary classification with held-out evaluation only at the end."""

    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.BCEWithLogitsLoss()
    started = time.perf_counter()
    history: list[float] = []

    model.train()
    for epoch in range(1, config.epochs + 1):
        optimizer.zero_grad()
        scores = model(data.x_train).reshape(-1)
        loss = criterion(scores, data.y_train)
        if not torch.isfinite(loss):
            raise ValueError("Training loss became non-finite; reduce the learning rate.")
        loss.backward()
        if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in model.parameters()):
            raise ValueError("Training gradients became non-finite; check the feature scale.")
        optimizer.step()
        history.append(float(loss.detach()))
        if on_epoch is not None:
            on_epoch(epoch, history[-1])

    model.eval()
    with torch.no_grad():
        test_scores = model(data.x_test).reshape(-1)
        if not torch.isfinite(test_scores).all():
            raise ValueError("Model produced non-finite predictions.")
        predictions = (test_scores >= 0).long()
        labels = data.y_test.long()
        accuracy = float((predictions == labels).float().mean())
        confusion = torch.bincount(labels * 2 + predictions, minlength=4).reshape(2, 2)
        tn, fp, fn, tp = [int(value) for value in confusion.reshape(-1)]
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0

    return {
        "final_train_loss": history[-1],
        "test_accuracy": accuracy,
        "test_loss": float(criterion(test_scores, data.y_test)),
        "precision": precision,
        "recall": recall,
        "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
        "confusion_matrix": [[tn, fp], [fn, tp]],
        "loss_history": history,
        "parameter_count": sum(p.numel() for p in model.parameters() if p.requires_grad),
        "runtime_seconds": time.perf_counter() - started,
    }


def _circuit_text(model: HybridVQCModel, sample: torch.Tensor) -> str:
    """Draw the trained preset down to individual gates."""

    import pennylane as qml

    return str(
        qml.draw(model.quantum.circuit, level="device")(
            sample, model.quantum.quantum_layer.weights.detach()
        )
    )


def _fingerprint(data: DataBundle) -> str:
    """Identify the exact validated tensors without embedding the user's dataset."""

    digest = hashlib.sha256()
    for tensor in (data.x_train, data.y_train, data.x_test, data.y_test):
        digest.update(str(tuple(tensor.shape)).encode())
        digest.update(tensor.contiguous().numpy().tobytes())
    return digest.hexdigest()


def run_experiment(
    script_path: Path | None,
    config: ExperimentConfig,
    output_path: Path | None = None,
    data: DataBundle | None = None,
    *,
    html_report: bool = True,
    on_epoch: EpochCallback | None = None,
) -> dict[str, Any]:
    """Run selected models, optionally save JSON plus an offline HTML dashboard.

    Existing JSON keys are retained for alpha-1 callers. Finite-shot reproducibility
    requires identical settings, data, dependency versions, and simulator operations.
    """

    from .. import __version__
    from ..reporting.artifacts import save_reports

    # Refuse to replace the user's training code before executing it.
    if output_path is not None:
        output_path = output_path.expanduser().resolve()
        if output_path.suffix.lower() != ".json":
            raise ValueError("output must end in .json; the HTML report is saved beside it")
        if script_path is not None and script_path.expanduser().resolve() in (
            output_path,
            output_path.with_suffix(".html") if html_report else output_path,
        ):
            raise ValueError("choose an output path different from the training script")

    with isolated_seed(config.seed):
        data = preflight(script_path, config, data=data)
    model_names = ("classical", "hybrid-vqc") if config.mode == "both" else (config.mode,)
    model_results: dict[str, Any] = {}
    circuit_text: str | None = None
    warnings: list[str] = []
    if config.shots is not None:
        warnings.append("Finite-shot estimates are noisy and slower than analytic simulation.")
    for name, labels in (("training", data.y_train), ("test", data.y_test)):
        if labels.unique().numel() < 2:
            warnings.append(f"The {name} split contains one class; accuracy may be misleading.")
    if len(data.x_train) > 512 or config.epochs > 100:
        warnings.append("This exceeds the small demo workload; simulator runs may take longer.")

    report: dict[str, Any] = {
        "schema_version": 2,
        "status": "running",
        "experiment": "qml-torch-v0.1",
        "version": __version__,
        "seed": config.seed,
        "epochs": config.epochs,
        "settings": config.to_dict(),
        "source": str(script_path.expanduser().resolve()) if script_path else "built-in-demo",
        "data": {
            "training_samples": len(data.x_train),
            "test_samples": len(data.x_test),
            "features": data.n_features,
            "fingerprint_sha256": _fingerprint(data),
        },
        "implementation": {
            "backend": "default.qubit",
            "circuit_preset": CIRCUIT_PRESET,
            "encoding_gate": "Y",
            "differentiation": "backprop" if config.shots is None else "parameter-shift",
            "feature_mapping": "one feature per qubit; no automatic preprocessing",
            "baseline": "linear logistic classifier (not parameter-matched)",
            "optimizer": "Adam",
            "batching": "full-batch",
            "decision_threshold_logit": 0.0,
        },
        "environment": {
            "python": platform.python_version(),
            **{name: version(name) for name in ("torch", "pennylane", "numpy")},
        },
        "models": model_results,
        "circuit": circuit_text,
        "warnings": warnings,
        "note": "Experimental comparison only; results do not establish quantum advantage.",
    }
    if output_path is not None:
        save_reports(report, output_path, html_report=html_report)
    try:
        for name in model_names:
            with isolated_seed(config.seed):
                if name == "classical":
                    model: nn.Module = ClassicalModel(data.n_features)
                else:
                    model = HybridVQCModel(
                        config.n_qubits, config.shots, config.layers, seed=config.seed
                    )

                def progress(epoch: int, loss: float, model_name: str = name) -> None:
                    if on_epoch is not None:
                        on_epoch(model_name, epoch, loss)

                model_results[name] = train_and_evaluate(model, data, config, progress)
                if isinstance(model, HybridVQCModel):
                    report["circuit"] = _circuit_text(model, data.x_train[0])
    except (Exception, KeyboardInterrupt) as exc:
        report["status"] = "cancelled" if isinstance(exc, KeyboardInterrupt) else "failed"
        report["error"] = str(exc) or "Cancelled by user"
        if output_path is not None:
            save_reports(report, output_path, html_report=html_report)
        raise
    report["status"] = "completed"
    if output_path is not None:
        save_reports(report, output_path, html_report=html_report)
    return report
