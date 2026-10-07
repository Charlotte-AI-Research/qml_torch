# Measurements

> **What:** This directory will define how each qubit is measured and converted
> into output values, beginning with Pauli-Z expectation values.
>
> **Why:** A separate measurement layer keeps the promised one-value-per-qubit
> output shape explicit and testable.

Future home of supported measurement builders and output metadata. Every v0.1
measurement must return one value per qubit and document its range and shot
behavior.
