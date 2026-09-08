"""Build and evaluate the smallest QML Torch circuit."""

from qmltorch.circuits import angle_embedding_qnode


def main() -> None:
    circuit = angle_embedding_qnode(2)
    print(circuit([0.1, 0.2], [[0.0, 0.0]]))


if __name__ == "__main__":
    main()
