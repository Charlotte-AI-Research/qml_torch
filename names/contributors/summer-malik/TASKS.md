# Summer — learning and project tasks

> **What:** Three suggested next steps for experiment review and project handoff.
>
> **Why:** Build on the planning, documentation, and release work already recorded.

Start with task 1. Task 3 is optional. Estimates are flexible; bring questions to
the team rather than feeling that you must finish in one sitting.

## 1. Explain one experiment — 30–45 minutes

**Need:** the shared setup, a terminal, and a browser. No circuit math required yet.

- [ ] Run `qml-torch demo --output qml-torch/reports/summer-demo.json` from the repository root.
- [ ] Open the HTML report. Find the dataset size, seed, accuracy, F1, and parameter counts.
- [ ] Write five sentences in this folder explaining what was trained and measured.
- [ ] Explain why one good demo result does not prove that quantum models are better.

**Open:** [demo data](../../../qml-torch/src/qml_torch/training/demo.py) and
[comparison runner](../../../qml-torch/src/qml_torch/training/experiment.py).

**Finished when:** you can explain the result to someone with basic ML knowledge
and point out that the linear baseline and hybrid model have different capacities.

## 2. Check whether the result repeats — 45–90 minutes

**Need:** task 1 and a basic understanding of a random seed.

- [ ] Repeat the demo with seeds 7, 8, and 9, using the same epoch count.
- [ ] Give each run a different output filename under `qml-torch/reports/`.
- [ ] Record both models' accuracy, F1, and runtime in a small table in this folder.
- [ ] Note one result that stays consistent and one thing that varies.
- [ ] Explain that changing the demo seed changes the generated data as well as initialization.

**Example:** `qml-torch demo --seed 8 --epochs 20 --output qml-torch/reports/seed-8.json`.

**Finished when:** your notes report all three seeds, including weaker results,
and do not present this tiny experiment as a general benchmark.

## 3. Optional: make the next release easy to hand off — 1–2 hours

**Need:** a fresh virtual environment and the release guide below.

- [ ] Follow the source-install tutorial and record any confusing instruction.
- [ ] Verify that `doctor`, `demo`, and `init` work without finding a script manually.
- [ ] Improve one confusing sentence or installation step in a small documentation PR.
- [ ] Record which maintainer handles repository review and which handles PyPI publishing.

**Open:** [README](../../../qml-torch/readme.md) and
[release guide](../../../qml-torch/docs/RELEASING.md).

**Finished when:** another teammate can follow the revised instructions and knows
who reviews a release. Document roles and account ownership, never credentials.

## Learn just enough

- [PyTorch training basics](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- [Python packaging walkthrough](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
