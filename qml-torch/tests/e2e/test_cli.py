"""Smoke-test the non-interactive CLI path."""

from pathlib import Path

from typer.testing import CliRunner

from qml_torch.cli import app


def test_cli_runs_example(tmp_path: Path) -> None:
    example = Path(__file__).parents[2] / "examples" / "train.py"
    output = tmp_path / "result.json"
    result = CliRunner().invoke(
        app,
        [
            "run",
            str(example),
            "--no-prompt",
            "--epochs",
            "1",
            "--output",
            str(output),
        ],
    )
    assert result.exit_code == 0, result.stdout
    assert output.exists()
    assert "classical accuracy" in result.stdout
    assert "hybrid-vqc accuracy" in result.stdout
