<!-- SPDX-License-Identifier: zlib-acknowledgement -->

SLIDES:
code smells
java docs

domain modelling:
is-a 'extends'
create files. may need to create empty functions like `addStudentToClassroom()`
just address dot points

DESIGN PRINCIPLES (code smells within):
lack of polymorphism, poor abstraction/inheritance misuse, fragility
Single-responsibility (low-cohesion)
  - feature envy (using lots of other class functions)
  - god class
  - bloaters (duplication)
Open-closed (high-coupling)
  - divergent change (single change; many changes within; switch/ifs; nesting)
  - shotgun surgery (single change; many changes elsewhere)
Liskov
  - refused bequest (does not use inherited methods)
Interface-seg
Dependency inversion
  - inappropriate intimacy (knows too much about other class)

checked exception generally something that occurs externally 
and is likely to be handled gracefully, e.g. malformedURL, not nullPointer

testing randomness with fixed seed helps verify authenticity of PRNG in use

streams:
`.collect(Collectors.toList())`
`.mapToInt(v -> v.getAge()).sum()`

```
class Person<T extends Comparable<T> & Number> {
  int compareTo(Person<T> other) {
    return this.getValue().compareTo(other.getValue());
  }
}
```

covariance (returns subclass)
contravariance (returns superclass)

compile-time polymorphism overloading
run-time overriding and inheritance
method-hiding (superclass and subclass same static method name)

try {

} catch (ex e)
{

}
