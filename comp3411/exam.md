<!-- SPDX-License-Identifier: zlib-acknowledgement -->
TOPICS:
→ 1b. Environment Types
Simulated/Static/Discrete/Observable/Deterministic/Sequential
PEAS
 - Performance: +1000 if gold, -1000 eaten
 - Environment: 4x4 grid, player/pit/wumpus locations
 - Actuators (->actions): Left/right/forward/back/shoot
 - Sensors (<-percepts): Breeze/stench 
 (pit causes breeze and wumpus stench in adjacent squares)
→ 1c. Agent Types
Reactive(no state)/World(state)/Planning(search)/Learning
dirt-cleaner/thermostat-regulator/self-driving/music-recommender
→ 1d. Constraint Satisfaction
- Backtrack with heuristic fewest legal values and arc consistency to propagate constraints
- Local search for many or few constraints. 
  Greedy on objective function of successor states
  `e^(cur_state-prev_state)/temp`
Cryptarithmetic:
  - Number limits
  - Carry: 4a + 1 = b or 3c + 10 + 1 = a
  - Exhaustive search
→ 2a. Reactive Agents
Braitenberg vehicle (light and obstacle sensor. move to light, away from obstacle)
- Horizontal decomposition splits functionality into independent layers that act in parallel
  More modularity, scalability.
- Vertical decomposition splits functionality into abstraction layers
  e.g low-level physical movement and high-level decision making
  More goal orientated 
→ 2b. Path Search
- UCS will expand in increasing order of g() (where g() is the shortest length)
- Greedy next shortest h()
- A-star a node is visited once expanded all of its neighbours and updated relevent node scores.
  Pick next smallest h() + g() (so g() updated as we go)
→ 2c. Heuristic Path Search
Manhatten (|x1 - x2| + |y1 - y2|)
Admissable never over-estimates
→ 3a. Game Playing
Monte Carlo search tree better if no logical static evaluation as learns it. 
TODO: expectimax walkthrough
→ 4a. Learning and Decision Trees
information entropy is how much variance data has
information gain is how much entropy removed
Laplace error used to give some value to a 0 probability
→ 4b. Perceptrons
Despite 1-layer linearly separable binary classifier; writing in CNF, 2-layer perceptron any logical function
→ 4c. Neural Networks
Unsupervised learning has no feedback, i.e. no labelled data
→ 5a. Probability & Uncertainty
Result of complexity, partial observability, noisy sensors.
→ 5c. Reinforcement Learning
Actions in environment to maximise reward 
Ideal Markov state, i.e. next state only based on previous state, not history of reaching previous state
However not always possible, e.g. temperature of wheels
→ 7a. Logical Agents
Valid in all, satisfiable in some, unsatisfiable in none.
Propositional logic can't express about objects and their relations
→ 7b. First Order Logic


FORMULAS:
* Conditional Probability
P(A∣B) = P(A ∧ B)/P(B)
P(A|B,C) = P(A|B ∧ C)
P(A|B ∧ C) = P(A ∧ (B ∧ C))/P(B ∧ C)
Independent if have no affect on the other, e.g. P(A|B) = P(A)   
Conditionally independent: P(A|B,C) = P(A|B)
* Bayes
P(A|B) = (P(B|A)P(A))/P(B)
* Prior
known = P(s1) + P(s2) ... (sum of probabilities of possible combinations)
P(a|known) = P(a) / known (where 'a' is a particular combination) 

* Information Gain For Attribute:
   a = instances in class 1
   b = instances in class 2
   N = num instances
1. Entropy for Parent, e.g. overall '+'/'-'
   IMPORTANT: log2
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
1. Convert propositional to CNF knowledge base:
  - A ⇒ B = ¬A∨ B
   ¬A ⇒ (B ∧ C) = (A ∨ B) ∧ (A ∨ C)
   ¬A ∨ B ⇒ C = (A ∨ C) ∧ (¬B ∨ C)  
  - ¬(A∨ B) = ¬A∧ ¬B
2. Resolutions:
KB⊨ query (saying that query is true in our knowledge base)
By contradiction, show that KB∧ ¬query is not true
Resolve pairs with complimentary literals, i.e. remove negated pairs from clauses and or them
Repeat this for all pairs and repeat again. If get to a point where we resolve to nothing, then a contradiction 

* First Order Logic
∀c Clown(c) → ∃b Big(b) (for every c that is a clown, there exists an object b that is big)
¬∀s (Swan(s) → White(s)) 
(it's not true that: 'for all s that is a swan, s is also white')
IMPORTANT i.e. not all swans are white (have this as answer)
TODO: more paramaters from tutorial questions

* Q-learning
transition δ(S1, a1) = S2
reward r(S1, a1) = +1
discount γ = 0.6
If γ=0, maximising immediate reward, if γ=1, maximising average reward 
1. Optimal Policy π(S1) = a1 
   Determine by exploration (when summing s1->s2 the s2 reward will be discounted)
2. Optimal Value Function
   IMPORTANT: reward is that of optimal action and state is succeeding from that action
   V(S1) = r(a2) + γV(S2) (factor out)
   or
   V(S1) = r(a1) + γV(S1) (have infinite geometric series a/(1-r) -> r(a1)/(1 - γ))
3. Q value 
   Q(S1, a1) = r(S1, a1) + γV(succeeding)
