# Part 3 Circuit Depth Comparison

I ran the two-qubit quantum layer with one and two circuit layers. Both runs used the same two input samples, fixed targets, seed of 42, and one SGD step at a learning rate of 0.1. I verified that the first layer started with identical angles in both runs.

Output: 
```
Layers: 1
Weight shape: (1, 2, 3) | Parameters: 6
First-layer initial angles: [5.543461322784424, 5.749139785766602, 2.405604124069214, 6.027495384216309, 2.453258514404297, 3.7755370140075684]
Output shape: (2, 2)

Gradient norms by layer: [0.666378]
Weight update norm: 0.066638


Layers: 2
Weight shape: (2, 2, 3) | Parameters: 12
First-layer initial angles: [5.543461322784424, 5.749139785766602, 2.405604124069214, 6.027495384216309, 2.453258514404297, 3.7755370140075684]
Output shape: (2, 2)

Gradient norms by layer: [0.476763, 0.455921]
Weight update norm: 0.065967
```


Each circuit layer adds three rotation angles per qubit. Both circuits return one Pauli-Z expectation per qubit, which means the output shape will still be (2, 2). The nonzero gradient norms show that backpropagation reached the weights in every circuit layer. The nonzero update norms confirm that the optimizer changed the weights.

When it comes to adding more layers to the circuit, it can indeed increase accuracy, but that won't always be the case. adding complexity to the circuit will only have a positive effect if its actually learning with that increased complexity. It can increase the risk of overfitting and could start learning and seeing patterns from noise or just fit too closely to the training data. This experiment used a single optimization step and fixed regression targets to check gradient flow. Comparing classification accuracy would require training both models and evaluating them on the same held-out data.

## Reproduce the run

With the nested qml-torch package installed, run `python compare_circuit_depth.py`.