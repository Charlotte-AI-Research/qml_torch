# QML Torch
### From features to qubits.

> **What:** A small PyTorch extension that makes a first quantum ML experiment
> approachable.
>
> **Why:** You should be able to try a quantum layer without first learning how
> to construct a device, QNode, or ansatz.

**0.1.0a2 · Educational alpha · Python 3.11+ · PennyLane + PyTorch**

Run a comparison, watch both models train, and open a complete experiment report
in your browser. The library handles the circuit and simulator setup.

## Try it

From the **repository root** (the folder containing the inner `qml-torch/` directory):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e "./qml-torch[dev]"
qml-torch doctor
qml-torch demo
```

Windows activation: `.venv\Scripts\activate`.

The demo includes balanced synthetic training/test data and needs no download.
It saves `qml-demo.json` and `qml-demo.html` in your current directory. Open the
HTML file in a browser; the report works offline.

The PyPI distribution is named `qml-torch`; the Python import is `qml_torch`.
After alpha 2 is published, `python -m pip install qml-torch==0.1.0a2` will install it.
Until then, use the source installation above.

## Your first model comparison

```bash
qml-torch init train.py
qml-torch run train.py
```

The wizard checks your script, infers a qubit default from the feature count, and
asks about qubits, model mode, encoding, measurement, and shots. Backend and
ansatz choices stay inside the library.

For an unattended run:

```bash
qml-torch run train.py --no-prompt --epochs 20 --seed 7 --output results.json
```

Supported model modes: `classical`, `hybrid-vqc`, and `both`.

## What you get

- A terminal comparison of test accuracy, F1, trainable parameters, and runtime.
- An offline HTML dashboard with learning curves, confusion matrices, circuit
  gates, settings, and dependency versions.
- Machine-readable JSON with loss history, precision, recall, test loss, data
  fingerprint, seed, and the hidden circuit preset.
- Explicit `running`, `completed`, `failed`, or `cancelled` status for training
  artifacts. Writes are atomic per file.

Repeat a run from its saved settings:

```bash
qml-torch run train.py --config results.json --output repeated.json
qml-torch demo --config qml-demo.json --output demo-repeated.json
```

Flags override saved settings. Dataset fingerprints let you check that a repeated
run actually used the same data. A user script must also be deterministic; a seed
does not control external files or network data.

## Use it inside PyTorch

```python
import torch
from qml_torch import QuantumLayer

model = torch.nn.Sequential(
    QuantumLayer(qubits=2),
    torch.nn.Linear(2, 1),
)
logits = model(torch.rand(8, 2))
loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, torch.ones(8, 1))
loss.backward()
```

The layer maps `[batch, qubits]` to `[batch, qubits]` and also accepts a single
sample shaped `[qubits]`. It returns one Pauli-Z expectation per qubit. Quantum
weights appear in `model.parameters()` and `state_dict()`.

## Bring your own data

A trusted Python script must define:

```python
def get_data():
    return x_train, y_train, x_test, y_test
```

All four values are real PyTorch tensors. Features use `[samples, features]`,
labels use `[samples]` or `[samples, 1]`, and labels must be 0 or 1. Hybrid runs
require one feature per qubit. The tool converts tensors to CPU float32 and does
not silently scale, truncate, or project features. Angle inputs are radians.

## Honest comparisons

The models share data, epochs, learning rate, and seed. The baseline is a linear
logistic classifier; the hybrid adds a VQC and a linear readout. They are **not
parameter-matched**: the report shows their sizes. One tiny test split or one seed
cannot establish quantum advantage.

Analytic simulation is the default. To sample measurements:

```bash
qml-torch demo --shots 100 --epochs 3 --output sampled.json
```

Sampled runs use parameter-shift gradients and can be much slower. Reproducibility
is tested for identical seeds, tensors, simulator operations, and dependency
versions. It is not promised across platforms or dependency upgrades.

## Commands

| Command | Purpose |
| --- | --- |
| `qml-torch demo` | Run the included comparison immediately |
| `qml-torch init train.py` | Create an editable starter script without overwriting files |
| `qml-torch run train.py` | Guided experiment with your data |
| `qml-torch doctor` | Check versions and a quantum forward/backward pass |
| `qml-torch version` | Show the installed alpha version |

Use `--no-html` for JSON only and `--debug` for troubleshooting tracebacks.

## Limits and development

The CLI supports 2–6 qubits, binary classification, angle encoding, Pauli-Z
measurement, CPU execution, and one versioned circuit preset. PennyLane 0.45.x
is the tested backend series. Qiskit, TensorFlow, hardware, large datasets, and
custom circuits remain future work.

From the inner `qml-torch/` directory:

```bash
ruff check src tests
pytest -q
python -m build
```

See [the tutorial](examples/README.md), [architecture](docs/ARCHITECTURE.md),
[release instructions](docs/RELEASING.md), [changelog](CHANGELOG.md), and
[MIT license](LICENSE). Every source module begins with a short purpose docstring.
