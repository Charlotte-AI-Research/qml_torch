# Jonathan — learning and project tasks

> **What:** Three suggested next steps for circuit behavior and reliable layer APIs.
>
> **Why:** Build on the original circuit and `BasicQuantumLayer` implementation.

Start with task 1. Task 3 is optional. Keep each code change small.

## 1. Draw the circuit you helped build — 30–45 minutes

**Need:** basic tensor shapes and a quick refresher on rotation gates and CNOT.

- [ ] Run `qml-torch demo --epochs 2` and inspect the gate diagram.
- [ ] Follow one sample from its two features through encoding, rotations, and measurement.
- [ ] Label which angles come from the data and which angles the optimizer trains.
- [ ] Explain why two qubits produce two numbers, rather than one class prediction.

**Open:** [circuit](../../../qml-torch/src/qml_torch/circuits/_basic_circuit.py),
[quantum layer](../../../qml-torch/src/qml_torch/nn/quantum_layer.py), and
[model readout](../../../qml-torch/src/qml_torch/training/models.py).

**Finished when:** a short sketch or note in this folder identifies the encoding,
trainable circuit, measurements, and final classical readout.

## 2. Improve direct circuit-factory errors — 1–2 hours

**Need:** task 1, Python argument validation, and basic pytest.

The PyTorch layer validates counts, but callers can also use `basic_circuit()`
directly. Review that path rather than adding the same check twice in the layer.

- [ ] Try direct factory calls with fractional qubits, fractional layers, and invalid shots.
- [ ] Add clear validation where it is missing before constructing a device/QNode.
- [ ] Reuse existing validation helpers where practical.
- [ ] Add focused tests for these direct calls in `tests/unit/test_basic_circuit.py`.
- [ ] Keep existing valid calls and output shapes working.

**Run from `qml-torch/`:** `pytest -q tests/unit/test_basic_circuit.py`.

**Finished when:** invalid factory arguments give a helpful error, covered by tests,
and the whole package suite still passes.

## 3. Optional: compare one versus two circuit layers — 1–2 hours

**Need:** an optimizer step and the meaning of a gradient.

- [ ] Make a tiny script using `QuantumLayer(qubits=2, layers=1)` and then `layers=2`.
- [ ] Keep inputs and the initialization seed fixed for the comparison.
- [ ] Record parameter counts, output shapes, and whether gradients reach the weights.
- [ ] Explain why adding circuit depth does not guarantee higher accuracy.

**Finished when:** your learning note shows the evidence, not just whether the code ran.
This is a local exercise; it does not need a new CLI option.

## Learn just enough

- [PennyLane circuit introduction](https://docs.pennylane.ai/en/stable/introduction/circuits.html)
- [PennyLane with PyTorch](https://docs.pennylane.ai/en/stable/introduction/interfaces/torch.html)
