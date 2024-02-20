<!-- SPDX-License-Identifier: zlib-acknowledgement -->

8-Puzzle Task:
* State -> Location of tiles
* Actions/Operators -> Move tile left/right/up/down
* Goal -> Tiles arranged ascending 1-8 
* Path Cost -> +1 for each tile moved

priority queue holds state space?
(often implemented as a hueristic so as to start search from a better state space)

search tree superimposed over state space?
node {
  parent, children;
  depth;
  cost;
}

so search expands takes state from queue, expands and adds new states to queue

cost of search strategy:
- b (max. branching factor)
- d (depth of least cost solution)
- m (max. depth of state space)


Uninformed Search:
Only know goal and non-goal states
IMPORTANT: BFS/DFS will halt if no cycle detection
IMPORTANT: BFS/DFS time complexities differ when used as search
* BFS: complete (finite-space), exponential space, optimal (if no weight)
  - Uniform-Cost-Search (BFS but expands based on weight)
* DFS: complete (finite-space), linear space, suboptimal
  - Depth Limited (DFS but with max. d)
* Iterative Deepening (a repeated depth limited search to combine benefits of BFS and DFS)

1. DFS:
  - Is suboptimal, i.e. may miss shortest path as it expands in the wrong order
  - Is not complete, i.e. may get stuck in infinite loop
  - Linear space
2. Iterative Deepening (utilising a repeated depth bounded search)
3. BFS:
  - Is complete
  - Is suboptimal if graph weights are different 
  - Exponential space
4. Uniform Cost Search (makes next selection with a priority queue)
IMPORTANT: In reality, BFS is Djikstra without weights and Djikstra is A* with a worthless heuristic.
IMPORTANT: djikstra implementation of ucs with no goal state, i.e. will find for all paths 

Informed Search:
Have domain knowledge, so can use heuristics
