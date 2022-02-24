% Informed search is when we have a way to estimate how far away are we from our goal, i.e. have domain knowledge
% An admissable heuristic is one that underestimates
% A consistent heuristic has f(n) always decreasing, 
% where f(n) = g(n) (tracking cost) + h(n) (heuristic)

% Example heuristics: manhatten distance, straight line distance (as crow flies), number of misplaced tiles, etc.

% If one heuristic always gives larger than another it dominates the other and is better. 
% This is because it is closer to the actual cost.

% Greedy (a greedy algorithm is memory efficient to implement, however gets caught in situations like cycles) best first search is like DFS, except it picks next node based on heuristic

% A* stores total cost and current heuristic (combines memory efficient best-first-search and optimal+complete ucs). 
% It adds frontier nodes to a priority queue, which is what makes the algorithm optimal.
% Using a heuristic drastically reduces search space
% When expanding nodes in A*, e.g. (A, running_cost, f(n)) 

% With assignment question 2, tradeoff between greediness and optimality
