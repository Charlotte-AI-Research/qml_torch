# Om + Trinity — try other QML tools and find our gaps

> **What:** Try other quantum ML software, compare it with QML Torch, and recommend
> improvements that would help our users.
>
> **Why:** Hands-on comparisons show what we make easier and where our library
> still needs work.

Your main job is exploration and feedback. Start small: two tools, one tiny
example in each, then a short list of useful improvements. All three tasks are
part of this track; trying a third tool is optional.

## Work together

This is one shared assignment with one comparison worksheet and one final
improvement list. Suggested split:

- **Om:** start with the direct PennyLane example and record its setup and quantum choices.
- **Trinity:** start with the Qiskit Machine Learning example and record its setup and user flow.
- **Both:** try QML Torch, walk each other through the examples, and agree on the
  most useful gaps to address. You can swap tools if that works better.

Submit one small documentation PR together and describe each person's contribution.

Use [COMPARISON.md](COMPARISON.md) to collect your findings. It starts blank
because no comparisons have been performed yet.

## 1. Pick two tools and understand their starting point — 30–45 minutes

**Need:** basic Python, a browser, and a little familiarity with training a model.

Start with these:

- **PennyLane directly:** follow its PyTorch interface example. PennyLane is also
  our backend, so compare the steps users do manually with the steps QML Torch hides.
- **Qiskit Machine Learning:** try a small classifier example from its official tutorial.

- [ ] Read the official getting-started/example material linked below.
- [ ] For each tool, note what it is for and which beginner example you will try.
- [ ] Write down what knowledge the example assumes: PyTorch, circuit gates, or something else.
- [ ] Record the tutorial links in your comparison notes.

**Finished when:** you have two specific examples to try and can explain what each
tool asks its user to understand. No long research paper is needed.

## 2. Actually try them — about 1–2 hours per tool

**Need:** task 1, separate virtual environments, and the tutorial's required Python
version. Follow each tool's own setup instructions.

- [ ] Install each tool in its own environment and record the package/Python versions.
- [ ] Run one small simulator example in each. No hardware account is needed for this assignment.
- [ ] Save the command, a short output snippet, and any changes needed to make it work.
- [ ] Note confusing instructions, missing explanations, useful defaults, and helpful errors.
- [ ] Run our `qml-torch demo` and `qml-torch init train.py` flow for comparison.

If setup blocks you for around 30 minutes, record the exact error and ask for help.
An installation problem is a valid observation; label that example as blocked,
rather than saying the tool does not support the feature.

**Finished when:** both tools have a documented attempt, ideally a runnable example,
and someone else could follow your notes. Distinguish what you ran from what you
only read about.

## 3. Find useful gaps in QML Torch — 45–60 minutes

**Need:** your hands-on notes and a look at our current tutorial and commands.

- [ ] Fill in the comparison table: installation, first run, required code, quantum choices,
      PyTorch integration, errors, and reports.
- [ ] Identify up to three evidenced gaps or confusing parts in our tool.
- [ ] Check our README/CLI first so an existing feature is not reported as missing.
- [ ] For each gap, describe the user problem, the other tool's approach, and one small next step.
- [ ] Rank the suggestions by user impact and effort. Include one thing we should keep.

A documentation improvement can be as valuable as a new feature. If a gap is only
suspected, mark it as a question to investigate. Do not invent findings to reach
three suggestions.

**Open:** [our README](../../../../qml-torch/readme.md),
[our tutorial](../../../../qml-torch/examples/README.md), and
[CLI guide](../../../../qml-torch/docs/CLI_SPEC.md).

**Finished when:** `COMPARISON.md` contains your observations and a short,
prioritized improvement list the team can turn into issues. You do not need to
implement the suggestions as part of this assignment.

## Official starting points

- [PennyLane with PyTorch](https://docs.pennylane.ai/en/stable/introduction/interfaces/torch.html)
- [Qiskit Machine Learning classifier tutorial](https://qiskit-community.github.io/qiskit-machine-learning/tutorials/02_neural_network_classifier_and_regressor.html)
- Optional third tool: [TorchQuantum](https://github.com/mit-han-lab/torchquantum)

Compare the beginner workflow first. If examples use different datasets, circuit
sizes, or training budgets, do not treat their accuracy or runtimes as a fair
performance benchmark.
