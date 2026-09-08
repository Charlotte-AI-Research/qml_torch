# Meeting 1 — Fall 2026

**Working session:** turn QML Torch into the first piece of a citable research artifact.

This meeting is designed to leave the room with a real pull request or a reproducible issue. Everyone will install the environment, run a control experiment, complete part of the quantum model, and record evidence that another researcher can inspect. Reading slides is not the deliverable.

## Before the meeting

Use Python 3.10–3.12. From this folder, create an environment and install the meeting dependencies:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python verify.py
```

The first verification run should report that the environment is ready. If installation fails, save the complete error in `submission.md` and bring it to the meeting.

## 90-minute plan for tomorrow

| Time | Work | Required output |
| --- | --- | --- |
| 0–10 min | Install, verify, and form pairs | Each pair has a working environment or a saved setup error. |
| 10–20 min | Run `python starter_experiment.py --baseline` | A control accuracy, runtime, and seed are recorded. |
| 20–35 min | Read the circuit and data path | Each pair writes down the input shape, output shape, and trainable parameter count. |
| 35–60 min | Implement the quantum layer TODO | A two-qubit hybrid model runs forward and backward. |
| 60–75 min | Measure three seeds and compare | Results include mean accuracy, spread, runtime, and one failure mode. |
| 75–87 min | Review another pair's work | One concrete code review comment and one suggested test. |
| 87–90 min | Submit the work log | `submission.md` is complete and the next issue is identified. |

## The actual work

Open `starter_experiment.py` and complete every `TODO`:

1. Implement `build_quantum_layer` with a PennyLane QNode and `qml.qnn.TorchLayer`.
2. Make the layer accept two features and return two expectation values.
3. Connect it to the provided PyTorch classifier and confirm gradients are nonzero.
4. Add a three-seed experiment to the command-line path.
5. Record the classical control and hybrid results in `submission.md`.

Do not change the dataset or metric after seeing the first result. If something is changed, document why and rerun both models.

## Definition of done

- `python verify.py` passes after the TODOs are complete.
- The hybrid model trains for at least 20 epochs without a NaN loss.
- The report contains the exact command, dependency versions, seed values, accuracy, runtime, and a one-sentence limitation.
- A reviewer can run the experiment from a clean environment.

The meeting project is deliberately small. It is the first layer of a research artifact: a versioned tool, an executable method, and evidence that can be archived and cited. It should not include independent research notes, unpublished claims, or a promise that the quantum model wins. Read `PRESENTATION.md` for the research-facing story and `RESEARCH_ARTIFACT_PLAN.md` for the release path.
