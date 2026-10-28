# Open product decisions

> **What:** This file lists choices the team still needs to make before coding.
>
> **Why:** Writing unclear decisions down prevents contributors from building
> different meanings for terms such as `Standard` or feature-to-qubit mapping.

The v0.1 decisions below are now resolved and reflected in the implementation.
Keep later changes in this file so the CLI and tests do not silently drift.

## Resolved v0.1 decisions

### 1. What does `Standard` mean?

The brief says “Standard and VQC,” but `Standard` could mean a classical model, a
fixed non-trainable quantum circuit, or a named circuit preset. The default
recommendation is to present model modes as `classical`, `hybrid-vqc`, and `both`,
while reserving circuit-type names for actual quantum circuit presets.

**Status:** resolved — model modes are `classical`, `hybrid-vqc`, and `both`.

### 2. What contract does `train.py` expose?

Supporting arbitrary PyTorch scripts safely and reliably is not realistic for the
first release. Define the smallest explicit protocol: for example, one function
that returns train/test loaders plus task metadata, or a declarative experiment
object.

**Status:** resolved — `train.py` defines `get_data()` returning four tensors:
`x_train, y_train, x_test, y_test`.

### 3. How are features mapped when `features != qubits`?

Options include padding, a learned classical projection, data re-uploading, or a
validation error. The choice affects fairness, parameter count, explainability,
and performance. The library must not silently truncate features.

**Status:** resolved — v0.1 requires the number of features to equal the number
of qubits and reports a friendly error otherwise.

### 4. Which encodings ship in v0.1?

Angle encoding is the simplest candidate. Amplitude encoding has normalization
and power-of-two size constraints and may be better deferred. The CLI must show
only fully supported options.

**Status:** resolved — angle encoding only.

### 5. Which measurements ship in v0.1?

Per-qubit Pauli-Z expectation is the simplest contract. Any additional choice must
still define one output value per qubit and document its range.

**Status:** resolved — Pauli-Z expectation for every qubit.

### 6. What qubit/shot limits keep the default experience fast?

The supported range and warning threshold should come from measured laptop
benchmarks. Analytic mode can be the default until those measurements exist.

**Status:** resolved — qubits 2–6; analytic mode by default; positive finite shots
are supported when explicitly selected.

### 7. What is the v0.1 dataset/task contract?

Binary classification on a small generated dataset is the recommended first
vertical slice. Confirm the metric, loss, label representation, and split policy.

**Status:** resolved — small binary classification with accuracy and
`BCEWithLogitsLoss`.

## Non-blocking later decisions

- Qiskit adapter scope and equivalence guarantees
- TensorFlow layer conventions
- hardware credentials, queueing, and cost limits
- expert mode for custom ansatz/backend selection
- regression, multiclass, and other task metrics
