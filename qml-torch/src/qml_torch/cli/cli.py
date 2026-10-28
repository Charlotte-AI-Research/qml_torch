"""Guided experiments, a zero-setup demo, and diagnostics for beginners."""

from __future__ import annotations

import json
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as installed_version
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from rich.table import Table

from .. import __version__
from ..config import ExperimentConfig
from ..reporting import print_summary

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Train small quantum models with PyTorch. Start with: qml-torch demo",
)
console = Console(markup=False)


def _read_config(path: Path | None) -> ExperimentConfig:
    if path is None:
        return ExperimentConfig()
    values = json.loads(path.expanduser().read_text(encoding="utf-8"))
    if not isinstance(values, dict):
        raise ValueError("config must be a JSON object or a QML Torch result report")
    values = values.get("settings", values)
    if not isinstance(values, dict):
        raise ValueError("config settings must be a JSON object")
    return ExperimentConfig.from_dict(values)


def _execute(
    script: Path | None,
    config: ExperimentConfig,
    output: Path,
    *,
    html_report: bool = True,
    data: Any = None,
) -> None:
    from ..training import run_experiment
    from ..training.experiment import isolated_seed
    from ..validation import preflight

    with isolated_seed(config.seed):
        data = preflight(script, config, data=data)
    console.print(
        Panel(
            f"{config.n_qubits} qubits · {config.mode} · "
            f"{config.shots if config.shots is not None else 'analytic'} shots\n"
            f"{len(data.x_train)} training / {len(data.x_test)} test samples · "
            f"{config.epochs} epochs · seed {config.seed}",
            title=f"QML TORCH / {__version__}",
            border_style="cyan",
        )
    )
    if config.shots is not None:
        console.print("Sampled mode uses parameter-shift gradients; expect a slower run.")
    names = ("classical", "hybrid-vqc") if config.mode == "both" else (config.mode,)
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TextColumn("{task.completed:.0f}/{task.total:.0f} epochs"),
        TimeElapsedColumn(),
        console=console,
        disable=not console.is_terminal,
    ) as progress:
        tasks = {name: progress.add_task(name, total=config.epochs) for name in names}

        def on_epoch(name: str, epoch: int, loss: float) -> None:
            progress.update(tasks[name], completed=epoch, description=f"{name} · loss {loss:.4f}")

        report = run_experiment(
            script,
            config,
            output_path=output,
            data=data,
            html_report=html_report,
            on_epoch=on_epoch,
        )
    print_summary(report, console)
    console.print(f"JSON report: {output.expanduser().resolve()}")
    if html_report:
        console.print(f"HTML dashboard: {output.expanduser().resolve().with_suffix('.html')}")
        console.print("Open the HTML file in your browser to explore the result.")


def _error(exc: Exception, debug: bool) -> None:
    if debug:
        raise exc
    Console(stderr=True, markup=False).print(f"Error: {exc}\nUse --debug for the full traceback.")
    raise typer.Exit(code=1) from exc


@app.command("run")
def run(
    script: Path = typer.Argument(..., help="Trusted Python script defining get_data()."),
    qubits: int | None = typer.Option(
        None, "--qubits", "-q", help="2–6; defaults to feature count."
    ),
    mode: str | None = typer.Option(None, help="classical, hybrid-vqc, or both."),
    encoding: str | None = typer.Option(None, help="angle (v0.1 encoding)."),
    shots: int | None = typer.Option(None, help="0 for analytic, or a positive shot count."),
    measurement: str | None = typer.Option(None, help="pauli-z (one output per qubit)."),
    epochs: int | None = typer.Option(None, min=1, help="Training epochs (default: 10)."),
    seed: int | None = typer.Option(None, help="Random seed (default: 7)."),
    learning_rate: float | None = typer.Option(None, "--learning-rate", help="Adam learning rate."),
    config_file: Path | None = typer.Option(
        None,
        "--config",
        help="Saved result JSON or a JSON settings object; flags override it.",
    ),
    output: Path = typer.Option(Path("results.json"), help="JSON output; HTML is saved beside it."),
    no_prompt: bool = typer.Option(False, help="Run unattended using flags, config, and defaults."),
    no_html: bool = typer.Option(False, help="Save only JSON."),
    debug: bool = typer.Option(False, help="Show a full traceback for troubleshooting."),
) -> None:
    """Check your data, choose settings, and compare classical and quantum models."""

    try:
        from ..training.experiment import isolated_seed
        from ..validation import load_training_script

        base = _read_config(config_file)
        selected_seed = seed if seed is not None else base.seed
        # Check syntax/data once before prompting and restore all random streams.
        with isolated_seed(ExperimentConfig(seed=selected_seed).seed):
            data = load_training_script(script)
        console.print("✓ Training script and data check")
        unattended = no_prompt or config_file is not None
        values = base.to_dict()
        prompt_fields = [
            (
                "n_qubits",
                qubits,
                "Number of qubits (one per feature)",
                data.n_features if 2 <= data.n_features <= 6 else base.n_qubits,
                int,
            ),
            ("mode", mode, "Model mode: classical / hybrid-vqc / both", base.mode, str),
            ("encoding", encoding, "Encoding", base.encoding, str),
            ("measurement", measurement, "Measurement", base.measurement, str),
            ("shots", shots, "Shots (0 = exact analytic simulation)", base.shots or 0, int),
        ]
        for key, supplied, label, default, kind in prompt_fields:
            if supplied is not None:
                values[key] = supplied
            elif config_file is not None:
                continue
            elif unattended:
                values[key] = default
            else:
                values[key] = typer.prompt(label, default=default, type=kind)
        if values["shots"] == 0:
            values["shots"] = None
        for name, value in (("epochs", epochs), ("seed", seed), ("learning_rate", learning_rate)):
            if value is not None:
                values[name] = value
        config = ExperimentConfig.from_dict(values)
        _execute(script, config, output, html_report=not no_html, data=data)
    except Exception as exc:
        _error(exc, debug)


@app.command()
def demo(
    qubits: int | None = typer.Option(None, "--qubits", "-q", help="2–6; default 2."),
    epochs: int | None = typer.Option(None, min=1, help="Default: 60."),
    seed: int | None = typer.Option(None, help="Default: 7."),
    shots: int | None = typer.Option(None, min=0, help="0 for analytic simulation (default)."),
    config_file: Path | None = typer.Option(None, "--config", help="Replay a saved demo report."),
    output: Path = typer.Option(Path("qml-demo.json")),
    no_html: bool = typer.Option(False),
    debug: bool = typer.Option(False),
) -> None:
    """Run a built-in experiment immediately. No dataset download or script needed."""

    try:
        from ..training.demo import make_demo_data

        values = (
            _read_config(config_file) if config_file else ExperimentConfig(epochs=60)
        ).to_dict()
        for key, value in (
            ("n_qubits", qubits),
            ("epochs", epochs),
            ("seed", seed),
            ("shots", shots),
        ):
            if value is not None:
                values[key] = value
        if values["shots"] == 0:
            values["shots"] = None
        config = ExperimentConfig.from_dict(values)
        _execute(
            None,
            config,
            output,
            html_report=not no_html,
            data=make_demo_data(config.n_qubits, config.seed),
        )
    except Exception as exc:
        _error(exc, debug)


@app.command()
def doctor() -> None:
    """Check package versions and run a real quantum forward/backward smoke test."""

    import platform

    table = Table(title="QML Torch environment")
    table.add_column("Component")
    table.add_column("Version")
    table.add_row("Python", platform.python_version())
    table.add_row("qml-torch", __version__)
    missing = []
    for name in ("torch", "pennylane", "numpy", "typer", "rich"):
        try:
            table.add_row(name, installed_version(name))
        except PackageNotFoundError:
            missing.append(name)
            table.add_row(name, "missing")
    console.print(table)
    if missing:
        console.print("Install missing packages: python -m pip install " + " ".join(missing))
        raise typer.Exit(code=1)
    try:
        import torch

        from ..nn import QuantumLayer

        layer = QuantumLayer(2, seed=7)
        layer(torch.ones(2)).sum().backward()
        console.print("✓ CPU quantum forward pass and gradients work.")
    except Exception as exc:
        _error(exc, False)


@app.command("init")
def initialize(
    path: Path = typer.Argument(Path("train.py"), help="Where to create the starter script."),
) -> None:
    """Create a beginner training script; existing files are never overwritten."""

    template = '''"""Starter data for qml-torch run train.py."""
import torch


def get_data():
    """Return training features, training labels, test features, test labels."""
    generator = torch.Generator().manual_seed(7)
    x = torch.rand(64, 2, generator=generator) * 2.5
    y = (x.sum(dim=1) > 2.5).float()
    return x[:48], y[:48], x[48:], y[48:]
'''
    path = path.expanduser()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as stream:
            stream.write(template)
    except FileExistsError:
        console.print(f"{path} already exists. Choose a new filename.")
        raise typer.Exit(code=1) from None
    console.print(f"Created {path}. Next: qml-torch run {path}")


@app.command()
def version() -> None:
    """Print the installed QML Torch version."""

    typer.echo(f"qml-torch {__version__}")
