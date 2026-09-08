# QML Torch — from student code to a citable research instrument

**CAIR QML · Fall 2026 interest meeting**  
**Summer Malik · Founder and QML Division Lead**

This is a replacement narrative for the attached interest deck. The attached deck is useful as a structure, but its broad claims about paper reproducibility and its benchmark-first framing should not be presented as established facts without a source. This version makes a smaller, stronger claim: we will build an artifact that researchers can run, inspect, reuse, and cite.

## Slide 1 — The ambition

### We are not making another QML demo.

We are building the research instrument that makes a QML claim easier to test.

QML Torch should let a researcher move from:

`data → encoding → quantum layer → PyTorch model → saved evidence`

without rebuilding the integration layer for every experiment.

## Slide 2 — Why I started this division

I started CAIR QML because students are often asked to read advanced quantum ML papers before they have a reliable way to run, inspect, or extend the underlying method. I want the group to build the missing bridge: software that teaches the idea, exposes the assumptions, and survives after one semester.

My job as division lead is to set a serious scope, protect the boundary between team work and independent work, review the method, and make sure contributors receive clear credit. The team's work should be useful even when the result is negative.

## Slide 3 — Why this matters to research

Quantum ML papers often combine a circuit, a data encoding, an optimizer, a simulator or device, and a classical model. When those choices are buried in one-off code, a reader cannot easily reuse the method or determine which choice caused the result.

Our contribution is the connective tissue: a stable interface, explicit configuration, tests, and an artifact that preserves how the result was produced.

The research questions stay open. We do not begin with “quantum wins.” We begin with “what exactly ran, under which assumptions, and can another group run it?”

## Slide 4 — What QML Torch is

QML Torch is a PyTorch-facing layer for small quantum circuits. A researcher can place it inside a familiar model, train it with a familiar optimizer, and keep the circuit configuration visible.

The first public surface is intentionally narrow:

- `QuantumLayer`: a trainable PennyLane circuit exposed as a Torch module.
- Configured input and output shapes.
- Deterministic simulator examples.
- Tests for forward passes, gradients, and validation errors.
- A record of seeds, versions, commands, and results.

The current repository is a prototype. The team earns the right to make bigger claims by hardening this surface.

## Slide 5 — Why a paper would cite it

A paper cites a tool when the tool is useful and stable enough to be part of the method. Our release must make that citation meaningful:

1. A tagged version with a changelog.
2. A permanent archive and DOI when the release is ready.
3. A `CITATION.cff` file with contributor credit.
4. A clean-install command that actually runs.
5. A methods document describing the circuit, interface, device, and training choices.
6. Machine-readable results and a figure generated from the artifact.
7. Tests that protect the API future papers depend on.

We cannot promise that a paper will cite us. We can build something worth citing.

## Slide 6 — The intellectual center

The tool is not valuable because it hides quantum code. It is valuable because it makes the boundary explicit.

For every run, we want to answer:

- What classical data entered the circuit?
- What state preparation and trainable gates were used?
- What was measured and returned to PyTorch?
- Which parameters received gradients?
- What simulator or device executed the circuit?
- What information is preserved for a later reader?

That is research engineering, not a toy wrapper.

## Slide 7 — What we do tomorrow

Tomorrow is a build session, not a motivational talk.

Every pair will:

1. Install the environment and save the exact versions.
2. Run the control model once.
3. Implement the missing quantum layer in `starter_experiment.py`.
4. Prove that a forward pass and backward pass work.
5. Run three seeds and save the evidence.
6. Review another pair's implementation.

The control comparison is a validity check for the instrument. It is not the scientific headline and it is not a promise of quantum advantage.

## Slide 8 — What counts as a contribution

There are two legitimate paths.

### Build path

Own a small part of the tool: API validation, circuit configuration, gradient tests, result serialization, packaging, or documentation.

### Evidence path

Own the research artifact around the tool: a methods note, a clean-run script, a figure, an error analysis, or a review of what another researcher would need to reproduce the run.

Both paths can produce authorship or contributor credit when the work is substantial, documented, and reviewed. No one needs to pretend to be a quantum expert on day one.

## Slide 9 — The first artifact

Meeting 1 produces a small but real package of evidence:

```text
meeting_one_fall_2026/
├── starter_experiment.py   # executable method
├── requirements.txt        # environment contract
├── submission.md           # human-readable record
└── PRESENTATION.md         # research-facing motivation
```

The next iteration adds a machine-readable result file, a generated figure, a methods note, and a release tag. The destination is an archived, versioned artifact—not a screenshot of a notebook.

## Slide 10 — The standard we are adopting

We will distinguish three statements:

- **Implemented:** the repository contains the code and a test.
- **Observed:** a named run produced a recorded result.
- **Supported:** multiple clean runs and review justify the claim.

“Quantum advantage,” “hardware-ready,” and “research-grade” are supported claims only after evidence exists. Precision is what makes ambitious work credible.

## Slide 11 — Research lineage

The project sits on established ideas: quantum data encoding as a feature map, quantum kernels, and variational quantum classifiers. The team will cite the literature that motivates each design choice, then make our own implementation and limitations inspectable.

Suggested starting points:

- Schuld and Killoran, *Quantum Machine Learning in Feature Hilbert Spaces*, Phys. Rev. Lett. 122, 040504 (2019), DOI: <https://doi.org/10.1103/PhysRevLett.122.040504>
- Havlíček et al., *Supervised learning with quantum-enhanced feature spaces*, Nature 567, 209–212 (2019), DOI: <https://doi.org/10.1038/s41586-019-0980-2>
- PennyLane, `TorchLayer` API: <https://docs.pennylane.ai/en/stable/code/api/pennylane.qnn.TorchLayer.html>

These works motivate the tool. They do not validate results we have not run.

## Slide 12 — The invitation

If you want to learn, come to the meetings. If you want to build, take an issue. If you want your work to appear in a research artifact, make it reproducible enough that a future reader can find it, run it, and understand what you changed.

**Tomorrow: install, implement, measure, document.**
