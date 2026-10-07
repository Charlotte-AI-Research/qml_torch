# Contributing to the planned project

Implementation has not started in this nested scaffold. Begin with the earliest
unblocked item in `TASKS.md` and keep each change small enough to review.

Before opening implementation work:

1. Link the change to a `QMLT-###` task.
2. Confirm any related blocking decision is resolved.
3. Add or update tests for observable behavior.
4. Update the relevant product/API documentation.
5. Avoid adding Qiskit, TensorFlow, hardware, or expert controls to v0.1 work.

A future pull request should pass the formatter, linter, type checker, and tests
defined by QMLT-002. Quantum-result claims must include the comparison protocol,
multiple seeds where appropriate, runtime, and limitations.
