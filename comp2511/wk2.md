<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Requirements analysis is external behaviour

Domain modelling part of design phase, 
Details internal high-level behaviour
Nouns entities, verbs behaviours

UML:
  - Structural

What is difference between association and inheritance?

  - Behavioural
    + Class diagram
      * Association (just uses, e.g. use a math library)
      * Directed Association (inherits)
      * Aggregation (has-a; open diamond)
      * Composition (has-a; contained class exist only here; dark diamond)
      * 'realisation/implementation' arrow for interfaces
      Want classes for pointers
    + Object diagram

Design-by-contract over defensive programming (for unexpected errors)
(cannot throw exceptions if not inherited)
pre-condition (0 < mark < 100) -> post-condition (return mark / 50) -> invariant (mark stays in range)
Only error check for things matching pre-conditions
Unit tests implement DbC. Comments/documentation specify them.
Assumes static design.
Inherited contracts can widen not lessen

```
equals(Object o) { p = (Parent)o; if (p == null) false; }
```

