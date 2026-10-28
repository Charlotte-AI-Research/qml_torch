"""Write complete run artifacts atomically, including a readable offline report."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .html import render_html


def _atomic_text(path: Path, content: str) -> None:
    """Avoid truncated artifacts if a process stops during a write."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def save_reports(report: dict[str, Any], path: Path, *, html_report: bool = True) -> None:
    """Save strict JSON and, optionally, a self-contained HTML sibling."""

    json_text = json.dumps(report, indent=2, allow_nan=False)
    html_text = render_html(report) if html_report else None
    _atomic_text(path, json_text)
    if html_text is not None:
        _atomic_text(path.with_suffix(".html"), html_text)
