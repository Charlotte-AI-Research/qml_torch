"""Human-readable rendering for a completed experiment."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from ..config import ExperimentConfig
    from ..validation import DataBundle

MODEL_STYLES = {"classical": "bright_cyan", "hybrid-vqc": "bright_magenta"}


def _paired_panels(left: Panel, right: Panel, console: Console) -> None:
    """Keep the dashboard compact on wide terminals and stack it on laptops."""

    if console.width < 110:
        console.print(left, right)
        return
    layout = Table.grid(expand=True, padding=(0, 1))
    layout.add_column(ratio=3)
    layout.add_column(ratio=2)
    layout.add_row(left, right)
    console.print(layout)


def print_experiment_setup(
    config: ExperimentConfig, data: DataBundle, console: Console, *, builtin: bool
) -> None:
    """Show the validated data and actual model architecture before training."""

    from .. import __version__

    brand = Text("Q M L   /   T O R C H\n", style="bold bright_cyan")
    brand.append("From features to qubits.\n", style="bold white")
    brand.append("PyTorch + PennyLane  /  local CPU simulator", style="dim")
    console.print(
        Panel(
            brand,
            title=Text("CHARLOTTE AI RESEARCH", style="dim"),
            subtitle=Text(f"v{__version__}  ·  educational alpha", style="dim"),
            border_style="bright_cyan",
            padding=(0, 2),
        )
    )

    details = Table.grid(padding=(0, 2))
    details.add_column(style="dim")
    details.add_column()
    details.add_row("Source", "Built-in synthetic demo" if builtin else "Your training script")
    details.add_row(
        "Data", f"{len(data.x_train)} train / {len(data.x_test)} test · {data.n_features} features"
    )
    quantum = config.mode != "classical"
    details.add_row(
        "Circuit",
        f"{config.n_qubits} qubits · {config.layers} layer(s)" if quantum else "Not used",
    )
    details.add_row(
        "Readout", "Angle encoding → Pauli-Z expectations" if quantum else "Linear classification"
    )
    measurements = f"{config.shots} shots" if config.shots else "Exact / analytic"
    details.add_row("Measurements", measurements if quantum else "Classical logits")
    details.add_row(
        "Training",
        f"Adam · lr {config.learning_rate:g} · {config.epochs} epochs · seed {config.seed}",
    )
    blueprint = Text()
    if config.mode in ("classical", "both"):
        blueprint.append("CLASSICAL\n", style="bold bright_cyan")
        blueprint.append(f"{data.n_features} features → Linear → logit\n", style="white")
    if config.mode in ("hybrid-vqc", "both"):
        blueprint.append("HYBRID VQC\n", style="bold bright_magenta")
        blueprint.append(f"{data.n_features} features → angle encoding\n")
        blueprint.append(f"→ RY / RZ / RY + CNOT ring × {config.layers}\n")
        blueprint.append(f"→ {config.n_qubits} measured values → Linear → logit\n")
    blueprint.append("Decision: logit ≥ 0 → class 1; otherwise 0", style="dim")
    _paired_panels(
        Panel(details, title="01 / DATA VALIDATED", border_style="bright_cyan"),
        Panel(blueprint, title="02 / MODEL ARCHITECTURE", border_style="bright_magenta"),
        console,
    )
    console.rule(Text("03 / TRAINING", style="bold bright_cyan"))


def _loss_trace(history: list[float], width: int) -> str:
    """Sample actual loss values into a compact trace with an explicit local scale."""

    if not history:
        return ""
    count = min(len(history), width)
    values = [history[round(i * (len(history) - 1) / max(1, count - 1))] for i in range(count)]
    low, high = min(history), max(history)
    if high == low:
        return "─" * count
    blocks = "▁▂▃▄▅▆▇█"
    return "".join(blocks[round((value - low) / (high - low) * 7)] for value in values)


def _learning_panel(report: dict[str, Any], console: Console) -> Panel:
    """Expose measured training histories even when the live bars finish quickly."""

    traces = Table.grid(padding=(0, 1))
    traces.add_column()
    traces.add_column()
    traces.add_column(justify="right")
    width = 18 if console.width >= 110 else max(4, min(28, console.width - 44))
    for name, result in report["models"].items():
        history = result["loss_history"]
        if history:
            style = MODEL_STYLES[name]
            traces.add_row(
                Text(name, style=style),
                Text(_loss_trace(history, width), style=style),
                f"{history[0]:.3f} → {history[-1]:.3f}",
            )
    return Panel(
        traces,
        title="TRAINING LOSS / BCE",
        subtitle=f"{report['epochs']} epochs · traces scaled separately",
        border_style="bright_cyan",
    )


def _confusion_panel(report: dict[str, Any]) -> Panel:
    """Keep prediction counts visible instead of presenting accuracy alone."""

    matrices = []
    for name, result in report["models"].items():
        matrix = Table(
            title=Text(name, style=MODEL_STYLES[name]),
            box=box.SIMPLE,
            padding=(0, 1),
            show_edge=False,
        )
        matrix.add_column("Actual", style="dim")
        matrix.add_column("0", justify="right")
        matrix.add_column("1", justify="right")
        for label, counts in enumerate(result["confusion_matrix"]):
            matrix.add_row(
                str(label),
                *[
                    Text(str(count), style="bright_green" if label == prediction else "white")
                    for prediction, count in enumerate(counts)
                ],
            )
        matrices.append(matrix)
    return Panel(
        Columns(matrices, padding=(0, 2)),
        title="TEST PREDICTIONS",
        subtitle="Columns: predicted class",
        border_style="bright_magenta",
    )


def format_summary(report: dict[str, Any]) -> str:
    """Return a concise terminal summary from a JSON-compatible report."""

    settings = report["settings"]
    lines = [
        "Experiment results",
        "------------------",
        f"Settings: {settings['n_qubits']} qubits, {settings['mode']} mode, "
        f"{settings['shots'] or 'analytic'} shots",
        f"Encoding: {settings['encoding']}",
        f"Measurement: {settings['measurement']}",
    ]
    for name, result in report["models"].items():
        lines.extend(
            [
                f"{name} accuracy: {result['test_accuracy']:.4f}",
                f"{name} runtime: {result['runtime_seconds']:.2f} seconds",
            ]
        )
    if report.get("circuit"):
        lines.extend(["", "Quantum circuit:", report["circuit"]])
    lines.extend(["", report["note"]])
    return "\n".join(lines)


def print_summary(report: dict[str, Any], console: Console) -> None:
    """Render real metrics, learning traces, predictions, and the trained circuit."""

    console.rule(Text("04 / EXPERIMENT RESULTS", style="bold bright_green"))
    table = Table(expand=True, border_style="bright_cyan", box=box.SIMPLE_HEAVY)
    for heading in ("Model", "Test accuracy", "F1", "Test loss", "Parameters", "Time"):
        table.add_column(heading, justify="left" if heading == "Model" else "right")
    for name, result in report["models"].items():
        table.add_row(
            Text(name, style=f"bold {MODEL_STYLES[name]}"),
            Text(f"{result['test_accuracy']:.1%}", style="bold bright_green"),
            f"{result['f1']:.3f}",
            f"{result['test_loss']:.3f}",
            str(result["parameter_count"]),
            f"{result['runtime_seconds']:.2f}s",
        )
    console.print(table)
    _paired_panels(_learning_panel(report, console), _confusion_panel(report), console)
    if report.get("circuit"):
        console.print(
            Panel(
                Text(report["circuit"], style="bright_white"),
                title="TRAINED QUANTUM CIRCUIT",
                subtitle="First training example · one Pauli-Z expectation per qubit",
                border_style="bright_magenta",
            )
        )
    data = report["data"]
    console.print(
        Text(
            f"RUN RECORD  ·  seed {report['seed']}  ·  "
            f"data SHA-256 {data['fingerprint_sha256'][:12]}…  ·  "
            f"{data['training_samples']} train / {data['test_samples']} test",
            style="dim",
        )
    )
    for warning in report.get("warnings", []):
        console.print(f"Note: {warning}")
    console.print(Text(report["note"], style="dim"))
