"""Compatibility imports for experiment callers using the CLI package."""

from ..training.experiment import run_experiment, train_and_evaluate

__all__ = ["run_experiment", "train_and_evaluate"]
