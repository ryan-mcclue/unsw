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
a:instances of class a (e.g. short in class '+')
b:instances of class b (e.g. short in class '-')
N:instances in set

So, height attribute has tall and short (each of which fall into set classes)
H(S, height) = (a/N)H(S, 'short') + (b/N)H(S, 'tall')
IMPORTANT: instances here are attribute amounts
InfoGain(height) = H(S) - H(S, height)
Now, iteratively select each attribute with highest information gain as root node for decision tree

Laplace error used to give some value to a 0 probability
If the combined average Laplace error of child nodes exceeds Laplace error of parent, then prune children
(a/N * child_err + b/N * child_err)
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
may have a bias term, i.e. a constant added to output, 
e.g. for AND number of inputs, e.g. (1/2-n) (want it to be slightly greater than 0)
     for OR (n-1/2)
     for NOT (just set weight to -1)
e.g. 2 inputs, 3 weights: `w0 + x0*w1 + x1*w2`
IMPORTANT: can find initial weight values with plane geometry;
specifically, find gradient of line from sample points, e.g. (y2-y1)/(x2-x1).
then take point between points and subsitute into y=mx+b

Now, to learn weights on training data:
* Compare output class to what was expected.
  IMPORTANT: outputs will be rounded to  classes, e.g. if 2 might be rounded to -1,1
  w = w + learning_rate*(desired-actual)*input
  IMPORTANT: if bias weight, will subtract/add learning rate multiplication term
  (small learning rate will minimise removing correct classifications)
  Repeat until all training samples have correct output

perceptron can only compute linearly separable functions, i.e. points separated by line, i.e. binary classifier
rosenblatt learning/training algorithm starts with random weights and increases if g(s) = 0 but should've been 1 and decreases vice versa
AND/OR/NOR are linearly separable
XOR is not. But, can re-write as (x AND y) NOR (x NOR y)
∧ (AND; conjunction), ∨ (OR; disjunction), ¬ (NOT; negation)
Conjunctive Normal Form (CNF) is conjunction of disjunction terms
Any logical function can be put in CNF, i.e. convert anything to and/or/not
Say, have CNF: (A ∨ B) ∧ (¬ B ∨ C ∨ ¬ D) ∧ (D ∨ ¬ E)
All inputs go to disjunction hidden layer and resulting conjunction to output layer.
So, a 2-layer perceptron can implement any logical function.

TODO: This becomes a neural network (feed forward?)

Error/loss function is square difference of actual and desired output (Sum Squared Error; so in relation to weight space)
However, for classification tasks use Cross Entropy loss.
Loss functions chosen based on maximising liklihood, i.e. log(P(D|h)) (where D is output and h is hypothesis)
Sometimes have penalty/weight decay on loss function to prevent weights getting large. 

A normal perceptron activation function is a step function, i.e. if above a threshold fire.
2-layer and above use continuous activation function like sigmoid, to generate smoother error curves
(effectively doing a local search on weight space, so a smoother curve helps this)

Gradient descent used to optimise minimising loss. Backpropagate error at output to input nodes
The partial derivatives of cost function and weights show how much cost would change if weight changed
Gradient descent rule updates weights, i.e. multiplying learning rate by derivatives
