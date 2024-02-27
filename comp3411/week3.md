<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Path Planning (mazes, graph search)

Babbage analytical engine was first proposed general purpose computer.
Lovelace concieved of first algorithm that would run on this machine

Game solving involves a strategy and approximation

2-players (we are assuming opponent will play optimally):
Minimax:
From perspective of one player.
In tree, a node is state, connection is move.
For each turn:
  * Generating all possible moves and resulting states from current state. 
  * For each final state, do a static evaluation, e.g. chess material count, position of king etc. 
  * Backtrack score for each state. We will pick the maximum score of children, opponent will pick the minimum
    So, each level alternates between our state and opponent's state.
Alpha-beta pruning:
Alpha is best move for us so far, and beta is for opponent
If beta <= alpha, prune off (IMPORTANT: alpha/beta values are from parent)
Allows for searching much deeper 

TODO: Negamax only has one evaluation for both, by negating other opponent's score?
Pruning can also negate a move early on in its exploration 



So, could exploit program by 'opening up game for more moves', i.e. increase branch factor

Stochastic games:
A 'Monte Carlo' player would make move based on simulating random move spaces.
This means tree is built up stochastically
Expectimax adaptation that handles chance nodes. Exact values DO matter, while in minimax they don't

Monotonic transformation, i.e. f(x2) > f(x1)
Ordinal means definining position in series
