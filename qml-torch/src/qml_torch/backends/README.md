# Backends

> **What:** This directory will connect QML Torch to PennyLane's simulator.
>
> **Why:** Isolating backend code lets beginner-facing layers hide device details
> and makes a future Qiskit backend possible without rewriting the whole library.

Future home of the backend contract and PennyLane adapter. This area owns device
and QNode construction, capability metadata, shot behavior, and differentiation
integration. Qiskit is deferred until the contract is stable.
