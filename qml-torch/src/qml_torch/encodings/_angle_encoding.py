import numpy as np
import torch
import pennylane as qml

def angle_encoding(inputs: torch.Tensor,qubits: int,selected_gate: str = "Y",):
    #Left to do
    qml.AngleEmbedding(inputs, wires=range(qubits), rotation=selected_gate)