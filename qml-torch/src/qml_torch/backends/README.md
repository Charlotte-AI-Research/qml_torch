# Backends

> **What:** This directory connects QML Torch to PennyLane's simulator.
>
> **Why:** Isolating backend code lets beginner-facing layers hide device details
> and makes a future Qiskit backend possible without rewriting the whole library.

The PennyLane adapter now owns device and QNode construction, shot behavior, and
differentiation integration. Qiskit is deferred until this contract is stable.
