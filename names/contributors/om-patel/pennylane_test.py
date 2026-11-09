import pennylane as qml
import torch

dev = qml.device("default.qubit", wires=2)


@qml.qnode(dev, interface="torch")
def circuit(phi, theta):
    qml.RX(phi[0], wires=0)
    qml.RY(phi[1], wires=1)
    qml.CNOT(wires=[0, 1])
    qml.PhaseShift(theta, wires=0)

    return qml.expval(qml.PauliZ(0)), qml.expval(qml.Hadamard(1))


phi = torch.tensor([0.5, 0.1], requires_grad=True)
theta = torch.tensor(0.2, requires_grad=True)

outputs = circuit(phi, theta)
result = torch.stack(outputs)
result.sum().backward()

print("Outputs:", result.detach().tolist())
print("Phi Gradient:", phi.grad.detach().tolist())
print("Theta Gradient:", theta.grad.item())