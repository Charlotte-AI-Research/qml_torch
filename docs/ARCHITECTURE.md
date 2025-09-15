# Architecture


- `circuits/`: pure circuit factories (no Torch). Accept simple typed configs, return QNodes.
- `nn/`: Torch modules wrapping QNodes; no data loading here.
- `trainers/`: small training loops; keep dependency light.
- `datasets/`: toy datasets for examples/tests only.
- `utils/`: seeds, logging, misc helpers.