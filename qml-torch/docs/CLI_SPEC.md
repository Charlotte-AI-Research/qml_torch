# CLI experience specification

> **What:** This file defines what the `qml-torch` command asks,
> validate, display, save, and return.
>
> **Why:** It keeps the command-line experience predictable and beginner-friendly
> even when different teammates build its individual parts.

## Main command

```text
qml-torch run train.py
```

This command is the beginner path. It first checks the environment and the
documented user-script contract. If preflight passes, it opens a guided prompt.
Importing `qml_torch` alone never opens this interface.

## Prompt order

1. **Qubits** — positive integer inside the supported v0.1 range.
2. **Mode/circuit type** — choose `classical`, `hybrid-vqc`, or `both`.
3. **Encoding** — only implemented, compatible choices are shown.
4. **Measurement** — only measurements that preserve the one-value-per-qubit
   contract are shown.
5. **Shots** — analytic mode or a supported positive integer.

Backend, ansatz, differentiation method, and internal weight shapes are not
beginner prompts. They remain visible later in the saved report.

## Example session

```text
$ qml-torch run train.py
✓ Python and dependency check
✓ Training-script contract
✓ Input shape: [120, 4]

Qubits [4]: 4
Mode [both]: both
Encoding [angle]: angle
Measurement [z-expectation]: z-expectation
Shots [analytic]: 100

✓ Input shape and configuration check
Plan: classical baseline + 4-qubit hybrid model
Estimated workload: small CPU simulation
```

## Non-interactive equivalent

Every prompt must have a flag or a config-file field so CI and research reruns do
not depend on terminal input. The precise flags are defined in QMLT-004 after
QMLT-001 resolves the option names.

## Required output

On success, the terminal and saved artifacts should include:

- a circuit text diagram or saved diagram path;
- classical and hybrid task metrics;
- training time for each model;
- warnings and limitations relevant to the configuration;
- explicit user choices and resolved hidden defaults;
- random seed and dependency versions;
- a command/config that can rerun the experiment.

On failure, output should state which phase failed, how to recover, and where any
debug details were saved. A partial run must not look successful.

## Exit behavior

- Validation errors return a nonzero status before training.
- Ctrl-C ends cleanly and labels any partial artifact as incomplete.
- A `--debug` mode may expose internal tracebacks; normal mode favors concise,
  beginner-readable diagnostics.
