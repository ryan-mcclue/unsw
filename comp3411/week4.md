<!-- SPDX-License-Identifier: zlib-acknowledgement -->
neuron:
dendrite (input) reaches threshold --> axon (output) --> synapse (on/off) --> dendrite ...
100billion neurons with 10000 synapses each. Delay is 5milliseconds. So favour parallelism

node:
input edges -> non-linear activation/transfer function (takes weighted sum of edges; g(s)) -> output

perceptron can only compute linearly separable functions, i.e. points separated by line, i.e. binary classifier
rosenblatt learning/training algorithm starts with random weights and increases if g(s) = 0 but should've been 1 and decreases vice versa

AND/OR/NOR are linearly separable
XOR is not. But, can re-write as (x AND y) NOR (x NOR y)
So, multi-layer perceptrons can implement any logical function
