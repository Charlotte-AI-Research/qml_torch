# Training

> **What:** This directory trains the classical baseline and hybrid VQC model
> using the same small experiment setup.
>
> **Why:** Shared training rules make the comparison easier to run and reduce
> accidental differences in data, seeds, epochs, and metrics.

The implementation provides small supervised training and classical-versus-hybrid
comparison loops. Both models share data splits, seeds, metrics, and budgets.
