% AI is understanding the operations underwhich reasoning is performed
% Reasoning is performed on knowledge

% Many components of AI (mathematics, neuroscience, etc.), however computing is the component that makes it practically useful
% This brought out the politics of AI funding in the 80s and more attainable for others to continue to advance

% As we have an infinite source of expression, we can only use heuristics to obtain a close to accurate answer  
% Similarly to complex to program complete solution, so train up to solve it

% Modern day AI dichotomy:
% 1. 'world' brain, i.e. huge data-centres of information 
% 2. child machine, i.e. learning

% Autonomous agents have many agricultural (mining, shipping, farming), commercial, etc. 
% An agent senses information and acts upon it.
% 1. Reactive agent performs minimal processing on the sensing information. No retained state. Can repeat the same action
% 2. Model based reactive agent will have a 'world model' (soccer robots can keep track of map). Cannot look into the future and plan ahead
% 3. Planning agent (usually involves search, i.e. a look ahead. assumes deterministic envrionment)
% 4. Utility (reinforced  learning; some numerical number to indicate whether the new state is better or worse than success)
% 5. Learning agent

% Uninformed search (not knowing the goal, i.e. a blind search. We often initially have to do an uninformed search first to find the goal)
% To consider search problems, it is useful to compare with a delivery robot example. In this example, we create a weighted directed graph with each node being a location.
% Note that a 'cycle' can be represented in a tree as a continual succession of the same nodes (doesn't necessarily have to be a graph structure)
% 1. DFS:
%   - Is suboptimal, i.e. may miss shortest path as it expands in the wrong order
%   - Is not complete, i.e. may get stuck in infinite loop
%   - Linear space
% 2. Iterative Deepening (utilising a repeated depth bounded search)
% 3. BFS:
%   - Is complete
%   - Is suboptimal if graph weights are different 
%   - Exponential space
% 4. Uniform Cost Search (makes next selection with a priority queue)

% planning is how you order a sequence of actions to acheive a goal

% minmax algorithm for chess

% a fact/clause
colour(a, red). 
colour(a, green). 

% we query prolog to prove a goal
% variables (uppercase; constants lowercase; _ is variable that is not printed) are possible values to prove a goal

% rule
grandchild(Grandparent, Grandchild) :-
  % conjunction
  parent(irene, Child), parent(Child, GrandChild).

% to include a file: consult(file). or [file].
