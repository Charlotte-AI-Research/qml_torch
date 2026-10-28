# CLI guide

> **What:** The supported commands and saved artifacts in alpha 2.
>
> **Why:** Contributors and users need an accurate description of the shipped CLI.

## Start here

```text
qml-torch demo
qml-torch doctor
qml-torch init train.py
qml-torch run train.py
```

`demo` has a bundled dataset. `doctor` checks versions and executes a quantum
forward/backward pass. `init` creates a small starter script using exclusive file
creation, so an existing file is preserved.

## Guided run

`run` executes the trusted script's `get_data()` once, checks the tensors, then
asks for qubits, mode, encoding, measurement, and shots. The qubit default follows
the feature count when it is in the supported 2–6 range.

Use `--no-prompt` for unattended runs. All choices have flags; `--epochs`,
`--seed`, and `--learning-rate` control training.

## Replay

```text
qml-torch run train.py --config results.json --output repeated.json
qml-torch demo --config qml-demo.json --output repeated-demo.json
```

A config can be either a saved report or a settings-only JSON object. Explicit
flags override its values. Passing a config disables prompts for `run`.

## Results

The default output is JSON plus an HTML sibling. `--no-html` saves JSON only.

The terminal includes progress on interactive terminals, test accuracy, F1,
parameter counts, runtimes, warnings, and the trained circuit. HTML adds learning
curves, confusion matrices, and reproducibility details.

Finite-shot runs use an explicit simulator seed. A dataset fingerprint helps
compare repeated runs. The baseline is linear and not parameter-matched to the VQC.

## Failure behavior

Validation errors stop before training. Training errors save a `failed` report;
Ctrl-C during training saves a `cancelled` report. The success path is marked
`completed`; interrupted processes may leave a report marked `running`.
Writes are atomic per artifact.

Normal error messages are concise. `--debug` exposes the traceback. Importing the
package does not start prompts.
