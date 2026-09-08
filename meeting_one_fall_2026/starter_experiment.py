"""Meeting 1 starter: build a citable QML Torch research artifact.

Run the baseline before editing the TODOs:

    python starter_experiment.py --baseline

Then implement ``build_quantum_layer`` and run ``--quantum``. The classical
model is a control for validating the experiment, not the project's headline.
"""

from __future__ import annotations

import argparse
import time
from typing import Any

import numpy as np
import pennylane as qml  # noqa: F401 - used by the build_quantum_layer TODO
import torch
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def make_dataset(seed: int = 7) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Create one fixed, small classification task for both model families."""

    features, labels = make_moons(n_samples=120, noise=0.16, random_state=seed)
    features = StandardScaler().fit_transform(features).astype(np.float32)
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.25, random_state=seed, stratify=labels
    )
    return (
        torch.from_numpy(x_train),
        torch.from_numpy(x_test),
        torch.from_numpy(y_train.astype(np.float32)),
        torch.from_numpy(y_test.astype(np.float32)),
    )


def set_seed(seed: int) -> None:
    """Set the random generators used by this experiment."""

    np.random.seed(seed)
    torch.manual_seed(seed)


def run_baseline(seed: int = 7) -> dict[str, float]:
    """Fit the fixed classical control and return auditable metrics."""

    x_train, x_test, y_train, y_test = make_dataset(seed)
    started = time.perf_counter()
    model = LogisticRegression(random_state=seed, max_iter=500)
    model.fit(x_train.numpy(), y_train.numpy())
    elapsed = time.perf_counter() - started
    return {"accuracy": float(model.score(x_test.numpy(), y_test.numpy())), "seconds": elapsed}


def build_quantum_layer(n_qubits: int = 2, n_layers: int = 1) -> Any:
    """Return a trainable two-feature quantum layer.

    TODO (meeting work): define the QNode with ``inputs`` and ``weights``,
    encode the two input features, add the trainable circuit, return one
    expectation value per qubit, and wrap it with ``qml.qnn.TorchLayer``.
    """

    if n_qubits != 2:
        raise ValueError("Meeting 1 uses exactly two qubits")
    if n_layers < 1:
        raise ValueError("n_layers must be positive")
    raise NotImplementedError("Implement the QNode and TorchLayer during Meeting 1")


def build_hybrid_model(seed: int = 7) -> torch.nn.Module:
    """Build the hybrid classifier after the layer TODO is implemented."""

    set_seed(seed)
    layer = build_quantum_layer()
    return torch.nn.Sequential(layer, torch.nn.Linear(2, 1))


def train_hybrid(seed: int = 7, epochs: int = 20) -> dict[str, float]:
    """Train and evaluate the hybrid classifier."""

    x_train, x_test, y_train, y_test = make_dataset(seed)
    model = build_hybrid_model(seed)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
    criterion = torch.nn.BCEWithLogitsLoss()
    started = time.perf_counter()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = criterion(model(x_train).squeeze(-1), y_train)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        predictions = (model(x_test).squeeze(-1) > 0).float()
    elapsed = time.perf_counter() - started
    accuracy = float((predictions == y_test).float().mean())
    return {"accuracy": accuracy, "seconds": elapsed, "loss": float(loss.detach())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", action="store_true", help="run the classical baseline")
    parser.add_argument("--quantum", action="store_true", help="run the completed hybrid model")
    args = parser.parse_args()
    if args.baseline == args.quantum:
        parser.error("choose exactly one of --baseline or --quantum")
    result = run_baseline() if args.baseline else train_hybrid()
    print(" ".join(f"{key}={value:.4f}" for key, value in result.items()))


if __name__ == "__main__":
    main()
