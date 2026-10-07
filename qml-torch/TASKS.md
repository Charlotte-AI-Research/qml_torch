# QML Torch implementation backlog

This backlog starts after the planning scaffold. Tasks are ordered so that a
small team can open them as GitHub issues and build vertical slices without first
creating the whole system.

Priority meanings:

- **P0:** required for the first usable path
- **P1:** required before a v0.1 release
- **P2:** useful follow-up after v0.1 is stable

## Milestone 0 — settle the contract

### QMLT-001 — resolve the open product decisions (P0)

**Depends on:** nothing

- Decide what the requested `Standard` mode means.
- Decide which encodings and measurements ship in v0.1.
- Choose the policy when feature count and qubit count differ.
- Define the minimum contract expected from a user's `train.py`.
- Record decisions in `docs/OPEN_QUESTIONS.md` and update the specs.

**Done when:** every v0.1 question in `OPEN_QUESTIONS.md` is marked resolved and
has one testable behavior.

### QMLT-002 — add package and developer metadata (P0)

**Depends on:** QMLT-001

- Add `pyproject.toml` with Python, PyTorch, and PennyLane version ranges.
- Register the future `qml-torch` console command.
- Configure Ruff, mypy, pytest, and a minimal CI job.
- Add installation and contribution instructions.

**Done when:** a clean environment can install an empty development package and
run the quality commands documented by the repository.

### QMLT-003 — define typed configuration models (P0)

**Depends on:** QMLT-001, QMLT-002

- Model qubits, encoding, circuit mode, shots, measurement, seed, and task type.
- Keep backend and ansatz out of the beginner-facing configuration.
- Support config construction from both CLI answers and Python.
- Make defaults serializable for reports and reproducibility.

**Done when:** valid choices round-trip to a saved config and invalid choices
produce a specific, beginner-readable error.

## Milestone 1 — compile a quantum layer

### QMLT-004 — build the preflight validator/compiler (P0)

**Depends on:** QMLT-003

- Validate environment versions and PennyLane availability.
- Inspect input/output shapes through an explicit user contract.
- Validate shots, qubits, encoding constraints, measurement, and task support.
- Return all actionable problems in one pass when possible.
- Produce a read-only compiled experiment plan before training.

**Done when:** preflight succeeds for the supported example and fails early for
each invalid configuration covered by unit tests.

### QMLT-005 — implement the PennyLane backend adapter (P0)

**Depends on:** QMLT-003

- Create the hidden default simulator device.
- Support analytic execution and finite shots.
- Isolate PennyLane-specific QNode and differentiation details.
- Expose backend capabilities to validation without exposing backend selection.

**Done when:** the adapter can execute a tiny differentiable circuit on CPU and
the rest of the package does not directly construct a PennyLane device.

### QMLT-006 — implement feature-to-qubit adaptation (P0)

**Depends on:** QMLT-001, QMLT-003

- Accept tensors shaped `[batch, features]` and a single-sample convenience form.
- Apply the resolved policy for fewer/more features than qubits.
- Never silently discard input features.
- Include the chosen adaptation in the experiment report.

**Done when:** equal, fewer, and greater feature-count cases have documented shape
behavior, gradients where applicable, and tests.

### QMLT-007 — add the v0.1 encoding registry (P0)

**Depends on:** QMLT-001, QMLT-005, QMLT-006

- Implement only the encodings approved for v0.1.
- Give each encoding a name, constraints, circuit builder, and help text.
- Keep encodings independent from measurements and training.

**Done when:** each advertised encoding compiles, differentiates where required,
and rejects unsupported input shapes with an actionable message.

### QMLT-008 — add versioned hidden circuit presets (P0)

**Depends on:** QMLT-001, QMLT-005, QMLT-007

- Implement the resolved `Standard`/VQC behavior.
- Hide ansatz selection behind stable, versioned presets.
- Define parameter shapes from qubit count and preset depth.
- Make the selected internal preset visible in reports for reproducibility.

**Done when:** users need no gate-level knowledge, but a run can still be exactly
identified and recreated.

### QMLT-009 — implement measurements and output contract (P0)

**Depends on:** QMLT-001, QMLT-005, QMLT-008

- Implement the v0.1 measurement choices.
- Return one scalar per qubit.
- Preserve batch dimension: `[batch, qubits]`.
- Document analytic versus finite-shot behavior and value ranges.

**Done when:** output shapes and gradients are tested across supported qubit
counts, measurements, and shot modes.

### QMLT-010 — build the PyTorch `QuantumLayer` (P0)

**Depends on:** QMLT-004 through QMLT-009

- Wrap the compiled QNode in `torch.nn.Module`.
- Register trainable parameters in `state_dict`.
- Preserve dtype/device behavior where supported.
- Give unsupported GPU or mixed-precision use a clear message.

**Done when:** a small PyTorch optimizer step changes quantum parameters and the
documented input/output contracts pass integration tests.

## Milestone 2 — guided training experience

### QMLT-011 — create the CLI preflight and prompt flow (P0)

**Depends on:** QMLT-003, QMLT-004

- Implement `qml-torch run train.py`.
- Run preflight before showing training prompts.
- Prompt for qubits, mode, encoding, shots, and measurement only.
- Support non-interactive flags for CI and reproducible reruns.
- Never prompt merely because `qml_torch` was imported.

**Done when:** an interactive beginner path and an equivalent non-interactive
command produce the same saved configuration.

### QMLT-012 — define the minimal user-script protocol (P0)

**Depends on:** QMLT-001, QMLT-004, QMLT-011

- Load only the explicitly documented callable/data contract from `train.py`.
- Avoid executing arbitrary code during static preflight where possible.
- Explain missing functions, tensors, loaders, or labels clearly.
- Document the security boundary: user scripts are trusted when executed.

**Done when:** the happy-path example loads successfully and each missing contract
element has a focused end-to-end failure test.

### QMLT-013 — add reusable training loops (P0)

**Depends on:** QMLT-010, QMLT-012

- Support one small supervised classification task first.
- Share split, seed, epoch budget, loss, and metric logic across models.
- Keep data loading out of the quantum modules.
- Capture loss history, runtime, and failures.

**Done when:** both comparison models can train through the same protocol with a
fixed seed and bounded laptop runtime.

### QMLT-014 — build a fair classical baseline (P0)

**Depends on:** QMLT-001, QMLT-013

- Define a small baseline with a documented parameter-matching policy.
- Use the same data split, preprocessing, seed policy, epochs, and metric.
- Label comparisons as experimental results, not quantum advantage.

**Done when:** one command trains classical and hybrid models under a recorded
comparison protocol.

### QMLT-015 — render circuits and result reports (P1)

**Depends on:** QMLT-008, QMLT-009, QMLT-013, QMLT-014

- Print a compact circuit summary and optionally save a diagram.
- Show classical and hybrid metrics, runtime, warnings, and failed-run context.
- Save machine-readable configuration and results.
- Record seed, dependency versions, hidden preset, and backend implementation.

**Done when:** a second user can identify and rerun an experiment from its output
folder without guessing hidden settings.

## Milestone 3 — make v0.1 dependable

### QMLT-016 — complete the test matrix (P1)

**Depends on:** all P0 implementation tasks

- Unit-test configuration, validation, shape rules, registries, and errors.
- Integration-test PennyLane/PyTorch gradients and optimizer behavior.
- End-to-end test CLI interactive-equivalent and non-interactive runs.
- Mark slow and finite-shot statistical tests explicitly.

**Done when:** CI covers the supported Python versions and the critical user path
has a deterministic smoke test.

### QMLT-017 — write beginner examples and tutorial (P1)

**Depends on:** QMLT-015

- Add a minimal generated/toy binary-classification example.
- Explain features, qubits, encoding, shots, and measurements in ML language.
- Show CLI and Python entry points.
- Add troubleshooting for installation, shapes, gradients, and runtime.

**Done when:** a user with PyTorch knowledge but no quantum background can finish
the tutorial without editing library internals.

### QMLT-018 — benchmark and set runtime guardrails (P1)

**Depends on:** QMLT-014, QMLT-015

- Benchmark supported qubit counts in analytic and sampled modes.
- Pick safe prompt defaults and warn before expensive configurations.
- Record accuracy distribution across multiple seeds, not only the best run.

**Done when:** v0.1 documents approximate laptop runtimes and enforces an agreed
maximum default workload.

### QMLT-019 — harden errors and cancellation (P1)

**Depends on:** QMLT-011 through QMLT-018

- Add beginner-readable messages with recovery suggestions.
- Handle Ctrl-C and partial report writing cleanly.
- Keep internal tracebacks available behind a debug flag.
- Prevent unsupported choices from reaching a long training run.

**Done when:** expected failures are tested and do not leave misleading success
artifacts.

### QMLT-020 — release v0.1 (P1)

**Depends on:** QMLT-016 through QMLT-019

- Freeze documented behavior and supported combinations.
- Run the clean-environment installation and tutorial checks.
- Publish limitations, changelog, and maintainer handoff notes.

**Done when:** the v0.1 user journey meets every success criterion in `readme.md`.

## Later work — explicitly not on the v0.1 critical path

- **QMLT-101 (P2):** Qiskit backend adapter after the backend contract is stable.
- **QMLT-102 (P2):** TensorFlow frontend after PyTorch behavior is stable.
- **QMLT-103 (P2):** additional tasks, datasets, encodings, and measurements.
- **QMLT-104 (P2):** optional expert mode for ansatz/backend selection.
- **QMLT-105 (P2):** hardware execution with credentials, queues, and cost guards.
