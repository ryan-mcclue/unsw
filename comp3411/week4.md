<!-- SPDX-License-Identifier: zlib-acknowledgement -->
supervised learning works with labelled data (training set):
- decision tree:
  ockham's razor means we want a smaller tree, i.e. fewer attributes
  parsimony is unwillingness to use resources
  low entropy means an attribute classifies into smaller number of groups; binary being best
  so, a low entropy attribute would give us little information
  huffman encoding assigns higher frequency symbols short symbols and vice versa
  entropy can be thought of the average number of bits used per symbol for a huffman encoding scheme
  Laplace error used to give some value to a 0 probability
  If Laplace error of child exceeds parent, then prune child
- neural network etc.
- can have pre/post-processing and over fitting issues
unsupervised unlabelled:

reinforcement learning doesn't work with input data, rather interacts with environment and gets feedback

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
