"""Smoke-test the non-interactive CLI path."""

import json
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
    assert "classical" in result.stdout
    assert "hybrid-vqc" in result.stdout
    assert output.with_suffix(".html").exists()


def test_demo_works_without_a_script_and_can_replay(tmp_path: Path) -> None:
    runner = CliRunner()
    output = tmp_path / "demo.json"
    result = runner.invoke(app, ["demo", "--epochs", "1", "--output", str(output)])
    assert result.exit_code == 0, result.output
    saved = json.loads(output.read_text())
    replay = tmp_path / "replay.json"
    result = runner.invoke(app, ["demo", "--config", str(output), "--output", str(replay)])
    assert result.exit_code == 0, result.output
    repeated = json.loads(replay.read_text())
    assert saved["data"] == repeated["data"]
    assert (
        saved["models"]["hybrid-vqc"]["loss_history"]
        == repeated["models"]["hybrid-vqc"]["loss_history"]
    )


def test_init_preserves_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "train.py"
    runner = CliRunner()
    assert runner.invoke(app, ["init", str(path)]).exit_code == 0
    original = path.read_text()
    result = runner.invoke(app, ["init", str(path)])
    assert result.exit_code == 1
    assert "already exists" in result.output
    assert path.read_text() == original
    result = runner.invoke(
        app,
        [
            "run",
            str(path),
            "--no-prompt",
            "--epochs",
            "1",
            "--output",
            str(tmp_path / "generated.json"),
        ],
    )
    assert result.exit_code == 0, result.output


def test_invalid_config_fails_without_training(tmp_path: Path) -> None:
    config = tmp_path / "invalid.json"
    config.write_text('{"shotz": 50}')
    output = tmp_path / "result.json"
    result = CliRunner().invoke(app, ["demo", "--config", str(config), "--output", str(output)])
    assert result.exit_code == 1
    assert "unknown configuration" in result.output
    assert not output.exists()


def test_script_exception_is_readable(tmp_path: Path) -> None:
    path = tmp_path / "bad.py"
    path.write_text("raise RuntimeError('dataset cannot load')")
    result = CliRunner().invoke(app, ["run", str(path), "--no-prompt"])
    assert result.exit_code == 1
    assert "dataset cannot load" in result.output


def test_guided_run_accepts_defaults_and_json_only(tmp_path: Path) -> None:
    example = Path(__file__).parents[2] / "examples" / "train.py"
    output = tmp_path / "guided.json"
    result = CliRunner().invoke(
        app,
        ["run", str(example), "--epochs", "1", "--no-html", "--output", str(output)],
        input="\n" * 5,
    )
    assert result.exit_code == 0, result.output
    assert output.exists()
    assert not output.with_suffix(".html").exists()
