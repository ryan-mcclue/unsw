<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Requirements analysis is external behaviour

Domain modelling part of design phase, 
Details internal high-level behaviour
Nouns entities, verbs behaviours

UML:
  - Structural

  - Behavioural
    + Class diagram
      * Directed Association (inherits)
      * Aggregation (has-a; open diamond)
      * Composition (has-a; contained class exist only here)
      Want classes for pointers
    + Object diagram

Design-by-contract over defensive programming (for unexpected errors)
pre-condition (0 < mark < 100) -> post-condition (return mark / 50) -> invariant (mark stays in range)
Only error check for things matching pre-conditions
Unit tests implement DbC. Comments/documentation specify them.
Assumes static design.
Inherited contracts can widen not lessen

TODO: throws runtime exception if pre-condition failed?
