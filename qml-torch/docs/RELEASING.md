# Release the alpha

> **What:** The exact build and upload steps for the inner `qml-torch` package.
>
> **Why:** The repository has an older root package; selecting the right directory
> and version avoids publishing the wrong files.

The prepared release is `0.1.0a2`. Uploading alpha 1 to TestPyPI does not publish
alpha 2, and TestPyPI and PyPI have separate accounts and tokens.

From the repository root, activate your environment and enter the package:

```bash
source .venv/bin/activate
cd qml-torch
python -m pip install -e ".[dev]"
ruff check src tests
pytest -q
python -m build
python -m twine check --strict dist/qml_torch-0.1.0a2-py3-none-any.whl dist/qml_torch-0.1.0a2.tar.gz
```

Upload exactly the alpha-2 files, even if `dist/` still contains older releases:

```bash
python -m twine upload --repository testpypi dist/qml_torch-0.1.0a2-py3-none-any.whl dist/qml_torch-0.1.0a2.tar.gz
```

For an install check, make a fresh environment. Install runtime dependencies from
PyPI, then install **only this package** from TestPyPI:

```bash
python -m pip install "torch>=2.2" "pennylane>=0.45,<0.46" "numpy>=1.24" "typer>=0.12" "rich>=13.7"
python -m pip install --no-deps --index-url https://test.pypi.org/simple/ qml-torch==0.1.0a2
qml-torch doctor
qml-torch demo
```

After verification, a maintainer can upload the same files using their real PyPI
token:

```bash
python -m twine upload dist/qml_torch-0.1.0a2-py3-none-any.whl dist/qml_torch-0.1.0a2.tar.gz
```

Users can then install with `python -m pip install qml-torch==0.1.0a2` or request
the latest prerelease using `python -m pip install --pre qml-torch`.

Create the GitHub tag/release `v0.1.0a2`, mark it as a pre-release, and use the
changelog entry for the notes. CI builds and checks the package but does not
upload it automatically.
