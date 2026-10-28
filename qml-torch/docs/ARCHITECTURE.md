# Architecture

> **What:** How the shipped alpha's modules fit together.
>
> **Why:** Each module owns one part of the experiment so changes can be tested.

```text
CLI (run / demo / doctor / init)
              |
      config + validation
              |
       shared training loop
       /                  \
linear baseline       PyTorch QuantumLayer
                           |
              angle encoding + hidden circuit
                           |
              seeded PennyLane default.qubit
                           |
                 Pauli-Z expectations
       \                  /
        metrics + circuit + provenance
                     |
           JSON + offline HTML report
```

## Boundaries

- `config/`: frozen settings, strict counts, serialization, and typo detection.
- `validation/`: trusted-script loading, real CPU tensors, shape and label checks.
- `backends/`: simulator construction and explicit random seed.
- `encodings/`: one angle per feature/qubit.
- `circuits/`: the versioned RY/RZ/RY plus CNOT-ring preset and QNode wiring.
- `measurements/`: one Pauli-Z expectation value per qubit.
- `nn/`: trainable parameters, batching, input checks, and PyTorch gradients.
- `training/`: shared full-batch Adam loop, held-out metrics, and bundled demo.
- `reporting/`: terminal tables, escaped offline HTML, and atomic artifact writes.
- `cli/`: beginner commands and progress; no circuit mathematics.

## Contracts

Features: `[batch, features]`, with `features == qubits` for quantum execution.
The layer also accepts `[qubits]`. Outputs preserve batch shape and have one
value per qubit. Analytic mode uses backpropagation; finite shots use
parameter-shift and a sample loop to support gradients to upstream layers.

Data loading converts real dense tensors to CPU float32. It never automatically
scales or projects features. Labels are binary and evaluated before conversion
so malformed values cannot silently become valid ones.

## Reproducibility

Experiments temporarily seed and restore Python, NumPy, and CPU Torch random
streams. Each sampled device has its own seed. Reports identify exact tensors
with SHA-256 and record environment versions and hidden circuit choices.

Results are repeatable for the tested environment and operation sequence. A
saved configuration alone cannot reproduce changes in a user's external data.

## Reports

Existing alpha-1 result keys remain present. Schema 2 adds histories, metrics,
model sizes, provenance, warnings, and status. Writes use a temporary file plus
atomic replacement. HTML is escaped, has no external dependencies, and supports
narrow screens and printing.

The linear baseline and quantum model share the training protocol but have
different parameter counts; reports explicitly describe this limitation.
