"""Human-readable rendering for a completed experiment."""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


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
    """Display model results with aligned metrics and a readable gate diagram."""

    table = Table(title="Experiment results", expand=True, border_style="cyan")
    for heading in ("Model", "Test accuracy", "F1", "Parameters", "Time"):
        table.add_column(heading, justify="left" if heading == "Model" else "right")
    for name, result in report["models"].items():
        table.add_row(
            name,
            f"{result['test_accuracy']:.1%}",
            f"{result['f1']:.3f}",
            str(result["parameter_count"]),
            f"{result['runtime_seconds']:.2f}s",
        )
    console.print(table)
    if report.get("circuit"):
        console.print(Panel(report["circuit"], title="Your quantum circuit", border_style="blue"))
    for warning in report.get("warnings", []):
        console.print(f"Note: {warning}")
    console.print(report["note"])
