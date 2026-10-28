# Changelog

All notable changes to QML Torch are recorded here.

## [0.1.0a1] — 2026-10-28

First public alpha release of the nested `qml-torch` package.

### Added

- PyTorch `QuantumLayer` backed by PennyLane's local simulator.
- Angle encoding and per-qubit Pauli-Z expectation measurements.
- Classical, hybrid-VQC, and combined comparison modes.
- Guided command: `qml-torch run train.py`.
- Non-interactive CLI flags for repeatable runs.
- `get_data()` protocol for small binary-classification experiments.
- JSON reports with settings, metrics, runtimes, and circuit diagrams.
- Beginner example, package metadata, contribution guidance, and test suites.

### Alpha limitations

- Simulator only; Qiskit and hardware backends are not included.
- PyTorch is the only supported host framework.
- Angle encoding and Pauli-Z measurements are the only v0.1 choices.
- Hybrid runs require the number of features to equal the number of qubits.
- The training script is executed as trusted local code.
- Results are experimental comparisons and do not establish quantum advantage.
