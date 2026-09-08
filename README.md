# QML Torch

QML Torch is CAIR's shared student software project for connecting small quantum circuits to PyTorch models. The Fall 2026 team will make the interface easier to use, test it on laptop-sized examples, and document what works.

The club project has a deliberately limited scope: a reusable quantum layer, examples, tests, and fair classical-versus-hybrid comparisons. It does not claim quantum advantage, reproduce a paper without a team proposal, or include any member's independent research.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
pytest -q
```

The first example is `examples/01_quantum_layer_torch.py`. A working PennyLane installation is required to run the quantum example; package metadata and documentation can still be inspected without it.

## Fall 2026 team deliverables

1. A stable `QuantumLayer` wrapper with input and output shape documentation.
2. One beginner tutorial and one reproducible comparison against a classical baseline.
3. Tests that run on every pull request.
4. A short end-of-semester demo and maintainer handoff notes.

Read [docs/MEETING_PLAN_FALL_2026.md](docs/MEETING_PLAN_FALL_2026.md) for tomorrow's interest meeting and [docs/TEAM_SCOPE.md](docs/TEAM_SCOPE.md) for ownership boundaries.
