# `qml_torch` package area

> **What:** This directory will hold the public Python package imported with
> `import qml_torch`.
>
> **Why:** Keeping package code under `src/` avoids accidental imports from the
> repository root and gives the library one clear public entry point.

This will become the Python import package. It intentionally contains no
`__init__.py` or implementation yet, so the planning scaffold cannot be mistaken
for an installable library.

Public exports should remain small. Backend-specific objects and hidden circuit
presets should not become accidental public API.
