# Configuration

> **What:** This directory stores and validates settings such as qubits,
> encoding, shots, measurement, mode, and seed.
>
> **Why:** One configuration format lets the CLI, Python API, tests, and saved
> reports describe the same experiment consistently.

The implementation provides typed user choices, safe defaults, serialization, and
validation. Beginner-facing config includes qubits, encoding, mode, shots, and
measurement; backend and ansatz remain internal for v0.1.
