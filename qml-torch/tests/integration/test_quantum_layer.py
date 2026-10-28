"""Tests the quantum layer's functionality"""

import pytest
import torch

from qml_torch.nn.quantum_layer import BasicQuantumLayer


def test_rejects_zero_qubits():
    with pytest.raises(ValueError, match="qubits must be at least 1"):
        BasicQuantumLayer(qubits=0)


def test_rejects_zero_layers():
    with pytest.raises(ValueError, match="layers must be at least 1"):
        BasicQuantumLayer(qubits=2, layers=0)


@pytest.mark.parametrize("gate", ["A", "H", "INVALID"])
def test_rejects_invalid_encoding_gate(gate):
    with pytest.raises(ValueError, match="encoding_gate"):
        BasicQuantumLayer(qubits=2, encoding_gate=gate)


def test_accepts_lowercase_encoding_gate():
    layer = BasicQuantumLayer(qubits=2, encoding_gate="y")
    assert layer.qubits == 2


@pytest.mark.parametrize(
    "inputs",
    [
        torch.randn(3),  # Wrong number of features
        torch.randn(4, 3),  # Batch with wrong number of features
        torch.randn(2, 4, 2),  # Unsupported number of dimensions
    ],
)
def test_rejects_invalid_input_shape(inputs):
    layer = BasicQuantumLayer(qubits=2)

    with pytest.raises(ValueError, match="Expected"):
        layer(inputs)


def test_quantum_layer_output_shape():
    qubits = 2
    batch_size = 4
    layer = BasicQuantumLayer(qubits=qubits)

    inputs = torch.randn(batch_size, qubits)
    outputs = layer(inputs)

    assert outputs.shape == (batch_size, qubits)


def test_quantum_layer_optimizer_step():
    qubits = 2
    layer = BasicQuantumLayer(qubits=qubits)
    optimizer = torch.optim.SGD(layer.parameters(), lr=0.1)

    inputs = torch.randn(4, qubits)
    targets = torch.randn(4, qubits)

    optimizer.zero_grad()
    outputs = layer(inputs)
    loss = torch.nn.functional.mse_loss(outputs, targets)
    loss.backward()

    parameters = list(layer.parameters())
    assert parameters, "The quantum layer should have trainable parameters"
    assert any(
        parameter.grad is not None
        and torch.isfinite(parameter.grad).all()
        and parameter.grad.abs().sum().item() > 0
        for parameter in parameters
    ), "Expected a finite, nonzero gradient"

    before = [parameter.detach().clone() for parameter in parameters]

    optimizer.step()

    assert any(not torch.allclose(old, new.detach()) for old, new in zip(before, parameters)), (
        "Expected the optimizer to update at least one parameter"
    )


def test_sampled_batch_gradients_reach_upstream_layer():
    upstream = torch.nn.Linear(2, 2)
    quantum = BasicQuantumLayer(2, shots=100, seed=7)
    inputs = upstream(torch.tensor([[0.4, 0.7], [0.2, 0.5]]))
    outputs = quantum(inputs)
    assert outputs.shape == (2, 2)
    outputs.sum().backward()
    assert upstream.weight.grad is not None
    assert torch.isfinite(upstream.weight.grad).all()
    assert upstream.weight.grad.abs().sum() > 0
