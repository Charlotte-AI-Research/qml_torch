# QML Torch — project scaffold

QML Torch is planned as a beginner-friendly PyTorch extension for prototyping
hybrid quantum machine-learning models. A user should be able to bring ordinary
PyTorch training code, run a guided command, choose a few understandable quantum
options, and receive both a classical baseline and a hybrid/QML result.

> **Status:** planning and file structure only. Nothing inside this folder is an
> installable or working library yet. Implementation work is listed in
> [TASKS.md](TASKS.md).

## Intended first experience

The planned command is:

```text
qml-torch run train.py
```

It should:

1. preflight-check the user's script, data shapes, and environment;
2. ask only for the supported user-facing quantum options;
3. build safe defaults for the hidden quantum details;
4. train a classical baseline and a hybrid variational quantum circuit (VQC);
5. show the circuit, metrics, runtime, configuration, and useful warnings.

Importing `qml_torch` will not launch a prompt. The guided interface begins only
when the user invokes the CLI or an explicit future Python entry point. This keeps
imports predictable in notebooks, tests, and other packages.

## Configuration boundary

| User chooses | Hidden in v0.1 |
| --- | --- |
| Qubit count | PennyLane device selection |
| Encoding | Exact ansatz/gate layout |
| Circuit/model mode | Backend wiring and differentiation method |
| Shots (including analytic mode) | Weight shapes and QNode construction |
| Measurement | Reproducibility and batching plumbing |

The first backend is PennyLane and the first host framework is PyTorch. Qiskit and
TensorFlow are later extensions, not v0.1 requirements.

## Naming

- Distribution and CLI name: `qml-torch`
- Python import name: `qml_torch`

Python module names cannot contain hyphens, so the two forms are intentionally
different.

## Planned layout

```text
qml-torch/
├── TASKS.md
├── benchmarks/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CLI_SPEC.md
│   ├── OPEN_QUESTIONS.md
│   └── PRODUCT_SPEC.md
├── examples/
├── src/qml_torch/
│   ├── backends/
│   ├── circuits/
│   ├── cli/
│   ├── config/
│   ├── encodings/
│   ├── measurements/
│   ├── nn/
│   ├── reporting/
│   ├── training/
│   └── validation/
└── tests/
    ├── e2e/
    ├── integration/
    └── unit/
```

Each empty implementation area contains a short README defining its future
responsibility. No Python implementation files have been added yet.

## v0.1 success criteria

- A beginner can complete one small binary-classification experiment on a CPU
  simulator without selecting a backend or writing a quantum circuit.
- The quantum layer accepts batched classical features and returns one value per
  qubit for each sample.
- Preflight validation catches unsupported shapes and invalid choices before a
  long training run.
- The result reports a fair classical baseline next to the hybrid result without
  claiming quantum advantage.
- The same seed and configuration reproduce the experiment within documented
  simulator tolerances.

## Deliberate non-goals for v0.1

- Qiskit, TensorFlow, quantum hardware, or distributed training
- automatic support for arbitrary user training scripts
- a user-defined ansatz builder
- claims that a quantum model is faster or more accurate
- large datasets or production-scale benchmarking
