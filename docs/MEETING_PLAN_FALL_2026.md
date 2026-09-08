# QML Torch interest meeting — Fall 2026

**Purpose:** explain the shared project, let students try a tiny example, and identify a realistic next step. This is an orientation, not a technical gate.

## 60-minute plan

| Time | Activity | Result |
| --- | --- | --- |
| 0–5 min | Welcome and introductions | Students know the meeting is open to learners and contributors. |
| 5–12 min | What QML Torch is | A quantum circuit is one component in an ordinary ML workflow. |
| 12–20 min | Why we benchmark | We compare the same task, data, metrics, and seeds; quantum is not assumed to win. |
| 20–35 min | Live demo | Run the starter layer or inspect the example; pair up if setup fails. |
| 35–43 min | Fall deliverables | Layer API, tutorial, tests, one controlled comparison, handoff. |
| 43–50 min | Roles and expectations | Members choose code, experiments, documentation, testing, or outreach. |
| 50–56 min | Application walkthrough | Explain the short application and the optional meeting path. |
| 56–60 min | Questions and next action | Collect interest, blockers, and preferred follow-up. |

## Opening script

“Welcome to CAIR QML. You do not need quantum-computing experience to participate. The shared project is QML Torch, a small Python package that makes it easier to put a quantum layer inside a PyTorch model. We will learn by building and testing one useful tool. We will keep classical baselines, report limits, and avoid promising results before we measure them.”

## Live demo fallback

If installation works, run `python examples/01_quantum_layer_torch.py`. If it does not, open the file and show the model boundary, then run `pytest -q` and discuss what a test protects. A setup failure is useful onboarding information, not a reason to exclude someone.

## Take-home action

Install the repository, read `docs/TEAM_SCOPE.md`, and open one small issue: a documentation gap, a test case, or a reproducible setup problem. Students who are not ready for an issue can continue attending general meetings.
