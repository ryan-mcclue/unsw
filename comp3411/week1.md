<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Turing test is a human interacts with another human and computer and can't tell whos who; If passed, not earthshattering.
A Turing machine has strip of paper with 1/0s, arrow pointing to 1/0s, can switch number and move left/right based on rules.
HTML is not Turing complete as cannot change state of system.

AI is performing reasoning on knowledge.
This may involve looking at past information, looking at a predefined goal etc. 

An agent senses information and acts upon it, ideally to maximise performance.
PEAS:
 - Performance: +1000 if gold, -1000 eaten
 - Environment: 4x4 grid, player/pit/wumpus locations
 - Actuators (->actions): Left/right/forward/back/shoot
 - Sensors (<-percepts): Breeze/stench 

Environment/task type influences agent design:
**CHESS**                                                               | **ROBOCUP**
Simulated (computer program)                                            | Situated (interacts directly with world) and Embodied (physical body)
Static (environment not changing as thinking)                           | Dynamic
Discrete (finite number of moves)                                       | Continuous
Observable (can see all pieces)                                         | Partially Observable
Deterministic                                                           | Stochastic
Sequential (evaluate based on sequence of actions, i.e. plan ahead)     | Sequential
Known (rules known)                                                     | Known

Agent types:
1. Reactive: Next action based on current percept. No state.
Braitenberg vehicle (light and obstacle sensor. move to light, away from obstacle), chemotaxis (organisms move to chemical)
Horizontal decomposition more independent layers. More adaptable to environment changes
Receive sensor input and act based on that.
Vertical decomposition more inter-connected hierarchical layers. More goal orientated 
Receive goal and try and accomplish based on sensor input.
2. Model: Keep state to look into past. Cannot look into future
3. Planning: Can look ahead (search; simulate; goals). TODO: Assumes deterministic environment?
4. Game Playing: Keep state of other player
5. Learning: Bayesian (update probabilities) 

Constraint Satisfaction Problems, e.g arranging, scheduling (N-queens, Sudoku) etc.
Consider map colouring, where variables are states, colours are values.
1. Backtracking Search
Explores variables with DFS and backtracks when current values don't satisfy.
To speed up:
* Heuristics, e.g. choose variable with fewest legal values, most constraints on variables etc.
* Constraint Propagation:
  - Forward checking: store remaining legal values so can terminate when none remain
    + Arc consistency: Each arc is a constraint between variables. 
      Making arc consistent is to update a variables remaining values based of other variable values
2. Local Search
Assigns variables randomly then change one at a time (efficient when very few or many constraints)
This iterative process can be thought of hill-climbing, e.g. at any stage could be at local/global optima.
* Choose variable that violates fewest constraints. 
* Simulated annealing, i.e. introduce a controlled (if h1 < h0) level of randomness (e^t) to escape local optima
