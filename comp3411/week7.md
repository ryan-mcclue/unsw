<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Planning can be done with state-based search, e.g. DFS, A\*, etc.

Some environments require a knowledge base of facts and rules to reason about those facts.
e.g. Fact: breeze; Rule: if breeze do this
Use a knowledge based agent
Knowledge Base (KB) is domain-specific set of sentences in formal language

Logics are languages representing information. 
* Syntax: is words used. 
* Semantics: meaning.
* Entailment: Necessary truth of one sentence given another. if a is true than b is true (a⊨ b). 
* Inference: derive sentence from another
* Soundness: derivations produce only entailed sentences
* Completeness: derivations produce all entailed sentences

World is a model of something if its true in that world
A sentence is:
  - 'valid' if true in all models
  - 'satisfiable' if true in some models
  (can be thought of as a CSP; number-of-clauses/number-of-symbols to get whether over or under constrained)
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

Use these to convert KB into CNF. (3-CNF would have at most 3 literals in each clause)
Resolution is a proof method that is faster than enumerating a truth table.
(Just using logic rules to prove clause?)

TODO: Resolution is sound and complete for propositional logic?

If KB in Horn clauses ((conjunction-of-positive-symbols)⇒ symbol), model checking can be done quicker with different proofs:
  - forward chaining (data-driven)
  - backward chaining (goal-driven)

First-order logic allows for combining sentences easily?
Have variables, functions, constants, predicates
Quantifiers express extent to which a statement is true: 
  1. ∀ (for all; true for all possible values in domain; universal)
  typical connector is ⇒ 
  e.g. ∀xGlitter(x)⇒ Gold(x)
  2. ∃ (for some; true for at least one value in domain; existential)
  typical connector is ∧
  e.g. ∃x(Sheep(x)∧ Black(x))

  - terms, e.g. a, f(a), mother_of(Mary)
  - atomic formulas: predicates applied to terms, e.g. likes(Mary, mother_of(Mary))

Situation calculus:
➛ conventions for describing actions and change
➛ can formulate planning as inference on a knowledge base
Query: Ask(KB, ∃s Holding(Gold, s))
Answer: s = Result(Grab, Result(Forward, S0))
so, query is answered by a plan that consists of a series of actions, e.g. plan = [forward, grab]

Actions are described by what will be true/false in the state resulting from previous state and action
∀s AtGold(s) ⇒ Holding(Gold, Result(Grab, s))
