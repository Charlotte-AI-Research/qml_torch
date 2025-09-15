# QML Torch

QML Torch is a hybrid quantum + classical machine learning toolkit.  
It is not just an idea or a research paper — it is a **software development project** with clear phases, code deliverables, benchmarks, documentation, and educational resources.  

The goal is to make hybrid quantum ML accessible, reproducible, and practical for teaching, research, and prototyping.

---

## Why This Is a Real Project (Not Just an Idea)

A real project has:
1. **Code deliverables** → QML Torch produces a Python library with PyTorch layers, sklearn kernels, and benchmark tools.  
2. **Infrastructure** → Docker containers, GitHub Actions CI pipeline, unit tests.  
3. **Benchmarks** → Case studies across cybersecurity, optimization, NLP, recommenders, and bioinformatics.  
4. **Documentation** → MkDocs site, API references, tutorials, Jupyter notebooks.  
5. **Applications** → A Streamlit demo app where users upload datasets and test hybrid vs classical models.  
6. **Outreach outputs** → Recorded demos and slides for AI Literacy Division.

Each phase produces concrete, checkable outputs. The scope is six months, with weekly deliverables that can be tracked on GitHub.

---

## What We Are Building

### 1. TorchQuantumLayer
- **Deliverable**: `torch.nn.Module` for PyTorch that runs quantum circuits.  
- **What it does**: Lets you add a quantum layer to a neural network as easily as `nn.Linear`.  

**Code tasks:**
- Implement encoders:
  - **Angle encoding** → maps features to qubit rotations (RY(x)).  
  - **Amplitude encoding** → normalizes dataset into qubit amplitudes.  
- Implement ansatz templates:
  - RY layers.  
  - RX–CNOT blocks.  
  - Hardware-efficient circuits.  
- Implement parameter binding so PyTorch optimizers can train gate parameters.  
- Unit tests for gradient flow and output dimensions.

---

### 2. QuantumKernel
- **Deliverable**: sklearn-compatible kernel for hybrid SVMs.  
- **What it does**: Uses quantum circuits to measure sample similarity.  

**Code tasks:**
- Implement sklearn-style API (`fit`, `transform`, `predict`).  
- Add caching for repeated kernel computations.  
- Add batching for large datasets.  
- Implement multiple feature maps (linear, polynomial, quantum).  
- Unit tests for kernel values on toy datasets.

---

### 3. Benchmarks + CLI
- **Deliverable**: Command-line tool (`qmltorch-bench`).  
- **What it does**: Runs classical vs hybrid experiments on datasets.  

**Code tasks:**
- CLI commands to train models.  
- Log metrics: accuracy, AUROC, runtime, convergence curves.  
- Export results as CSV/JSON.  
- Unit tests for CLI commands.

---

### 4. Applied Case Studies
- **Deliverable**: Case study scripts + benchmark results in `/case_studies/`.  
- **Datasets and tasks**:
  - **Cybersecurity**: intrusion detection dataset.  
  - **Optimization**: traveling salesman (small graphs).  
  - **NLP/Misinformation**: fake news classification.  
  - **Recommender Systems**: MovieLens dataset.  
  - **Bioinformatics**: codon/protein classification (optional).  

**Tasks:**
- Preprocess datasets.  
- Train classical baselines.  
- Train hybrid models.  
- Compare results.  
- Store results reproducibly in repo.

---

### 5. Educational + Outreach Resources
- **Deliverables**:  
  - Jupyter notebooks for each concept (Intro to Qubits → Applied Case Studies).  
  - MkDocs documentation site.  
  - Streamlit demo app for “classical vs hybrid” comparisons.  
  - Outreach slides + recorded demo runs.  

**Tasks:**
- Write API documentation.  
- Write tutorials with code examples.  
- Build Streamlit UI (frontend + backend).  
- Test notebooks in clean environments.

---

## Execution Plan (Step by Step)

### Phase 0: Onboarding & Teaching (Weeks 0–2)
**Goal:** Get every member set up and aligned.  
**Tasks:**
- Workshop: teach qubits, superposition, entanglement.  
- Install environment: Python, PyTorch, PennyLane, Qiskit, sklearn, Docker.  
- Configure GitHub repo + CI pipeline.  
- Mini exercise: quantum kernel SVM on moons dataset.  
**Output:** Everyone can run hybrid ML code, repo initialized.

---

### Phase 1: Core Toolkit (Weeks 1–6)
**Goal:** Build the foundation library.  
**Tasks:**
- Implement TorchQuantumLayer (encoders, ansatz).  
- Implement QuantumKernel (API, caching, batching).  
- Build CLI for benchmarks.  
- Add Docker + CI pipeline.  
**Output:** First working version of the library with unit tests.

---

### Phase 2: Applied Tracks (Weeks 7–16)
**Goal:** Apply QML Torch to real-world datasets.  
**Tasks:**
- Run cybersecurity, optimization, NLP, recommender, bioinformatics (optional).  
- Compare classical vs hybrid.  
- Collect benchmarks.  
**Output:** Case study scripts + benchmark results.

---

### Phase 3: Documentation & Outreach (Weeks 17–24)
**Goal:** Package and release QML Torch.  
**Tasks:**
- Build MkDocs site.  
- Publish notebooks.  
- Release Streamlit app.  
- Package to PyPI + Docker Hub.  
- Outreach demos and slides.  
**Output:** Complete release with library + docs + demo app.

---

## Scope of Work

**We will do:**
- Build a tested Python library.  
- Run applied case studies with honest benchmarks.  
- Provide reproducible Docker + CI setup.  
- Create notebooks, tutorials, documentation, and demo apps.  
- Publish results for teaching and outreach.  

**We will not do:**
- Train large-scale quantum models (hardware is too limited).  
- Simulate >30 qubits (RAM limits).  
- Promise that quantum always outperforms classical ML — benchmarking is the point.  
- Spend money on quantum hardware — all runs are on simulators or free cloud tiers.

---

## Frequently Asked Questions

**Q: Do I need a quantum computer?**  
A: No. Everything runs on simulators (PennyLane, Qiskit). Optional small demos can use IBM Quantum’s free tier.  

**Q: Will this use too much RAM?**  
A: No, because:  
- We stick to small datasets (hundreds of samples).  
- We use 2–8 qubits for most experiments.  
- Circuits are shallow (1–2 layers).  
- Kernel computations are batched and cached.  
This runs fine on laptops with 8–16 GB RAM.  

**Q: What if I want to scale bigger?**  
A: HPC nodes let you simulate ~25–30 qubits (needs 100s of GB RAM). But this is optional — the core project is scoped for laptops.  

**Q: Why does this count as a project?**  
A: Because it has:  
- Code deliverables (library, CLI).  
- Infrastructure (Docker, CI, tests).  
- Applied benchmarks.  
- Documentation + demo app.  
- A six-month roadmap with clear outputs.  

**Q: Isn’t this just research?**  
A: No. Research papers talk about hybrid quantum ML. QML Torch turns it into a **usable software resource** with code, benchmarks, and teaching tools.  

**Q: What’s the value for industry?**  
A: Benchmarks show where hybrid ML might add value (cybersecurity, optimization, NLP, recommender systems, bioinformatics). Industry cares about these signals to decide where to invest.  

**Q: What’s the value for students?**  
A: Lowers the barrier to entry — students can run hybrid ML on laptops without coding circuits from scratch or buying expensive hardware.  

**Q: What’s the value for educators?**  
A: Provides ready-to-use tutorials, notebooks, and demos for teaching hybrid ML.  

**Q: What do you mean by case studies?**

A: When we say case studies in this project, we don’t mean writing essays. We mean small applied experiments where we take QML Torch and test it on a real world dataset or domain.
for an example for cybersecurity we’d take a tiny intrusion dataset, train a normal model, then train the same model with our quantum kernel, and compare them. Each domain (cyber, NLP, bio, etc.) gets its own mini test like that. Such as intrusion detection (obviously doesnt need to be this)

**Q: What even is the difference between QML torch and pytorch?**
A: PyTorch is classical ML only. QML Torch is PyTorch with plug-and-play quantum layers and kernels, so you can test hybrid quantum-classical models without learning a new framework.

**Q: What is a quibit?**
A: A qubit is the quantum version of a bit. A normal bit is like a light switch...it’s either on (1) or off (0). A qubit, by contrast, can be in a blend of both at once, a property called superposition. This doesn’t mean it’s “half on and half off,” but that it carries probabilities of being measured as either. When you finally check the qubit, it snaps into one outcome (0 or 1). Qubits can also be entangled, where two qubits behave as a single system no matter the distance. These features give qubits far richer ways to encode and process information than ordinary bits, which is why they’re promising for fields like optimization, physics simulation, and machine learning.

**Q: What technical skills are needed for this project?**
A:This project mainly needs people who are comfortable writing a little Python and willing to learn. If you’ve used libraries like PyTorch or scikit-learn before, that’s a bonus, but not required we’ll walk through the basics together in Phase 0. People who like working with data (cleaning, plotting, visualizing results) or writing clear documentation will also be very valuable. For those curious about quantum, you don’t need to know physics we’ll cover what qubits and circuits are, and the code libraries (PennyLane, Qiskit) handle the math for us. Advanced members can focus on Docker, CI/CD, or model tuning, but beginners can absolutely contribute by running examples, building notebooks, or helping with case studies. The project is structured so no one has to do everything, and everyone can learn while contributing.

---

## Team Structure (8–10 Members)

- Project Lead → roadmap, reviews.  
- Circuit Team → encoders + ansatz implementations.  
- ML Integration Team → PyTorch/sklearn APIs.  
- Benchmark Team → CLI + experiments.  
- Applied Track Owners → cybersecurity, optimization, NLP, recommenders, bio.  
- Docs/Frontend Team → notebooks, Streamlit app, documentation.  
- Infra Team → CI/CD, Docker, packaging.  

---

## Why This Matters

- **Education** → prepares students for quantum ML with real code.  
- **Reproducibility** → shared toolkit instead of scattered one-offs.  
- **Industry relevance** → case studies show where hybrid ML may help.  
- **Future value** → prepares CAIR community for the quantum future.  

---
