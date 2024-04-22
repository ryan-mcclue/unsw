<!-- SPDX-License-Identifier: zlib-acknowledgement -->
TOPICS:
→ 1b. Environment Types
→ 1c. Agent Types
→ 1d. Constraint Satisfaction
TODO: cryptarithmetic
→ 2a. Reactive Agents
→ 2b. Path Search
TODO: algorithm expansion
→ 2c. Heuristic Path Search
→ 3a. Game Playing
→ 4a. Learning and Decision Trees
→ 4b. Perceptrons
→ 4c. Neural Networks
→ 5a. Probability & Uncertainty
→ 5c. Reinforcement Learning
→ 7a. Logical Agents
→ 7b. First Order Logic


FORMULAS:
* Bayesian
P(A∣B) = P(A ∧ B)/P(B)
P(A|B,C) = P(A|B ∧ C)
P(A|B ∧ C) = P(A ∧ (B ∧ C))/P(B ∧ C)

* Information Gain For Attribute:
   a = instances in class 1
   b = instances in class 2
   N = num instances
1. Entropy for Parent, e.g. overall '+'/'-'
   -(a/Nlog(a/N) + b/Nlog(b/N))
2. Entropy for attribute value 1, e.g. short
   Entropy for attribute value 2, e.g. tall
   -(a/Nlog(a/N) + b/Nlog(b/N))
3. Entropy for attribute
   (a/N)H(val1) + (b/N)H(val2)
4. Information gain
   H(parent) - H(attr)

* Laplace Pruning
1 - (n + 1)/(N + k)
n = majority
N = total
k = num classes
1. Error for parent [4, 7]
2. Error for children [2, 1]
3. Backed up error (prune if larger than parent)
(a/N * child_err + b/N * child_err)

* Perceptron

