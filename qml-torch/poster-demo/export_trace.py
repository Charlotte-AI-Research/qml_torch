"""Record a real ``qml-torch demo`` training run for the looping poster animation.

Run from the repository root:

    python qml-torch/poster-demo/export_trace.py

It trains the same hybrid model as ``qml-torch demo --epochs 60`` (seed 7) with
the library's own training loop, snapshots every parameter after each epoch, and
embeds that trace in ``index.html`` next to this file. The page replays it, so
every number in the animation comes from the real run. The page stays a single
self-contained file that works offline.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import torch

from qml_torch.config import ExperimentConfig
from qml_torch.training.demo import make_demo_data
from qml_torch.training.experiment import isolated_seed, train_and_evaluate
from qml_torch.training.models import ClassicalModel, HybridVQCModel

PAGE = Path(__file__).with_name("index.html")
MARKERS = re.compile(r"/\* TRACE:BEGIN \*/.*?/\* TRACE:END \*/", re.S)


def snapshot(model: HybridVQCModel) -> dict:
    return {
        "q": model.quantum.quantum_layer.weights.detach().reshape(-1, 3).tolist(),
        "w": model.output.weight.detach().reshape(-1).tolist(),
        "b": float(model.output.bias.detach()),
    }


def train_accuracy(model: torch.nn.Module, x: torch.Tensor, y: torch.Tensor) -> float:
    with torch.no_grad():
        return float(((model(x).reshape(-1) >= 0).float() == y).float().mean())


def main() -> None:
    config = ExperimentConfig(epochs=60)
    data = make_demo_data(config.n_qubits, config.seed)

    frames: list[dict] = []
    with isolated_seed(config.seed):
        model = HybridVQCModel(config.n_qubits, config.shots, config.layers, seed=config.seed)
        frames.append(snapshot(model) | {"acc": train_accuracy(model, data.x_train, data.y_train)})

        def on_epoch(epoch: int, loss: float) -> None:
            # Called after optimizer.step(); `loss` was measured before that step.
            frames[-1]["loss"] = loss
            frames.append(
                snapshot(model) | {"acc": train_accuracy(model, data.x_train, data.y_train)}
            )

        hybrid = train_and_evaluate(model, data, config, on_epoch)

    with torch.no_grad():
        criterion = torch.nn.BCEWithLogitsLoss()
        frames[-1]["loss"] = float(criterion(model(data.x_train).reshape(-1), data.y_train))
        sample = data.x_train[:4]
        check = {
            "x": sample.tolist(),
            "z": model.quantum(sample).tolist(),
            "score": model(sample).reshape(-1).tolist(),
        }

    with isolated_seed(config.seed):
        classical = train_and_evaluate(ClassicalModel(data.n_features), data, config)

    trace = {
        "source": "qml-torch 0.1.0a2 demo, seed 7, 60 epochs, Adam lr 0.03, analytic simulator",
        "train": {"x": data.x_train.tolist(), "y": data.y_train.int().tolist()},
        "test": {"x": data.x_test.tolist(), "y": data.y_test.int().tolist()},
        "frames": frames,
        "hybrid": {k: v for k, v in hybrid.items() if k != "loss_history"},
        "classical": {k: v for k, v in classical.items() if k != "loss_history"},
        "check": check,
    }
    payload = "/* TRACE:BEGIN */window.TRACE = " + json.dumps(trace, separators=(",", ":"))
    payload += ";/* TRACE:END */"
    html = PAGE.read_text()
    if not MARKERS.search(html):
        raise SystemExit(f"{PAGE} is missing the TRACE:BEGIN/END markers")
    PAGE.write_text(MARKERS.sub(lambda _: payload, html, count=1))
    print(f"embedded {len(frames)} frames in {PAGE}")
    print(f"hybrid: train loss {frames[0]['loss']:.3f} -> {frames[-1]['loss']:.3f}, "
          f"test acc {hybrid['test_accuracy']:.2f}")


if __name__ == "__main__":
    main()
