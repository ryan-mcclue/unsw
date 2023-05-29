% Informed search is when we have a way to estimate how far away are we from our goal, i.e. have domain knowledge
% An admissable heuristic is one that underestimates
% A consistent heuristic has f(n) always decreasing, 
% where f(n) = g(n) (tracking cost) + h(n) (heuristic)

% Example heuristics: manhatten distance, straight line distance (as crow flies), number of misplaced tiles, etc.

% If one heuristic always gives larger than another it dominates the other and is better. 
% This is because it is closer to the actual cost.

% Greedy (a greedy algorithm is memory efficient to implement, however gets caught in situations like cycles) best first search is like DFS, 
% except it picks next node based on heuristic

% A* stores total cost and current heuristic (combines memory efficient best-first-search and optimal+complete ucs). 
% It adds frontier nodes to a priority queue, which is what makes the algorithm optimal.
% Using a heuristic drastically reduces search space
% When expanding nodes in A*, e.g. (A, running_cost, f(n)) 

% With assignment question 2, tradeoff between greediness and optimality

% Examples of constraint satisfaction problems: transit scheduling, circuit layout, assignment
% CSP is to find variables from their domains that don't violate constraints
% Translated to a constraint graph, nodes are variables, arcs are constraints 
% Types of constraints are unary, binary, higher order, inequality
% An adjacency relationship means nodes are connected
% As opposed to path search, with constraint search the goal state is unknown
% With constraint search, solvability is difficult without heuristics

% Backtracking search. Like a DFS, assigning one value, then a new one which doesn't conflict and move on
% Various heuristics to improve this (often the optimal heuristic will be determined via experimentation):
%   Minimum Remaining Values, i.e. pick the variable that is the most constrained (smallest domain perhaps)
%   Least Constraining Value. This means we won't have to backtrack as much
%   Forward Checking, we keep track of remaining legal values . So, in a sense we propagate the constraints forwards to detect a failure earlier 
% Middle ground between number of constraints and available domains in determining problem difficulty

% For send + money problem, consider pairing equality, e.g. D + E > 11

% arc consistency example of forward checking that constantly propagates constraints down (forward checking not always propagate). so there is an arc consistency algorithm
%
% variable elimination remove a node and add a new constraint between the nodes of the removed node
% 1. write out constraint extension
% 2. union extensions

% Local search (iterative improvement, hill climb search) first sets out variables with most constraint violations. 
% Then progress through each variable and try and remove/reduce constraints iteratively.
% To prevent local minima, i.e. situation where you can't get any better, introduce randomness. A form of this is simulated annealing, i.e modeling change in temperatue

% prolog good for constraint solving problems

% could domain split from {1, 2, 3, 4} with {1,2} and {3,4} or {1},{2},{3},{4}
