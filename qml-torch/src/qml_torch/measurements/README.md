# Measurements

> **What:** This directory defines how each qubit is measured and converted
> into output values, beginning with Pauli-Z expectation values.
>
> **Why:** A separate measurement layer keeps the promised one-value-per-qubit
> output shape explicit and testable.

The implementation provides Pauli-Z expectation measurements. It returns one
value per qubit and supports analytic and finite-shot behavior through the hidden
PennyLane device.
