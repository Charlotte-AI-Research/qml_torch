import pytest

from qmltorch.nn import QuantumLayer


def test_layer_factory_is_available() -> None:
    try:
        layer = QuantumLayer(2)
    except ImportError:
        pytest.skip("Torch/PennyLane are not installed in this environment")
    assert layer is not None
