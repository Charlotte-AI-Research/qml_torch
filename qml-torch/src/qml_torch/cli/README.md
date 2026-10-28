# CLI

> **What:** This directory implements commands such as
> `qml-torch run train.py` and display prompts and results.
>
> **Why:** A guided CLI is the main beginner experience and keeps setup choices
> out of the user's Python model code.

The implementation provides `qml-torch run train.py`, guided prompts, flags,
terminal rendering, and useful exit codes. It translates user answers into typed
configuration and delegates validation/training rather than implementing quantum
logic.
