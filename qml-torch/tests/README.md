# Test structure

> **What:** This directory groups all automated checks into unit, integration,
> and end-to-end tests.
>
> **Why:** The three levels help the team find whether a problem is in one small
> function, the PyTorch/PennyLane connection, or the complete user journey.

- `unit/`: configuration, validation, registries, shape rules, and error messages
- `integration/`: PennyLane/PyTorch execution, gradients, and training components
- `e2e/`: CLI preflight, guided-equivalent runs, reports, and failure behavior

No tests exist yet because implementation has not started.
