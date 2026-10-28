# Neural-network layers

> **What:** This directory holds PyTorch modules such as `QuantumLayer` that
> can be inserted into a normal model.
>
> **Why:** It is the bridge that makes the quantum circuit feel like a familiar
> PyTorch layer and allows optimizers to train its parameters.

The implementation provides `QuantumLayer`, input-shape validation, trainable
weight registration, and the `[batch, qubits]` output contract. It does not own
datasets, prompts, or general training loops.
