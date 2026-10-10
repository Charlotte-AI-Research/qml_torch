import numpy as np
import torch 
import pennylane as qml

def pauli_z_output(qubits: int):
    #left to do
    return [qml.expval(qml.PauliZ(i)) for i in range(qubits)]