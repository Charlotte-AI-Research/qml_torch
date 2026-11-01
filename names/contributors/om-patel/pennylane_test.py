import pennylane as qml
import torch

dev = qml.device("default.qubit", wires=2)


@qml.qnode(dev, interface="torch", diff_method="parameter-shift")
def circuit(inputs, weights):
    qml.AngleEmbedding(inputs, wires=range(2))
    qml.RY(weights[0], wires=0)
    qml.CNOT(wires=[0, 1])

    return (
        qml.expval(qml.PauliZ(0)),
        qml.expval(qml.PauliZ(1)),
    )


weights = torch.tensor([0.2], requires_grad=True)
inputs = torch.tensor([0.1, 0.3])

outputs = circuit(inputs, weights)
result = torch.stack(outputs)

result.sum().backward()

print("PennyLane:", qml.__version__)
print("PyTorch:", torch.__version__)
print("Output:", result.detach().tolist())
print("Gradient:", weights.grad.detach().tolist())