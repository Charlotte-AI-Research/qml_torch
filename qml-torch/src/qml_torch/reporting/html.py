"""Self-contained HTML experiment dashboard with SVG learning curves."""

from __future__ import annotations

import json
from html import escape
from typing import Any

COLORS = ("#67e8c2", "#9ca9ff")


def _loss_chart(models: dict[str, Any]) -> str:
    """Draw training loss without a charting dependency or network request."""

    histories = [(name, result.get("loss_history", [])) for name, result in models.items()]
    values = [value for _, history in histories for value in history]
    if not values:
        return "<p>No completed training history is available.</p>"
    low, high = min(0.0, min(values)), max(values) * 1.1
    high = max(high, low + 0.01)
    epochs = max(len(history) for _, history in histories)
    chart = []
    for fraction in (0.0, 0.5, 1.0):
        y = 215 - fraction * 180
        value = low + fraction * (high - low)
        chart.append(f'<path d="M50 {y}H690" stroke="#30394e"/>')
        chart.append(f'<text x="42" y="{y + 4}" text-anchor="end">{value:.2f}</text>')
    legend = []
    for index, (name, history) in enumerate(histories):
        if not history:
            continue
        points = " ".join(
            f"{50 + i / max(epochs - 1, 1) * 640:.2f},"
            f"{215 - (value - low) / (high - low) * 180:.2f}"
            for i, value in enumerate(history)
        )
        color = COLORS[index % len(COLORS)]
        chart.append(
            f'<polyline points="{points}" fill="none" stroke="{color}" '
            'stroke-width="3" stroke-linejoin="round"/>'
        )
        if len(history) == 1:
            chart.append(f'<circle cx="50" cy="{points.split(",")[1]}" r="4" fill="{color}"/>')
        legend.append(f'<span style="color:{color}">● {escape(name)}</span>')
    chart.append(
        f'<text x="50" y="242">Epoch 1</text><text x="690" y="242" '
        f'text-anchor="end">Epoch {epochs}</text>'
    )
    return (
        '<div class="legend">' + " ".join(legend) + "</div>"
        '<svg viewBox="0 0 720 260" role="img" aria-label="Training loss by epoch">'
        + "".join(chart)
        + "</svg>"
    )


def _matrix(name: str, result: dict[str, Any]) -> str:
    """Show all four classification counts with explicit label directions."""

    matrix = result.get("confusion_matrix", [[0, 0], [0, 0]])
    return f"""<article class="card"><h3>{escape(name)}</h3>
    <p class="muted">Rows: actual class · Columns: predicted class</p>
    <table><thead><tr><th>Actual / predicted</th><th>0</th><th>1</th></tr></thead>
    <tbody><tr><th>0</th><td>{matrix[0][0]}</td><td>{matrix[0][1]}</td></tr>
    <tr><th>1</th><td>{matrix[1][0]}</td><td>{matrix[1][1]}</td></tr></tbody></table>
    </article>"""


def render_html(report: dict[str, Any]) -> str:
    """Render an escaped report that works offline, on phones, and in print."""

    settings, models = report["settings"], report["models"]
    cards, rows = [], []
    for index, (name, result) in enumerate(models.items()):
        color = COLORS[index % len(COLORS)]
        cards.append(
            f'<article class="card metric" style="--accent:{color}">'
            f"<h2>{escape(name)}</h2><strong>{result['test_accuracy']:.1%}</strong>"
            f"<p>test accuracy · {result['runtime_seconds']:.2f}s</p></article>"
        )
        rows.append(
            f"<tr><th>{escape(name)}</th><td>{result['test_accuracy']:.1%}</td>"
            f"<td>{result['f1']:.3f}</td><td>{result['precision']:.3f}</td>"
            f"<td>{result['recall']:.3f}</td><td>{result['parameter_count']}</td></tr>"
        )
    warnings = "".join(f"<li>{escape(warning)}</li>" for warning in report.get("warnings", []))
    warning_box = f"<aside><h2>Run notes</h2><ul>{warnings}</ul></aside>" if warnings else ""
    error = report.get("error")
    if error:
        warning_box += f"<aside><h2>Run stopped</h2><p>{escape(str(error))}</p></aside>"
    circuit = escape(report.get("circuit") or "No quantum circuit in this run.")
    matrices = "".join(_matrix(name, result) for name, result in models.items())
    details = escape(
        json.dumps(
            {
                "settings": settings,
                "data": report.get("data"),
                "source": report.get("source"),
                "implementation": report.get("implementation"),
                "environment": report.get("environment"),
            },
            indent=2,
        )
    )
    status = escape(report.get("status", "completed"))
    shot_mode = "analytic" if settings["shots"] is None else f"{settings['shots']} shots"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>QML Torch · Experiment report</title>
<style>
:root{{color-scheme:dark;--bg:#0c1120;--panel:#141c2d;--text:#edf1fa;--muted:#aab8d0}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);
font:16px/1.6 system-ui,-apple-system,sans-serif}}
main{{max-width:1120px;margin:auto;padding:54px 24px}}
header{{border-bottom:1px solid #30394e;padding-bottom:32px;margin-bottom:32px}}
.brand{{font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:#67e8c2}}
h1{{font-size:clamp(32px,5vw,54px);line-height:1.15;letter-spacing:-.04em;margin:16px 0}}
h2{{font-size:19px;margin:0 0 12px}}h3{{font-size:17px;margin:0 0 6px}}
.muted,footer{{color:var(--muted)}}.chips,.legend{{display:flex;flex-wrap:wrap;gap:12px}}
.chips span{{border:1px solid #39465e;border-radius:999px;padding:4px 14px;font-size:13px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}}
.card{{background:var(--panel);border:1px solid #30394e;border-radius:18px;padding:24px;
min-width:0;margin-bottom:20px}}.metric{{border-top:3px solid var(--accent)}}
.metric strong{{font-size:52px;line-height:1.3;letter-spacing:-.04em;color:var(--accent)}}
.metric p{{margin:6px 0 0;color:var(--muted)}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th,td{{padding:10px 12px;text-align:left;border-bottom:1px solid #30394e}}th{{font-weight:500}}
svg{{width:100%;height:auto}}svg text{{fill:#aab8d0;font:12px system-ui}}
pre{{overflow:auto;font:13px/1.65 ui-monospace,SFMono-Regular,monospace;white-space:pre}}
.overflow{{overflow:auto}}aside{{border-left:3px solid #ffd38b;background:#231e22;padding:18px 24px;
border-radius:12px;margin-bottom:24px}}summary{{cursor:pointer;font-weight:600}}footer{{font-size:13px}}
@media print{{:root{{color-scheme:light;--bg:white;--panel:#f4f6fa;--text:#111;--muted:#444}}
.card{{break-inside:avoid}}.metric strong{{color:#183b58}}svg text{{fill:#444}}}}
</style></head><body><main>
<header><div class="brand">QML Torch · {escape(report.get("version", "alpha"))}</div>
<h1>From features to qubits.</h1>
<p class="muted">Your classical and quantum experiment, explained.</p>
<div class="chips"><span>{status}</span><span>{settings["n_qubits"]} qubits</span>
<span>{escape(shot_mode)}</span><span>{settings["epochs"]} epochs</span>
<span>seed {settings["seed"]}</span></div></header>
{warning_box}<section class="grid" aria-label="Model results">{"".join(cards)}</section>
<section class="card"><h2>The learning journey</h2>
<p class="muted">Training loss per epoch. Test data is evaluated after training.</p>
{_loss_chart(models)}</section>
<section class="card overflow"><h2>Beyond accuracy</h2><table>
<thead><tr><th>Model</th><th>Accuracy</th><th>F1</th><th>Precision</th><th>Recall</th>
<th>Parameters</th></tr></thead><tbody>{"".join(rows)}</tbody></table>
<p class="muted">The linear baseline and VQC have different capacities.
Parameter counts are shown; the models are not parameter-matched.</p></section>
<h2>Where predictions land</h2><section class="grid">{matrices}</section>
<section class="card"><h2>Inside your quantum layer</h2><pre>{circuit}</pre></section>
<section class="card"><details><summary>Reproduce this experiment</summary><pre>{details}</pre>
<p>Use the same script or built-in demo and pass the saved JSON to --config.
The dataset fingerprint identifies the exact tensors used.</p></details></section>
<footer>{escape(report["note"])} This report is self-contained and works offline.</footer>
</main></body></html>"""
