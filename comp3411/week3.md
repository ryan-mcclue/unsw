<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Path Planning (mazes, graph search)

Babbage analytical engine was first proposed general purpose computer.
Lovelace concieved of first algorithm that would run on this machine

Game solving involves a strategy and approximation

2-players (we are assuming opponent will play optimally):
Minimax:
From perspective of one player.
In tree, a node is state, connection is move.
For each turn generate a tree of all possible moves and resulting states from current state:
  - each node wants to alternate finding the max() and then min() of its children
  - if at leaf node, do a static evaluation, e.g. chess material count, position of king etc. 
  Alpha-beta pruning:
    * alpha is best move for us so far, and beta is for opponent
      starting alpha = -∞
      starting beta = +∞
    * if max(), alpha = max(alpha, node); 
      if min(), beta = min(beta, node); 
      for any level, if beta <= alpha prune
      (IMPORTANT: follow a recursive DFS, so pass starting alpha/beta from parent)

Negamax has only one utility function, as oppose to two.
For each level choose the maximum value and negate it in the parent.
(so, each level still alternates between players)
Equates to both players looking for maximum.

So, could exploit program by 'opening up game for more moves', i.e. increase branch factor

Stochastic games:
A 'Monte Carlo' player would make move based on simulating random move spaces.
This means tree is built up stochastically
Expectimax:
  * chance nodes don't recieve alpha/beta values from children 
    similarly, chance nodes don't pass probability up to parent
    starting probability takes into account value range, e.g. [-10, 10], so: 0.1*10 + 0.5*10 + 0.4*10 = 10 
  * TODO: same pruning rules or? 
    for parent maximum, prune if alpha > P
    for parent minimum, prune if P < B

Monotonic transformation, i.e. f(x2) > f(x1)
Ordinal means definining position in series
