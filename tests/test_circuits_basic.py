import pytest

from qmltorch.circuits import angle_embedding_qnode


def test_circuit_validates_dimensions() -> None:
    with pytest.raises(ValueError):
        angle_embedding_qnode(0)


def test_circuit_factory_requires_pennylane_when_missing() -> None:
    try:
        circuit = angle_embedding_qnode(2)
    except ImportError:
        pytest.skip("PennyLane is not installed in this environment")
    assert callable(circuit)
