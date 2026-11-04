# QML software comparison worksheet

> **What:** Om and Trinity's shared notes from trying other QML tools and QML Torch.
>
> **Why:** Turn observed user problems into useful improvements for our library.

**Status:** Om completed the direct PennyLane and root QML Torch quantum-layer
attempts.

**Contributors:** Om Patel and Trinity McKay.

## 1. What I tried

| Tool | Tried by | Version / Python | Example or tutorial link | Command used | Result: worked / blocked / not tried |
| --- | --- | --- | --- | --- | --- |
| PennyLane directly | Om Patel | Python 3.12.10, PennyLane 0.45.1, PyTorch 2.14.1+cpu | [PennyLane with PyTorch](https://docs.pennylane.ai/en/stable/introduction/interfaces/torch.html) | python pennylane_test.py | worked  |
| Qiskit Machine Learning | To record | To record | To record | To record | Not tried |
| QML Torch | Om Patel | Python 3.12.10, PyTorch 2.14.1+cpu, PennyLane 0.45.1 | [Quantum layer example](../../../../examples/01_quantum_layer_torch.py) | `$env:PYTHONPATH=(Resolve-Path .\src).Path; .\venv\Scripts\python.exe .\examples\01_quantum_layer_torch.py` | Worked |

For each attempt, add a short output snippet or exact setup error. Record changes
you made to the example so someone else can repeat it.

PennyLane Output:

Outputs: [0.8775825769558367, 0.6880373394540326]
Phi Gradient: [-0.8167369961738586, 0.6416231393814087]
Theta Gradient: 0.0
python .\examples\01_quantum_layer_torch.py

QML Torch output:

accuracy=0.984


## 2. The beginner experience

| Question | PennyLane directly | Qiskit Machine Learning | QML Torch |
| --- | --- | --- | --- |
| Was installation clear? | Yes, the installation was clear. | Not assessed | The root project instructions identify the editable install and dependencies; the example ran with the existing environment and `PYTHONPATH`. |
| What did I need for the first working run? | Python, pytorch, circuit, measurements, and gradient | Not assessed | PyTorch, PennyLane, the built-in dataset, `QuantumLayer`, and a linear readout. |
| How much code did I have to write or edit? | A code from the tutorial that tells different information. | Not assessed | No edits were needed; I just had to type the terminal scripts commands to run the qml torch. |
| What quantum knowledge or choices were required? | Knowing measurments, qubits. | Not assessed | The wrapper hides device and QNode construction; the example exposes qubit count and the layer/readout composition. |
| How did it connect to my ML workflow? | The pytorch tensors and gradients that are connected to the Qnode to a torch training workflow. | Not assessed | `QuantumLayer` is placed in `torch.nn.Sequential`, trained with Adam, and optimized through `BCEWithLogitsLoss`. |
| Were errors understandable and fixable? | Yes there some small errors but they were fixable. | Not assessed | The example ran without errors and the required `PYTHONPATH` was needed from the repository checkout. |
| What results, diagrams, and saved artifacts did I get? | I got the output and the gradients. | Not assessed | A terminal accuracy result is `0.984` |
| What feature or explanation did I wish QML Torch had? | The direct PennyLane concepts should be mapped to the wrapper's configuration. | Not assessed | A short explanation of the hidden circuit choices and a simpler install/run command for the root checkout would help beginners. |

## 3. Suggested improvements for QML Torch

| Priority | User problem in our tool | Evidence / other tool's approach | Proposed small improvement | Impact | Effort |
| --- | --- | --- | --- | --- | --- |
| 1 | A beginner running the root checkout needs to know why `PYTHONPATH=src` is required when the package is not installed. | The example ran with `PYTHONPATH` set, while the README's quick start expects an editable install first. | Add a Windows PowerShell command block that installs the root package and runs `examples/01_quantum_layer_torch.py`, plus a one-line explanation of the `src` layout. | Medium | Small |

**One thing QML Torch does well and should keep:** `QuantumLayer` fits directly
inside `torch.nn.Sequential`, so the example uses ordinary PyTorch loss,
optimizer, and backpropagation code around the quantum layer.

**Most useful next change:** Add a copy-pasteable Windows setup/run command for
the checked-in quantum-layer example, because the current source checkout needs
the package installed or `PYTHONPATH` configured before the example imports.

**Questions I could not verify yet:** to record.

## 4. What each person contributed

- **Om:** Ran the direct PennyLane example and the root QML Torch quantum-layer example; recorded the environments, quantum choices, commands, outputs, and training behavior.
- **Trinity:** to record after doing the work.
- **Reviewed together:** to record after discussing the recommendations.

This worksheet compares workflows. Accuracy or runtime numbers from different
examples are not controlled benchmarks.
