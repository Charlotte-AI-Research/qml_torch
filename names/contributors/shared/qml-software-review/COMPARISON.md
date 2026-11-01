# QML software comparison worksheet

> **What:** Om and Trinity's shared notes from trying other QML tools and QML Torch.
>
> **Why:** Turn observed user problems into useful improvements for our library.

**Status:** Om completed the direct PennyLane attempt.

**Contributors:** Om Patel and Trinity McKay.

## 1. What I tried

| Tool | Tried by | Version / Python | Example or tutorial link | Command used | Result: worked / blocked / not tried |
| --- | --- | --- | --- | --- | --- |
| PennyLane directly | Om Patel | Python 3.12.10, PennyLane 0.45.1, PyTorch 2.14.1+cpu | [PennyLane with PyTorch](https://docs.pennylane.ai/en/stable/introduction/interfaces/torch.html) | python pennylane_test.py | worked  |
| Qiskit Machine Learning | To record | To record | To record | To record | Not tried |
| QML Torch | To record | To record | To record | To record | Not tried |

For each attempt, add a short output snippet or exact setup error. Record changes
you made to the example so someone else can repeat it.

## 2. The beginner experience

| Question | PennyLane directly | Qiskit Machine Learning | QML Torch |
| --- | --- | --- | --- |
| Was installation clear? | Yes, the installation was clear. | Not assessed | Not assessed |
| What did I need for the first working run? | Python, pytorch, circuit, measurements, and gradient | Not assessed | Not assessed |
| How much code did I have to write or edit? | A code from the tutorial that tells different information. | Not assessed | Not assessed |
| What quantum knowledge or choices were required? | Knowing measurments, qubits.    | Not assessed | Not assessed |
| How did it connect to my ML workflow? | The pytorch tensors and gradients that are connected to the Qnode to a torch training workflow. | Not assessed | Not assessed |
| Were errors understandable and fixable? | Yes there some small errors but they were fixable. | Not assessed | Not assessed |
| What results, diagrams, and saved artifacts did I get? | I got the output and the gradients. | Not assessed | Not assessed |
| What feature or explanation did I wish QML Torch had? | To asses after trying the QML torch.  | Not assessed | Not assessed |

## 3. Suggested improvements for QML Torch

| Priority | User problem in our tool | Evidence / other tool's approach | Proposed small improvement | Impact | Effort |
| --- | --- | --- | --- | --- | --- |
| To rank | To investigate | To record | To propose | Low / medium / high | Small / medium / large |

**One thing QML Torch does well and should keep:** to assess.

**Most useful next change:** to recommend, with a short reason.

**Questions I could not verify yet:** to record.

## 4. What each person contributed

- **Om:** Ran the pennylane example, recorded the enviornment, the output and the gradient. 
- **Trinity:** to record after doing the work.
- **Reviewed together:** to record after discussing the recommendations.

This worksheet compares workflows. Accuracy or runtime numbers from different
examples are not controlled benchmarks.
