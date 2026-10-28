# Timmy — learning and project tasks

> **What:** Three suggested next steps for tests that explain model behavior.
>
> **Why:** Extend the circuit/layer tests you contributed with meaningful new coverage.

Start with task 1. Task 3 is optional. Review existing tests before adding cases.

## 1. Explain what an optimizer test actually proves — 30–45 minutes

**Need:** `zero_grad()`, `backward()`, `step()`, and basic pytest assertions.

- [ ] Read your existing quantum-layer optimizer test.
- [ ] Run it alone and explain the purpose of each assertion.
- [ ] Write down how an output-shape check differs from a gradient check.
- [ ] Explain why one successful update does not prove that a model has learned well.

**Open:** [quantum-layer tests](../../../qml-torch/tests/integration/test_quantum_layer.py).

**Run from `qml-torch/`:**
`pytest -q tests/integration/test_quantum_layer.py -k optimizer_step`.

**Finished when:** a short note in this folder explains what the test catches and
what it cannot tell you about the circuit's mathematical correctness.

## 2. Check saving/loading and shape edge cases — 1–2 hours

**Need:** task 1, `state_dict()`, `load_state_dict()`, and `torch.allclose`.

- [ ] Add an analytic-mode save/load test for `QuantumLayer`.
- [ ] Run a fixed input through a layer, load its state into a fresh layer, and compare outputs.
- [ ] Test a single sample and a batch with one qubit; the layer API supports this even though the CLI starts at two.
- [ ] Keep the random seed fixed and use a clear numerical tolerance.
- [ ] Confirm the tests fail for a real mismatch rather than just checking object existence.

**Open:** [layer code](../../../qml-torch/src/qml_torch/nn/quantum_layer.py) and
[existing tests](../../../qml-torch/tests/integration/test_quantum_layer.py).

**Finished when:** one small test PR covers model state restoration and an output
shape not already covered. The current test suite still passes.

## 3. Optional: verify metrics using a tiny example — 1–2 hours

**Need:** the definitions of precision, recall, F1, and a confusion matrix.

- [ ] Choose four true labels and four predicted labels with both correct and incorrect answers.
- [ ] Calculate the confusion matrix, accuracy, precision, recall, and F1 by hand.
- [ ] Compare those answers with the metrics produced by the trainer using controlled model outputs.
- [ ] Include a case with no positive predictions to check zero-division handling.

**Open:** [training metrics](../../../qml-torch/src/qml_torch/training/experiment.py)
and [report tests](../../../qml-torch/tests/integration/test_reports.py).

**Finished when:** the expected answers are understandable without trusting the
implementation being tested. Keep these tests deterministic and small.

## Learn just enough

- [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [PyTorch optimizer walkthrough](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
