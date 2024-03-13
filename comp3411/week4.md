<!-- SPDX-License-Identifier: zlib-acknowledgement -->
supervised learning works with labelled data (training set):
- decision tree:
  ockham's razor means we want a smaller tree, i.e. fewer attributes
  parsimony is unwillingness to use resources
  information entropy is how much variance data has
  information gain is how much entropy removed
  huffman encoding assigns higher frequency symbols short symbols and vice versa
  entropy can be thought of the average number of bits used per symbol for a huffman encoding scheme

H(s); entropy of set with 2 classes, e.g. hired/not-hired  = -(a/Nlog(a/N) + b/Nlog(b/N))
a:instances of class a
b:instances of class b
N:instances in set

So, height attribute has tall and short (each of which fall into set classes)
H(S, height) = (a/N)H(S, 'short') + (b/N)H(S, 'tall')
InfoGain(height) = H(S) - H(S, height)
Now, iteratively select each attribute with highest information gain as root node for decision tree

Laplace error used to give some value to a 0 probability
If the combined Laplace error of child nodes exceeds Laplace error of parent, then prune children
Laplace error = 1 - (n + 1)/(N + k)
N = total number
n = majority class
k = number of classes
Typically tree node will be [10, 5]; 10 instances in majority class a, 5 instances in class b


- neural network etc.
- can have pre/post-processing and over fitting issues
unsupervised unlabelled:

reinforcement learning doesn't work with input data, rather interacts with environment and gets feedback

neuron:
dendrite (input) reaches threshold --> axon (output) --> synapse (on/off) --> dendrite ...
100billion neurons with 10000 synapses each. Delay is 5milliseconds. So favour parallelism

node:
input edges -> non-linear activation/transfer function (takes weighted sum of edges; g(s)) -> output

perceptron has inputs multiplied by learned weights which lead to output
perceptron can only compute linearly separable functions, i.e. points separated by line, i.e. binary classifier
rosenblatt learning/training algorithm starts with random weights and increases if g(s) = 0 but should've been 1 and decreases vice versa
AND/OR/NOR are linearly separable
XOR is not. But, can re-write as (x AND y) NOR (x NOR y)
So, multi-layer perceptrons can implement any logical function.
They consist of input, hidden and output layers.
This becomes a neural network (feed forward?)

Error/loss function is square difference of actual and desired output (Sum Squared Error; so in relation to weight space)
However, for classification tasks use Cross Entropy loss.
Loss functions chosen based on maximising liklihood, i.e. log(P(D|h)) (where D is output and h is hypothesis)
Sometimes have penalty/weight decay on loss function to prevent weights getting large. 

Having continuous activation function like sigmoid generates smoother error curves
(effectively doing a local search on weight space, so a smoother curve helps this)
Gradient descent used to optimise minimising loss. Backpropagate error at output to input nodes
The partial derivatives of cost function and weights show how much cost would change if weight changed
Gradient descent rule updates weights, i.e. multiplying learning rate by derivatives
