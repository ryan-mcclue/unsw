% logic is a represenation of knowledge and also a way to make deductions from knowledge
% prolog is basically a constraint solver. constraint ordering is important as the order will determine the amount of backtracking required

% knowledge representation (various levels of abstraction) could be a world map, pixels, computer vision identification 

% Nilsson's Triple Tower (perception <-> world model <-> planning). 
% information traverses up world model to perception which transforms it to something more abstract back to the world model.
% then information traverses down from world model to planning

% forms of long-term memory:
%   episodic memory is memory of the past 
%   semantic memory is recognition 
%   procedural memory is actions to perform

% model learning is learning how actions affect the world

% neural networks are good at identifying objects, but not good for planning (symbolic memory better hear)

% 'sentences' are rules that reason information from facts (our knowledge base)

% ontology is essentially taxonomy to classify facts (sometimes easier to consider language/visual examples and translate that to more practical subjects)
% categorisation essential for knowledge representation (could be predicates)

% prolog a subset of first-order logic (which is just like set membership operators, e.g. member of, subclass of, etc.) 
% in prolog :- can be thought as meaning 'if'. First-order logic is just quantifying membership?

% in logic, a variable is not a memory location. TODO: watch for 1:45 definition of prolog variable
% think of 'there exists a variable such that it satisfies this condition'

% static fact is something that persists. transient fact only applies at a specific instance

% semantic network; like object orientated programming making a distinction between classes and instances
% nodes will be objects/values, e.g. car, vehicle, red, 4
% arcs will be attributes, e.g. 'is a', 'kind of', 'number of wheels'
% To reason, a semantic network could use frames (code that is run instances added, modified, etc.) 

% rule based system; constantly scanning 
