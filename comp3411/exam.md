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
1. Initial Weight Finding (x2 might be considered y)
  1.1: Using points on axes, i.e. with 0
       m = (y2-y1)/(x2-x1) 
  1.2: A point on this line is midway between point on y_axis and 3rd point
       b = y - mx
  1.3: TODO: weights based on what is positive 
2. Learn Weights
  For bias, just +- learning-rate
  Otherwise, +- `learning-rate*input`
3. CNF
∧ bias (1/2 - n) (n is number of terms)
∨ bias (k - 1/2) (k is number of negated terms)

* Model Satisfaction
A ⇒  B only false when A=T and B=F
Write out truth tables. 
Models are for variables that when true, give results as true

* Knowledge Resolution
⇒  written in English as if-then

TODO: logic ...

* Q-learning
transition δ(S1, a1) = S2
reward r(S1, a1) = +1
discount γ = 0.6
policy π(S1) = a1
