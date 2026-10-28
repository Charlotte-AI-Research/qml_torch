# Encodings

> **What:** This directory contains ways to place classical feature values
> into a quantum circuit, beginning with angle encoding.
>
> **Why:** Encoding has its own rules and shape requirements, so it should be
> testable without mixing it into circuit presets or training code.

The implementation provides the named angle-encoding strategy and its circuit
operation. Additional encodings should provide their own constraints and tests
before they are added to the CLI.
