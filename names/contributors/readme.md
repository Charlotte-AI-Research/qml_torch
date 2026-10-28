# Contributor folders and next steps

> **What:** Each contributor has a profile and a small personal or shared task list.
>
> **Why:** Turn earlier contributions into manageable learning and project work.

These are suggested next assignments based on Git history and the project log.
They do not assert that someone struggled with a topic. Om and Trinity share
the hands-on software comparison and product feedback track. The alpha already
runs; these tasks extend understanding and
coverage rather than restart the completed five-task build plan.

| Contributor | Focus | Start here |
| --- | --- | --- |
| Summer Malik | Experiment review, onboarding, release handoff | [Tasks](summer-malik/TASKS.md) · [Profile](summer-malik/README.md) |
| Jonathan De La Paz Posadas | Circuit behavior and layer contracts | [Tasks](jonathan-de-la-paz-posadas/TASKS.md) · [Profile](jonathan-de-la-paz-posadas/README.md) |
| Om Patel | QML software comparison and gap review with Trinity | [Shared tasks](shared/qml-software-review/TASKS.md) · [Profile](om-patel/README.md) |
| Timothy / Timmy Lin | Gradient tests, save/load, metric correctness | [Tasks](timmy-lin/TASKS.md) · [Profile](timmy-lin/README.md) |
| Trinity McKay | QML software comparison and gap review with Om | [Shared tasks](shared/qml-software-review/TASKS.md) · [Profile](trinity-mckay/README.md) |

## How to use these lists

1. Start with task 1. Use the time estimates as a guide, not a deadline.
2. Do task 2 as one small pull request after the learning exercise.
3. Complete task 3 unless it is marked optional. Om and Trinity's shared gap review is a core
   deliverable; the other tracks have an optional stretch. Ask a teammate to review.

Each task says what to learn, which files to open, what to produce, and how to
recognize completion. Mark a checkbox only after you can show the result.

Om and Trinity use [one shared worksheet](shared/qml-software-review/COMPARISON.md)
and submit one joint comparison. Suggested split: Om starts with PennyLane,
Trinity starts with Qiskit Machine Learning, and both review the gaps together.

## Shared setup

From the repository root, use Python 3.11 or newer and an activated environment:

```bash
python -m pip install -e "./qml-torch[dev]"
qml-torch doctor
```

To run tests, enter the inner package directory:

```bash
cd qml-torch
pytest -q
```

The current package is `qml-torch/src/qml_torch/`. The root `src/qmltorch/` is
the older teaching package. Keep reusable code and tests in the current package;
keep short learning notes in your contributor folder. Put dated team progress
updates in `LOGS.md/`, following its template.

For a pull request, include what changed, what you learned, and the command you
used to check it. The [GitHub flow guide](https://docs.github.com/en/get-started/using-github/github-flow)
explains the branch and review workflow. Suggested reviewers are suggestions, not
confirmed assignments or deadlines.
