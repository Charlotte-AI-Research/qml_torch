# Planned architecture

This document defines boundaries, not implementations. The folder intentionally
contains no Python modules yet.

## System flow

```text
CLI or explicit Python API
          |
          v
typed user configuration
          |
          v
preflight validator/compiler ---> actionable diagnostics
          |
          v
compiled experiment plan
     |                |
     v                v
classical model   PyTorch QuantumLayer
                       |
                 feature adapter
                       |
              encoding + hidden preset
                       |
             PennyLane backend adapter
                       |
                 measurement values
     |                |
     +------ trainer -+
              |
              v
     circuit + comparison report
```

## Stable contracts

### Quantum layer

- Primary input: floating tensor shaped `[batch, features]`.
- Convenience input: `[features]`, with explicitly documented output behavior.
- Primary output: floating tensor shaped `[batch, qubits]`.
- Each output column is the selected measurement for one qubit.
- Gradients must reach registered circuit parameters in supported analytic modes.
- Finite-shot gradients and randomness must be documented per supported method.

The feature-to-qubit adaptation rule is intentionally pending QMLT-001. Whatever
is chosen must never silently drop features and must appear in the run report.

### Compiled experiment plan

The compiler converts user choices and the user-script contract into an immutable,
serializable plan. It contains resolved defaults, hidden preset identity, tensor
contracts, backend capabilities, seed policy, and estimated workload. Training
consumes a plan rather than rebuilding quantum choices ad hoc.

### Backend adapter

Only `backends/` may construct PennyLane devices or handle backend-specific QNode
details. Circuits describe operations; the PyTorch layer consumes a compiled
callable. This boundary makes a later Qiskit adapter possible without promising it
for v0.1.

## Module responsibilities

| Area | Owns | Must not own |
| --- | --- | --- |
| `config` | typed choices, defaults, serialization | prompting or devices |
| `validation` | preflight checks and compiled plans | training loops |
| `cli` | commands, prompts, flags, presentation | quantum math |
| `encodings` | feature-to-operation strategies | data loading |
| `circuits` | hidden/versioned circuit presets | CLI concerns |
| `measurements` | measurement builders and output metadata | metrics |
| `backends` | PennyLane device/QNode integration | product defaults |
| `nn` | PyTorch modules and tensor contracts | datasets or CLI |
| `training` | fair training/comparison protocol | circuit construction |
| `reporting` | diagrams, metrics, configs, provenance | model optimization |

## Dependency direction

Higher-level orchestration may depend on lower-level quantum pieces, but the
quantum pieces must not import the CLI or trainers. A proposed direction is:

```text
cli -> validation -> config
cli -> training -> nn -> backends
                    |      |
                    v      v
              circuits/encodings/measurements
training -> reporting
```

Exact cycles and framework constraints must be checked when QMLT-002 adds import
tests.

## Safety and reproducibility

- Treat executed user training scripts as trusted code; say this clearly.
- Avoid executing the script during checks that can be static.
- Validate workload before starting a potentially slow simulation.
- Record versions, seed, shots, hidden preset, adapter policy, and resolved config.
- Write incomplete/failed status distinctly from successful result artifacts.

## Extension seams

Qiskit should be added through the backend contract, not conditionals scattered
through the code. TensorFlow requires a frontend/layer contract and should not
alter PyTorch semantics. Expert configuration should be an additive interface;
beginner defaults remain versioned and reproducible.
