"""Guided and non-interactive command-line interface."""

from __future__ import annotations

from pathlib import Path

import typer

from .. import __version__
from ..config import ExperimentConfig
from ..reporting import format_summary
from ..training import run_experiment
from ..validation import load_training_script, preflight

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _value_or_prompt(
    value: str | None,
    prompt: str,
    default: str,
    no_prompt: bool,
) -> str:
    if value is not None:
        return value
    if no_prompt:
        return default
    return typer.prompt(prompt, default=default)


def _int_or_prompt(
    value: int | None,
    prompt: str,
    default: int,
    no_prompt: bool,
) -> int:
    if value is not None:
        return value
    if no_prompt:
        return default
    return typer.prompt(prompt, type=int, default=default)


@app.command("run")
def run(
    script: Path = typer.Argument(..., help="Training script defining get_data()."),
    qubits: int | None = typer.Option(None, "--qubits", "-q", help="Number of qubits."),
    mode: str | None = typer.Option(
        None,
        "--mode",
        help="classical, hybrid-vqc, or both.",
    ),
    encoding: str | None = typer.Option(None, "--encoding", help="Feature encoding."),
    shots: int | None = typer.Option(
        None,
        "--shots",
        help="Positive shot count; omit or use 0 for analytic mode.",
    ),
    measurement: str | None = typer.Option(None, "--measurement", help="Measurement type."),
    epochs: int = typer.Option(10, "--epochs", min=1, help="Training epochs."),
    seed: int = typer.Option(7, "--seed", help="Random seed."),
    output: Path = typer.Option(Path("results.json"), "--output", help="JSON report path."),
    no_prompt: bool = typer.Option(
        False,
        "--no-prompt",
        help="Use defaults for omitted beginner choices.",
    ),
) -> None:
    """Run a small classical and/or hybrid QML experiment."""

    try:
        if not script.expanduser().is_file():
            raise FileNotFoundError(f"training script not found: {script}")
        data = load_training_script(script)
        typer.echo("✓ Training script and data check")
        chosen_qubits = _int_or_prompt(qubits, "Number of qubits", 2, no_prompt)
        chosen_mode = _value_or_prompt(mode, "Model mode", "both", no_prompt).lower()
        chosen_encoding = _value_or_prompt(encoding, "Encoding", "angle", no_prompt).lower()
        chosen_measurement = _value_or_prompt(
            measurement, "Measurement", "pauli-z", no_prompt
        ).lower()
        chosen_shots = shots
        if chosen_shots is None and not no_prompt:
            chosen_shots = typer.prompt(
                "Number of shots (0 for analytic mode)", type=int, default=0
            )
        if chosen_shots == 0:
            chosen_shots = None

        config = ExperimentConfig(
            n_qubits=chosen_qubits,
            mode=chosen_mode,
            encoding=chosen_encoding,
            shots=chosen_shots,
            measurement=chosen_measurement,
            epochs=epochs,
            seed=seed,
        )
        data = preflight(script, config, data=data)
        typer.echo(
            f"✓ Input shape: [{data.x_train.shape[0]}, {data.n_features}] (train samples, features)"
        )
        report = run_experiment(script, config, output_path=output, data=data)
    except (FileNotFoundError, ImportError, TypeError, ValueError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(format_summary(report))
    typer.echo(f"\nResults saved to {output.expanduser().resolve()}")


@app.command("version", hidden=True)
def version() -> None:
    """Print the package version without adding another public workflow."""

    typer.echo(f"qml-torch {__version__}")
