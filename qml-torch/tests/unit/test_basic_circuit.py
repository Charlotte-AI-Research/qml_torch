"""Tests for the basic quantum circuit's outputs."""

import torch

from qml_torch.circuits import basic_circuit


def test_basic_circuit_output_shape():
    qubits = 2
    batch_size = 3

    layer = basic_circuit(qubits=qubits)
    inputs = torch.rand(batch_size, qubits, dtype=torch.float64)

    outputs = layer(inputs)

    assert outputs.shape == (batch_size, qubits)


def test_basic_circuit_returns_finite_values():
    qubits = 2
    batch_size = 3

    layer = basic_circuit(qubits=qubits)
    inputs = torch.rand(batch_size, qubits, dtype=torch.float64)

    outputs = layer(inputs)

    assert torch.isfinite(outputs).all()


def test_basic_circuit_accepts_single_example_input():
    qubits = 2

    layer = basic_circuit(qubits=qubits)
    inputs = torch.rand(qubits, dtype=torch.float64)

    outputs = layer(inputs)

    assert outputs.shape == (qubits,)