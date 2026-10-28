# Examples

> **What:** This directory contains small runnable examples and the beginner
> tutorial.
>
> **Why:** Users learn the public API faster from a complete, working example than
> from internal source code alone.

This folder contains the first small binary-classification script. Future examples
must use only supported public interfaces and remain cheap enough to run on a
laptop.

## Run the first example

From the `qml-torch/` directory:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
python -m pip install -e ".[dev]"
qml-torch run examples/train.py
```

The command asks for qubits, model mode, encoding, measurement, and shots. For a
quick non-interactive run, use:

```bash
qml-torch run examples/train.py --no-prompt --epochs 10
```

## Training-script contract

Your script must define `get_data()` and return four PyTorch tensors in this order:

```python
x_train, y_train, x_test, y_test
```

Feature tensors have shape `[samples, features]`. Labels are binary (`0` or `1`).
For a hybrid run, the number of features must equal the selected number of qubits
in v0.1.

## What the output means

- **Classical accuracy:** the linear PyTorch baseline on the test set.
- **Hybrid VQC accuracy:** a trainable quantum layer followed by a linear output.
- **Shots:** `analytic` uses exact simulator expectations; a positive number uses
  sampled measurements.
- **Circuit:** the hidden library circuit used for the hybrid model.

The saved JSON report contains the settings, data shape, metrics, runtime, circuit,
and the warning that this is an experimental comparison—not a quantum-advantage
claim.

## Common fixes

- If the feature count does not match qubits, choose the same number or use
  `--mode classical`.
- If `get_data()` is missing, add it with the four-tensor return value above.
- If training is slow, use fewer epochs, analytic shots, or fewer qubits.
