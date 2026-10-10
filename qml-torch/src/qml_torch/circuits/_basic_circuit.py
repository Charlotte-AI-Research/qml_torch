import numpy as np
import torch 
import pennylane as qml

from ..encodings import angle_encoding
from ..measurements import pauli_z_output


def basic_circuit(qubits: int,encoding_gate: str = "Y", layers: int = 1,):
    dev = qml.device("default.qubit", wires=qubits)

    @qml.qnode(dev, interface="torch", diff_method="backprop")
    def qnode(inputs, weights):
        angle_encoding(inputs, qubits, encoding_gate)

        #strongly entangling ansatz
        for layer in range(layers):
            for i in range(qubits):
                qml.RY(weights[layer, i, 0], wires=i)
                qml.RZ(weights[layer, i, 1], wires=i)
                qml.RY(weights[layer, i, 2], wires=i)
            if qubits > 1:
                for i in range(qubits):
                    qml.CNOT(wires=[i, (i + 1) % qubits])

        return pauli_z_output(qubits)

    weight_shapes = {"weights": (layers, qubits, 3)}

    return qml.qnn.TorchLayer(qnode, weight_shapes)