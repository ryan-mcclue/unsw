<!-- SPDX-License-Identifier: zlib-acknowledgement -->
When exception thrown, call stack will be unwound to find appropriate exception handler to catch it.
(All inherit from Throwable)
- Checked (io; inherit only from Exception; are checked by compiler, i.e. must handle in throws)
- Unchecked (inherit from Error or Runtime; majority)
  * Error (out of memory)
  * Runtime (array index)
Try and handle exception as early on as possible.  

```
Node<T> (T type)
Map<K, V> (K key, V value)
List<E> (E element)
```
Collection is grouping of objects/elements, e.g. queue, list etc.
Implement collection interface.

JUnit:
- Test case is class (can also have @Nested)
@TestInstance(value = Lifecycle.PER_CLASS)
- Method is @Test
- @TestFactory dynamic test (return a stream/collection/iterable test object)

Ideal software has: low coupling, high cohesion
Reduces rigidity (refactoring hard), fragility (break many in one place), etc.
To acheive this have 'design principles', e.g. DRY, KISS, SOLID (single-responsibility;liskov)
1. Law of Demeter (just call methods within class, e.g. no o.get().get() etc.)
2. LSP (passing subclasses as parent classes should work. 
        so, inherited methods must make sense for subclass.
        if not, favour composition over inheritance)
        (IMPORTANT: violation of LSP even if 'still work', rather has attributes that don't make logical sense)


DESIGN PRINCIPLES (code smells within):

lack of polymorphism, poor abstraction/inheritance misuse

Single-responsibility (low-cohesion)
  - feature envy (using lots of other class functions)
  - god class
  - bloaters (duplication, deep nesting etc.)
Open-closed (high-coupling)
  - divergent change (single change; many changes within)
  - shotgun surgery (single change; many changes elsewhere)
Liskov
  - refused bequest (does not use inherited methods)
Interface-seg
Dependency inversion
  - inappropriate intimacy (knows too much about other class)


Covariance allows for returning subclass types when overriding
Contravariance allows for defining parentclass types (will not override)
