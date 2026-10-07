# Neural-network layers

> **What:** This directory will hold PyTorch modules such as `QuantumLayer` that
> can be inserted into a normal model.
>
> **Why:** It is the bridge that makes the quantum circuit feel like a familiar
> PyTorch layer and allows optimizers to train its parameters.

Future home of PyTorch modules, including `QuantumLayer`, input adaptation, weight
registration, and tensor shape behavior. It must not own datasets, prompts, or
general training loops.
