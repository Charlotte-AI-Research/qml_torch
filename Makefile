.PHONY: setup test lint type format run
setup:
python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e .[dev]


test:
pytest -q


lint:
ruff check .


type:
mypy src


format:
ruff check . --fix


run:
python examples/01_quantum_layer_torch.py