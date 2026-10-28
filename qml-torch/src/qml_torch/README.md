# `qml_torch` package area

> **What:** This directory will hold the public Python package imported with
> `import qml_torch`.
>
> **Why:** Keeping package code under `src/` avoids accidental imports from the
> repository root and gives the library one clear public entry point.

This is the Python import package. Public exports are kept small so users can
start with `ExperimentConfig` and `QuantumLayer` without learning internal
backend or circuit objects.

Public exports should remain small. Backend-specific objects and hidden circuit
presets should not become accidental public API.
