"""Compare two circuit depths with the same inputs and initial first-layer angles."""

import torch
from qml_torch.nn import QuantumLayer

inputs = torch.tensor([[0.3, -0.4], [-0.2, 0.5]])
targets = torch.tensor([[0.2, -0.3], [-0.1, 0.4]])
seed = 42

#test using 1 and 2 layers
for depth in (1, 2):
    
    torch.manual_seed(seed)
    
    #using the quantum layer
    model = QuantumLayer(qubits=2, layers=depth, seed=seed)
    weights = model.quantum_layer.weights
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

    initial_weights = weights.detach().clone()
    outputs = model(inputs)

    #backprop
    loss = torch.nn.functional.mse_loss(outputs, targets)
    loss.backward()
    gradient_norms = weights.grad.flatten(start_dim=1).norm(dim=1)
    optimizer.step()
    update_norm = (weights.detach() - initial_weights).norm()

    #outputting information
    print(f"Layers: {depth}")
    print(f"Weight shape: {tuple(weights.shape)} | Parameters: {weights.numel()}")
    print(f"First-layer initial angles: {initial_weights[0].flatten().tolist()}")
    print(f"Output shape: {tuple(outputs.shape)}")
    print(f"Gradient norms by layer: {[round(norm.item(), 6) for norm in gradient_norms]}")
    print(f"Weight update norm: {update_norm.item():.6f}")
