"""Tests for the basic quantum circuit's outputs."""

import pytest
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


@pytest.mark.parametrize(
    ("argument", "value"),
    [
        ("qubits", 2.5),
        ("layers", 1.5),
        ("shots", 0),
        ("shots", -1),
        ("shots", 2.5),
        ("shots", True),
    ],
)
def test_basic_circuit_rejects_invalid_counts(argument, value):
    kwargs = {"qubits": 2, argument: value}

    with pytest.raises(ValueError, match=rf"^{argument} must be a positive integer$"):
        basic_circuit(**kwargs)


def test_basic_circuit_accepts_positive_shots():
    layer = basic_circuit(qubits=2, layers=2, shots=32, seed=0)
    inputs = torch.tensor([0.3, -0.4], dtype=torch.float64)

    assert layer(inputs).shape == (2,)
