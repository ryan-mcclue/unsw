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
% e.g. a delivery robot, convert 'map' to a weighted directed graph, i.e a search tree
% DFS improved with depth bounded limited search. naive approach will not find complete solution if cycles
% BFS improved with uniform cost search
% An iterative deepening search is a repeated depth bounded search. This gives the effect of a bfs search, but without the space complexity issues  

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
