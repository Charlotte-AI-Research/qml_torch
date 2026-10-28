"""Run one fair classical-versus-hybrid experiment and save its report."""

from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import Any

import torch
from torch import nn

from ..config import ExperimentConfig
from ..validation import DataBundle, preflight
from .models import ClassicalModel, HybridVQCModel


def set_seed(seed: int) -> None:
    """Seed Python and Torch for repeatable small simulator runs."""

    random.seed(seed)
    torch.manual_seed(seed)
    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:  # pragma: no cover - NumPy is a runtime dependency
        pass


def train_and_evaluate(
    model: nn.Module,
    data: DataBundle,
    config: ExperimentConfig,
) -> dict[str, float]:
    """Train one binary classifier and return loss, accuracy, and runtime."""

    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.BCEWithLogitsLoss()
    started = time.perf_counter()
    final_loss = 0.0

    model.train()
    for _ in range(config.epochs):
        optimizer.zero_grad()
        scores = model(data.x_train).reshape(-1)
        loss = criterion(scores, data.y_train)
        loss.backward()
        optimizer.step()
        final_loss = float(loss.detach())

    model.eval()
    with torch.no_grad():
        test_scores = model(data.x_test).reshape(-1)
        predictions = (test_scores >= 0).to(dtype=torch.float32)
        accuracy = float((predictions == data.y_test).to(dtype=torch.float32).mean())

    return {
        "final_train_loss": final_loss,
        "test_accuracy": accuracy,
        "runtime_seconds": time.perf_counter() - started,
    }


def _circuit_text(model: HybridVQCModel, sample: torch.Tensor) -> str:
    """Render one representative circuit for a saved report."""

    try:
        import pennylane as qml

        weights = model.quantum.quantum_layer.weights.detach()
        return str(qml.draw(model.quantum.circuit)(sample, weights))
    except Exception as exc:  # pragma: no cover - presentation should not lose metrics
        return f"Circuit diagram unavailable: {exc}"


def run_experiment(
    script_path: Path,
    config: ExperimentConfig,
    output_path: Path | None = None,
    data: DataBundle | None = None,
) -> dict[str, Any]:
    """Run the selected model(s), return a report, and optionally save JSON."""

    data = data or preflight(script_path, config)
    model_names = {
        "classical": ("classical",),
        "hybrid-vqc": ("hybrid-vqc",),
        "both": ("classical", "hybrid-vqc"),
    }[config.mode]
    model_results: dict[str, dict[str, float]] = {}
    circuit_text: str | None = None

    for name in model_names:
        set_seed(config.seed)
        if name == "classical":
            model: nn.Module = ClassicalModel(data.n_features)
        else:
            model = HybridVQCModel(config.n_qubits, shots=config.shots, layers=config.layers)
        model_results[name] = train_and_evaluate(model, data, config)
        if name == "hybrid-vqc":
            circuit_text = _circuit_text(model, data.x_train[0])

    report: dict[str, Any] = {
        "experiment": "qml-torch-v0.1",
        "seed": config.seed,
        "epochs": config.epochs,
        "settings": config.to_dict(),
        "data": {
            "training_samples": int(data.x_train.shape[0]),
            "test_samples": int(data.x_test.shape[0]),
            "features": data.n_features,
        },
        "models": model_results,
        "circuit": circuit_text,
        "note": "Experimental comparison only; results do not establish quantum advantage.",
    }
    if output_path is not None:
        output_path = output_path.expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
