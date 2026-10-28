"""Allow ``python -m qml_torch`` to invoke the CLI."""

from .cli import app

if __name__ == "__main__":
    app()
