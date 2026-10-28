# Reporting

> **What:** This directory formats circuit diagrams, metrics, runtimes,
> settings, warnings, and saved result files.
>
> **Why:** Users need to see both their choices and the library's hidden defaults
> to understand and reproduce an experiment.

`summary.py` formats terminal tables and circuit diagrams. `html.py` builds an
offline dashboard with SVG loss curves, confusion matrices, and provenance.
`artifacts.py` saves JSON and HTML atomically per file. User-provided text is
escaped before entering HTML. Reports expose hidden defaults without requiring
beginners to configure them.
