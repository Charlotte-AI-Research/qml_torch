# First quantum experiment

> **What:** A short path from installation to a repeatable experiment.
>
> **Why:** You can learn the interface before writing a quantum circuit.

## 1. Run the demo

From the repository root, install the inner package:

```bash
python -m pip install -e "./qml-torch[dev]"
qml-torch doctor
qml-torch demo
```

Open `qml-demo.html` in a browser. The dashboard shows accuracy, F1, runtime,
parameter counts, loss curves, confusion matrices, and the circuit used.

The demo is a tiny synthetic dataset. Good performance here is a demonstration
of the workflow, not a general performance claim.

## 2. Understand the five choices

- **Qubits:** the number of quantum inputs and outputs; match this to your features.
- **Mode:** run a classical model, a hybrid VQC, or both.
- **Encoding:** turns feature values into gate angles. Alpha 2 supports angle encoding.
- **Measurement:** converts the final quantum state into numbers. Pauli-Z gives one
  value per qubit, between -1 and 1.
- **Shots:** 0 means analytic expectations. A positive count samples the circuit,
  adding noise and usually more runtime.

A **VQC** is a quantum circuit with trainable rotation angles. A classical
optimizer updates them just as it updates neural network weights.

## 3. Bring your own features

```bash
qml-torch init train.py
qml-torch run train.py
```

The created script defines `get_data()`, returning:

```python
return x_train, y_train, x_test, y_test
```

Return real PyTorch tensors: feature matrices `[samples, features]` and binary
label vectors `[samples]` or `[samples, 1]`. The tool converts them to CPU
float32; preprocessing is your responsibility. If scaling is needed, fit it to
training data only, then apply it unchanged to test data.

You can also use the checked-in example from the inner package directory:

```bash
qml-torch run examples/train.py --no-prompt --epochs 20
```

## 4. Repeat and inspect

```bash
qml-torch run train.py --config results.json --output repeated.json
```

Compare the saved data fingerprints and settings. Runtimes naturally vary.
The HTML details include the environment and hidden circuit preset.

Loss curves use training data only; test metrics are computed after training.
F1 combines precision and recall, useful when accuracy hides class imbalance.
The confusion matrix shows actual labels on rows and predicted labels on columns.

The baseline is a linear classifier with fewer parameters than the VQC. These
are workflow comparisons, not parameter-matched research benchmarks.

## Troubleshooting

- No command: activate the environment used to install `qml-torch`.
- Wrong feature count: choose matching qubits (2–6) or classical mode.
- Invalid labels: use 0 and 1.
- Slow run: use analytic shots, fewer samples, or fewer epochs.
- Need details: add `--debug`; use `qml-torch doctor` to check the environment.
- Saved only JSON: remove `--no-html` to produce the dashboard.
