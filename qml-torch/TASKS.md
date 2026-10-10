# QML Torch — first-version tasks

> **What:** This file splits the first working version into five approachable
> tasks, with requirements, checklists, and completion rules.
>
> **Why:** It gives the team a simple build order and prevents the first version
> from becoming too large or confusing.

For now, the project has only **five main tasks**. Complete them in order. Each
task can be assigned to one person or a small group, and each checklist item can
become a smaller GitHub issue later if needed.

The goal of version 0.1 is intentionally small:

> Run one tiny classification example, choose a few quantum settings, train a
> classical model and a hybrid VQC model, and display both results.

## What the team will probably need

You do **not** need a quantum computer or a GPU. A normal laptop is enough.

### Tools

- Python 3.11 is the recommended starting version.
- Git and GitHub for sharing work.
- A Python virtual environment (`venv`).
- A code editor such as VS Code.

### Likely Python packages

- `torch` — models and training
- `pennylane` — quantum circuits and simulator
- `numpy` — basic numerical work
- `typer` — simple command-line interface
- `pytest` — tests
- `ruff` — formatting and linting

Task 2 will put the final package list in `pyproject.toml`, so team members should
not install a large collection of packages yet.

### Helpful knowledge

- Basic Python functions, classes, and imports
- Basic PyTorch tensors, models, losses, and optimizers
- Basic Git branches and pull requests

Quantum experience is helpful for Task 3, but beginners can learn the small amount
needed from PennyLane's introductory circuit examples.

## Simple v0.1 defaults

These are the recommended choices for the first working version. Task 1 confirms
them before coding begins.

- One small binary-classification dataset
- PennyLane's local simulator
- PyTorch only
- Angle encoding only
- Pauli-Z expectation measurement only
- One output value per qubit
- Require `number of features == number of qubits` for now
- Hide the ansatz and backend from beginners
- Analytic mode as the default, with one finite-shot option
- Run both a classical baseline and a hybrid VQC model

More encodings, feature mapping, Qiskit, TensorFlow, hardware, and custom circuits
can come after version 0.1 works.

---

## QMLT-001 — agree on the first version

**Goal:** Make the project small and remove unclear words before anyone starts
coding.

**Good task for:** someone comfortable organizing ideas and explaining them
clearly. Deep quantum knowledge is not required.

### To do

- [ ] Confirm or edit the “Simple v0.1 defaults” above.
- [ ] Replace the unclear word `Standard` with clear model choices. Recommended:
      `classical`, `hybrid-vqc`, and `both`.
- [ ] Decide what the example `train.py` must provide. Keep it to one small,
      documented function that returns training and test data.
- [ ] Decide a safe qubit range for the first example, such as 2–6 qubits.
- [ ] Update `docs/OPEN_QUESTIONS.md` with the final answers.

### Finished when

The team can describe the first version in a few sentences, and all seven blocking
questions in `OPEN_QUESTIONS.md` have simple answers.

---

## QMLT-002 — set up the Python project

**Goal:** Make the empty project installable and give the rest of the team one
shared development setup.

**Needs:** Python packaging basics, Git, and a virtual environment. Complete
QMLT-001 first.

### To do

- [ ] Add `pyproject.toml` with only the packages needed for v0.1.
- [ ] Add the `qml_torch` package and a `qml-torch` command entry point.
- [ ] Add a small configuration object for qubits, encoding, mode, shots, and
      measurement.
- [ ] Add simple validation for missing packages and invalid settings.
- [ ] Configure `pytest` and `ruff`.
- [ ] Start every new Python file with a short module docstring explaining what
      the file owns and why it exists.
- [ ] Write setup commands that work in a clean virtual environment.

### Finished when

A teammate can clone the project, create a virtual environment, install it, run
`qml-torch --help`, and run an empty test suite without errors.

---

## QMLT-003 — build one working quantum layer

**Goal:** Create the smallest useful PyTorch quantum layer. Do not add multiple
backends, encodings, or circuit builders yet.

**Needs:** basic PyTorch `nn.Module` knowledge and PennyLane's beginner QNode
tutorial. Complete QMLT-002 first.

### To do

- [X] Create a hidden PennyLane `default.qubit` simulator.
- [X] Accept an input shaped `[batch, features]`.
- [X] For v0.1, give a friendly error unless `features == qubits`.
- [X] Encode features with angle encoding.
- [X] Add one small trainable VQC ansatz chosen by the library.
- [X] Measure Pauli-Z expectation on every qubit.
- [X] Return `[batch, qubits]`, meaning one value per qubit for every sample.
- [ ] Confirm a PyTorch optimizer can update the circuit parameters.

### Finished when

A tiny tensor can pass through `QuantumLayer`, produce the expected shape, and
complete one optimizer step without the user creating a PennyLane device or
writing a circuit.

---

## QMLT-004 — add the guided CLI and comparison

**Goal:** Give beginners the simple experience described in the project idea.

**Needs:** basic command-line programming and PyTorch training loops. Complete
QMLT-003 first.

### To do

- [ ] Implement `qml-torch run train.py`.
- [ ] Check the environment, training-script contract, and feature shape before
      training starts.
- [ ] Ask for qubits, model mode, shots, encoding, and measurement. In v0.1,
      encoding and measurement may each have only one supported choice.
- [ ] Build one small classical model and one small hybrid VQC model.
- [ ] Train both with the same data split, seed, epochs, and accuracy metric.
- [ ] Print the quantum circuit, both accuracies, both runtimes, and the settings.
- [ ] Save a small result file so the run can be repeated.
- [ ] Make sure importing `qml_torch` does not automatically open the CLI.

### Finished when

The example command runs from start to finish on a laptop and clearly shows the
classical and hybrid results. The output should describe an experiment, not claim
quantum advantage.

---

## QMLT-005 — test it and teach someone to use it

**Goal:** Make the first version understandable and dependable enough for another
beginner to try.

**Needs:** `pytest`, careful documentation, and the working flow from QMLT-004.
This person can start drafting the tutorial while earlier tasks are in progress.

### To do

- [ ] Test configuration errors and the `features == qubits` rule.
- [ ] Test the quantum layer's input/output shape and optimizer step.
- [ ] Add one end-to-end test for `qml-torch run train.py`.
- [ ] Write a short beginner tutorial using the included toy dataset.
- [ ] Explain qubits, encoding, shots, measurement, and VQC in ML-friendly words.
- [ ] Test the tutorial in a clean environment on a normal laptop.
- [ ] Record approximate runtime and set safe default qubit/epoch limits.
- [ ] Document known limitations and common setup errors.

### Finished when

A person who knows basic PyTorch but little quantum computing can follow the
tutorial, finish a run, understand the output, and recover from common mistakes.

## Not part of these five tasks

Wait until the first version works before adding:

- Qiskit or real quantum hardware
- TensorFlow
- amplitude encoding or many measurement types
- automatic feature compression or data re-uploading
- custom ansatz builders
- large datasets or claims of quantum speedup
