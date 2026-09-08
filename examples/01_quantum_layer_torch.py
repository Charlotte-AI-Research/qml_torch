"""Train a tiny hybrid model on the built-in binary blobs."""

import torch

from qmltorch.datasets import make_binary_blobs
from qmltorch.nn import QuantumLayer


def main() -> None:
    torch.manual_seed(7)
    x, y = make_binary_blobs()
    features = torch.tensor(x, dtype=torch.float32)
    labels = torch.tensor(y, dtype=torch.float32)
    model = torch.nn.Sequential(QuantumLayer(n_qubits=2), torch.nn.Linear(2, 1))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    for _ in range(10):
        optimizer.zero_grad()
        loss = loss_fn(model(features).squeeze(-1), labels)
        loss.backward()
        optimizer.step()
    accuracy = ((model(features).squeeze(-1) > 0) == labels.bool()).float().mean()
    print(f"accuracy={accuracy.item():.3f}")


if __name__ == "__main__":
    main()
