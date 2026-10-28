"""Human-readable rendering for a completed experiment."""

from __future__ import annotations

from typing import Any


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
