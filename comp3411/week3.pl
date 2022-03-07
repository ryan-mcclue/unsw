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

% in logic, a variable is not a memory location. 
% think of like a representation of an instance; 'there exists a variable such that it satisfies this condition'
% it allows for pattern matching

% static fact is something that persists. transient fact only applies at a specific instance

% semantic network; like object orientated programming making a distinction between classes and instances
% the type of knowledge is say ask for a property on an object, if it doesn't have it, get from parent (in fact object orientation taken from AI knowledge representation; hence why bad for most other things)
% it takes more work to reason this with pure logic
% nodes will be objects/values, e.g. car, vehicle, red, 4
% arcs will be attributes, e.g. 'is a', 'kind of', 'number of wheels'
% If semantic network requires non-inheritance reasoning, requires procedural attachments. 
% e.g, could use frames (code that is run when instances added, modified, deleted etc.) 

% rule based system; structured like PNF programming grammar (not actual if else statements)
% inserting a fact could cause a rule to fire which could cause another rule to fire or produce a derived fact.

% in the knowledge representations covered, they assume no uncertainty.
% to cpature uncertainty could use bayesian inference (attaching some probability to a fact)

% to prevent having to continously loop over all the rules (which would degrade performance),
% can compile rules into an inference network. in the situation of duplicate conditions across multiple rules,
% this will avoid having to iterate over the duplicated subcondition multiple times.

% from facts we can make conclusions,
% deduction: from cause, e.g. Ryan has strong glutes, get effect, e.g. Ryan is happy
% abduction: from effect, get cause (useful in diagnosing medical, psychology, aircraft faults)
% induction: from cause and effect, get rule (machine learning; this is popular as it can be tedious to manually construct all rules)

% everything outside of knowledge base is assumed false. 
% so more accurate to say can you prove this with your knowledge base, i.e. is this provable or not provable as oppose to true or false

% context is important in knowledge representation, e.g. how many rabbits? does a statue of a rabbit count, etc.

% more nerve endings from brain to eye, then from eye to brain (this is so we can predict things; we can get fooled)
% do we want cars that are 100% reliable or just more reliable than a human driver?
