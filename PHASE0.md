## Phase 0 — Onboarding & Teaching (Weeks 0–1 or 2)

**Goal:** Get everyone comfortable with the tools and workflows before development begins.

---

### Workshop
- Introduce the concept of a **qubit** (a quantum bit that can exist in a superposition of 0 and 1).
- Walk through simple quantum circuits in **PennyLane** and **Qiskit** (e.g., applying a Hadamard gate to create superposition).
- Explain how these circuits can be embedded into machine learning workflows.

---

### Setup
- Install required ML tools: **Python, PyTorch, scikit-learn**.
- Install quantum tools: **PennyLane, Qiskit**.
- Install development tools: **Docker** (for reproducibility across machines), **GitHub CLI** (for easier repo contribution).
- Configure **Continuous Integration (CI)** so all pushes to GitHub are automatically tested.

---
### Mini Exercise (Everyone)

**Task:** Run a **Quantum Kernel SVM** on the classic **moons dataset**.

---

#### Why this exercise?
- The **moons dataset** is a simple toy dataset shaped like two interlocking crescents.  
  - Classical linear models (like plain logistic regression) struggle with it.  
  - You need non-linear kernels (like RBF) to separate the classes.  
- A **quantum kernel** works like a *fancy similarity checker*.  
  - It maps the data into a high-dimensional quantum space before measuring similarity.  
  - This can sometimes reveal structure that classical kernels miss.  

By running this, you will:
1. Confirm your Python + quantum libraries are correctly installed.  
2. See how quantum feature maps connect directly to classical ML (SVM).  
3. Understand what QML Torch will automate and extend later.  

---

#### Step-by-step breakdown
1. **Generate the dataset**  
   - Use `sklearn.datasets.make_moons` to create two half-moon shapes.  
   - Add some noise to make it more realistic.  

2. **Define a quantum feature map**  
   - Each input point (x, y) is encoded into qubits.  
   - Use rotations (angle encoding) and entangling gates to spread data into quantum space.  

3. **Build the quantum kernel**  
   - The kernel computes similarity between two points by measuring how close their quantum states are.  
   - Formula: `K(x1, x2) = |⟨ψ(x1) | ψ(x2)⟩|^2` (the squared overlap between two quantum states).  

4. **Train an SVM with the quantum kernel**  
   - Instead of the usual RBF kernel, plug in the quantum kernel.  
   - Fit it to the moons dataset.  

5. **Check results**  
   - If everything works, you’ll see decision boundaries that can separate the moons.  
   - Compare with classical SVM → this shows the **value of hybrid approaches**.  

---

#### Example Code (simplified)
```python
import pennylane as qml
from pennylane import numpy as np
from sklearn.datasets import make_moons
from sklearn.svm import SVC

# 1. Dataset
X, y = make_moons(n_samples=50, noise=0.1)

# 2. Quantum device
dev = qml.device("default.qubit", wires=2)

# 3. Feature map
@qml.qnode(dev)
def feature_map(x):
    qml.AngleEmbedding(x, wires=[0, 1])
    qml.CZ(wires=[0, 1])  # add entanglement
    return qml.state()

# 4. Kernel function
def kernel(x1, x2):
    return np.abs(np.vdot(feature_map(x1), feature_map(x2)))**2

# 5. Kernel matrix
K = np.zeros((len(X), len(X)))
for i in range(len(X)):
    for j in range(len(X)):
        K[i, j] = kernel(X[i], X[j])

# 6. Train SVM
clf = SVC(kernel="precomputed")
clf.fit(K, y)

print("Training complete! Accuracy:", clf.score(K, y))


```bash
# Step 1. Install dependencies
pip install torch torchvision scikit-learn pennylane qiskit

# Step 2. Clone the repo
git clone https://github.com/simransummermalik/qml-torch.git
cd qml-torch
