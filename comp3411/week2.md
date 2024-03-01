<!-- SPDX-License-Identifier: zlib-acknowledgement -->
8-Puzzle Task:
* State -> Location of tiles
* Actions/Operators -> Move tile left/right/up/down
* Goal -> Tiles arranged ascending 1-8 
* Path Cost -> +1 for each tile moved

priority queue holds state space?
(often implemented as a hueristic so as to start search from a better state space)

search tree superimposed over state space
node {
  parent, children;
  depth;
  cost;
}

so search expands takes state from priority queue, expands and adds new states to queue
construct tree as you take off queue
BFS adds to back, DFS adds to front
Best First Search uses evaluation-function or a hueristic to order queue
Example heuristic straight-line distance, manhattan distance (can find one that relates to a relaxed rules version, i.e. assume tiles can move anywhere)
Larger admissable heuristic, i.e. never over estimates, dominates as best

Cost of search strategy:
- b (max. branching factor)
- d (depth of least cost solution)
- m (max. depth of state space)

Uninformed Search:
Only know goal and non-goal states
IMPORTANT: Standard BFS/DFS don't handle cycles and weights
IMPORTANT: BFS/DFS time complexities differ when used as search
* BFS: complete (finite-space), exponential space, optimal (if no weight)
  - Uniform-Cost-Search (BFS but expands based on weight; minimises g(n))
    (costs of nodes accumulate based on parent cost)
* DFS: not-complete (stuck on cycles), linear space, suboptimal (considering pre-order traversal)
  - Depth Limited (DFS but with max. d)
  (cycle detection if node contains reference to parent)
  (in tutorial, if some sorting principle on selecting next node, like alphabetical, then would deviate from strict pre-order)
* Iterative Deepening (a repeated depth limited search to combine benefits of BFS and DFS)
* Bidirectional Search (forward from initial, backward from goal

IMPORTANT: In reality, BFS is Djikstra without weights and Djikstra is A-star with a worthless heuristic.
IMPORTANT: Djikstra implementation of UCS with no goal state, i.e. will find for all paths 

Informed Search:
Have domain knowledge, so can use heuristics 
(total manhattan distance for a state would be distance all nodes from destination)
* Greedy: same as DFS, except heuristic can yield faster times
IMPORTANT: Differs to UCS in that minimises h(n) (n to goal)
* A-star: optimal if heuristic is admissable (combines greedy and UCS; so BFS expansion)
* ID-A-Star: Iterate over f(n) = g(n) + h(n)

MOTION PLANNING:
Partially observable (e.g. on-board sensors):
* Occupancy grid (x, y grid) with probability of obstacles 
Fully Observable (e.g. overhead camera)
TODO: Delaunay triangulation and Voronoi Diagram (shortest distance with obstacles?)
TODO: obstacles are probabilistic as oppose to known in graphs?
Delaunay triangulation operates on waypoints and creates a connectivity graph (that is not necessarily optimal) to then apply A-star on.
Cubic spline smoothing looks for shortest time instead of shortest distance (would be applied on A-star)
