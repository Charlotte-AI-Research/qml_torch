# Changelog

All notable changes to QML Torch are recorded here.

## [0.1.0a2] — 2026-10-28

### Added

- `qml-torch demo`: a complete built-in experiment after installation.
- `qml-torch init` for starter scripts and `qml-torch doctor` for diagnostics.
- Progress bars, aligned terminal results, and gate-level circuit diagrams.
- Offline HTML dashboards with SVG learning curves and confusion matrices.
- Precision, recall, F1, test loss, training histories, and model parameter counts.
- Saved JSON settings can be replayed using `--config`; flags override them.
- Dataset fingerprints, dependency provenance, and explicit run status.
- Atomic report writes and failed/cancelled training reports.

### Fixed

- Seeded finite-shot simulator execution and gradients through upstream layers.
- Input/configuration validation, including fractions, booleans, and NaN settings.
- Misspelled configuration keys now fail instead of being silently ignored.
- User scripts can import helpers from their own directory.
- Experimental runs restore the calling process's random streams.
- Source downloads include examples, tests, documentation, and release notes.

### Compatibility

- Alpha 1 remains available as previously uploaded; alpha 2 uses a new version.
- Python 3.11+ and PennyLane 0.45.x are required for the supported QNode API.
- Existing basic `QuantumLayer` calls and alpha-1 JSON result keys are retained.
- The baseline remains linear and is explicitly described as not parameter-matched.

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
