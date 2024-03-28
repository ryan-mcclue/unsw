<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Planning can be done with state-based search, e.g. DFS, A\*, etc.

Some environments require a knowledge base of facts and rules to reason about those facts.
e.g. Fact: breeze; Rule: if breeze do this
Use a knowledge based agent
Knowledge Base (KB) is domain-specific set of sentences in formal language

Logics are languages representing information. Syntax is words used. Semantics is meaning.
Entailment means if a is true than b is true (a⊨ b)

World is a model of something if its true in that world
A sentence is:
  - 'valid' if true in all models
  - 'satisfiable' if true in some models
  - 'unsatisfiable' if true in no models

Propositional logic is sentences.
Logical equivalence rules: 
  - commutative (operands commute)
  (X + Y) = (Y + X)
  - associative (associate terms in brackets) 
  (X·Y)·Y = X·(Y·Y)
  - distributive (multiplying out, i.e. pulling out common factor) 
  X(X + Y) = X·X + X·Y
  - de Morgan's
  !(X + Y + ...) = !X·!Y ...

Use these to convert KB into CNF.
Resolution is a proof method that is faster than enumerating a truth table.
(Just using logic rules to prove clause?)

If KB in Horn clauses ((conjunction-of-positive-symbols)⇒ symbol), model checking can be done quicker.

TODO: Resolution is sound and complete for propositional logic?
