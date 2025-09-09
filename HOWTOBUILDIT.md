# How We Are Going to Build It

QML Torch sounds complicated, but the process is broken into small steps.  
We are not inventing new physics or simulators. The heavy math and optimization is already handled by libraries like PennyLane, Qiskit, and PyTorch.  
Our job is to **connect these tools together** so quantum methods can be used just like normal ML layers and kernels.

---

## Step 1: Start Simple (Phase 0)

What we do:  
1. Install Python, PyTorch, scikit-learn, PennyLane, and Qiskit.  
2. Run a short workshop on what a qubit is, what superposition means, and how a tiny quantum circuit looks in code.  
3. Do a small coding exercise: train a quantum kernel SVM on the moons dataset.  

Why this matters:  
- Proves that everyone’s laptop can run hybrid ML with just a few lines of code.  
- Ensures everyone’s environment is set up correctly.  
- Builds shared understanding before coding the main library.  

What might feel tricky:  
- Quantum terms like “superposition” can sound abstract, but the code itself is short.  
- For example, the whole moons exercise is only ~20 lines of Python.  

Output: everyone can run a simple hybrid ML experiment.

---

## Step 2: Core Toolkit (Phase 1)

What we do:  
1. Build **TorchQuantumLayer**: a PyTorch class that wraps PennyLane/Qiskit circuits.  
   - Angle encoding: turns numbers into qubit rotations.  
   - Amplitude encoding: packs a vector into amplitudes of a quantum state.  
   - Ansatz templates: small reusable circuits like RY layers or RX + CNOT blocks.  
   - Fine-tuning: test shallow vs deep circuits and log accuracy vs runtime.  
2. Build **QuantumKernel**: an sklearn-compatible kernel for SVMs.  
   - Works with fit, transform, and predict just like classical kernels.  
   - Adds caching and batching so we don’t run out of RAM.  
3. Add **infrastructure**:  
   - Dockerfile for reproducible installs.  
   - GitHub Actions for automated testing.  
   - Unit tests for each new function.  

Why this matters:  
- TorchQuantumLayer lets you plug quantum circuits into neural nets.  
- QuantumKernel makes quantum similarity checks usable in sklearn pipelines.  
- Infrastructure makes the library professional and reliable.  

What might feel tricky:  
- Making sure PyTorch gradients flow correctly through PennyLane circuits.  
- Preventing kernel calculations from becoming too large.  

Output: a small but real Python library you can import and use.

---

## Step 3: Case Studies (Phase 2)

What we do:  
1. Split into sub-teams for applied tracks:  
   - Cybersecurity (intrusion detection).  
   - Optimization (traveling salesman on small graphs).  
   - NLP (fake news dataset).  
   - Recommender systems (MovieLens).  
   - Bioinformatics (optional).  
2. Train classical models (logistic regression, SVM, MLP) as baselines.  
3. Train hybrid models using QML Torch.  
4. Compare results: accuracy, AUROC, runtime, convergence.  

Why this matters:  
- Shows where quantum methods help and where they do not.  
- Provides real, reproducible benchmarks across fields.  

What might feel tricky:  
- Quantum kernels scale poorly if datasets are too large.  
- That’s why we stick to subsets and toy problems.  

Output: benchmark results and case study scripts in the repo.

---

## Step 4: Documentation and Outreach (Phase 3)

What we do:  
1. Write documentation with MkDocs: API references and tutorials.  
2. Polish Jupyter notebooks: from “Intro to Qubits” to “Case Studies.”  
3. Build a simple Streamlit demo app:  
   - Upload a dataset.  
   - Choose classical or hybrid model.  
   - View results and plots.  
4. Make outreach slides and short recorded demos for teaching.  
5. Release package to PyPI and Docker Hub.  

Why this matters:  
- Makes QML Torch easy to learn and use.  
- Creates a long-term resource for CAIR and future students.  

What might feel tricky:  
- Writing docs that are clear for beginners but still correct.  
- Ensuring notebooks run cleanly on fresh installs.  

Output: a polished toolkit with docs, tutorials, a demo app, and teaching resources.

---

## Why We Don’t Need C or C++

All the heavy lifting (quantum simulation, matrix math, gradient calculation) is already written in fast C++ and CUDA inside PennyLane, Qiskit, and PyTorch.  
When we use these libraries in Python, we are already calling optimized C++ code under the hood.  

Our project is about **integration and usability**: making those tools work together in a way that feels natural to ML developers. That’s why Python is enough.

---

## Keeping It Doable

1. Python only — no low-level coding required.  
2. Small scope — 2 to 8 qubits, toy datasets that fit in laptop RAM.  
3. Clear roles — each sub-team owns a small piece, no one does everything.  
4. Reusable tools — PennyLane and Qiskit handle the quantum logic.  
5. Step-by-step phases — each phase has outputs before moving to the next.  

---

## Why This Is Accessible

- You do not need to be a quantum expert. Phase 0 teaches the basics.  
- You do not need to master PyTorch or sklearn. Templates will be provided.  
- You do not need HPC or expensive hardware. Everything runs on laptops.  
- You do not need to do everything. Each team member contributes a piece.  

---

## Honest Challenges

- Quantum kernels grow quadratically with dataset size. We avoid this by keeping datasets small and using batching.  
- Debugging PyTorch + PennyLane integration may take time.  
- Quantum circuits train slower than classical layers.  
- Some case studies will show classical methods still perform better.  

But that is exactly the purpose:  
Not to prove quantum always wins, but to build a **toolkit, benchmarks, and learning resources** so others can explore hybrid ML with real code.
