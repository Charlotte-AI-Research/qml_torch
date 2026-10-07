# Product specification

## Problem

PyTorch users who are new to quantum computing face several decisions before they
can test even a small hybrid model: device construction, circuit design, encoding,
measurement, QNode wiring, differentiation, and output shape handling. QML Torch
should make the first experiment possible without requiring those details up
front, while still reporting what the library chose.

## Target users

1. PyTorch users curious about quantum machine learning.
2. Beginners who do not yet know how to construct quantum circuits.
3. Students exploring the mathematical behavior of small hybrid models.
4. Researchers and builders who need quick, reproducible prototypes.

The primary v0.1 persona knows basic Python, tensors, models, losses, and training
loops. Quantum-computing knowledge is optional.

## Core user story

> As a PyTorch user, I want to run one guided command against a small supported
> training script, select only understandable quantum options, and compare a
> classical baseline with a hybrid model so that I can learn and prototype without
> writing a circuit or choosing a quantum backend.

## Functional requirements

- **FR-001:** provide an explicit CLI entry point that validates before training.
- **FR-002:** let users choose qubit count, encoding, circuit/model mode, shots,
  and measurement.
- **FR-003:** hide backend and ansatz selection in beginner mode.
- **FR-004:** use PennyLane and PyTorch for the first release.
- **FR-005:** accept classical features and return one value per qubit.
- **FR-006:** support batches with output shape `[batch, qubits]`.
- **FR-007:** show the constructed circuit or a faithful text representation.
- **FR-008:** train and report a classical baseline and hybrid/QML model using the
  same comparison protocol.
- **FR-009:** save all explicit and hidden settings needed to understand a run.
- **FR-010:** provide actionable errors before expensive training when possible.

## Experience requirements

- Use machine-learning language first and introduce quantum terms in context.
- Offer safe defaults, short help beside every prompt, and a way to go back.
- Allow flags/config files to reproduce the same run without interactive input.
- Never launch a CLI or mutate global state merely on import.
- Never silently discard features, alter labels, or change the requested metric.
- Clearly distinguish analytic simulation (`shots = None`) from sampled results.

## Comparison rules

The classical and hybrid runs must share the dataset split, preprocessing, random
seed policy, task metric, and training budget unless a report clearly explains a
difference. Results are observations for that experiment, not evidence of quantum
advantage. Accuracy is appropriate only for supported classification tasks; later
task types must choose suitable metrics.

## v0.1 boundaries

The first release targets a small CPU-simulated supervised classification example.
It does not promise compatibility with arbitrary PyTorch programs. Qiskit,
TensorFlow, hardware runs, large-scale datasets, custom ansatz design, and claims
of speedup are deferred.

## Product success checks

- A new user completes the tutorial without writing gate-level circuit code.
- An invalid shape or configuration fails before training with a recovery step.
- A saved result explains both user choices and hidden defaults.
- A repeated seeded run behaves within documented tolerances.
- Default workloads finish inside the runtime budget selected in QMLT-018.
