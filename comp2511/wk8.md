<!-- SPDX-License-Identifier: zlib-acknowledgement -->
- Visitor Behavioural Pattern
External class helper functions
```
// define for all classes operating on
interface ElementVisitor {
  visit(ElementOne e);
  visit(ElementTwo e);
  visit(ElementThree e);
}

class PrintElementVisitor implements ElementVisitor {
  visit(ElementOne e) {
    print(e.getHeight());
  }
  visit(ElementTwo e) {
    print(e.getAge());
  }
}

interface VisitableElement {
  accept(Visitor v);
}

class ElementOne implements VisitableElement {
  accept(ElementVisitor ev) {
    ev.visit(this);
  }
}
```

- Iterator Pattern
Abstracting iteration
Iterator is object that allows to traverse container.
Java for loops can be given something iterable
```
class CarIterator implements Iterator<Car> {
  Car[] list;
  int position;

  Car next() {
    return list[position++]; 
  }
  boolean hasNext() {
    return position < list.length;
  }
}

class Garage implements Iterable<Car> {
  Iterator<Car> iterator() {
    return new CarIterator(cars);
  }
}
```

Testing:
  - Input space
    * Input groups, e.g. all same, decreasing etc.
    * Boundary testing
    * Randomness
  (a parameterised test runs same test with different input)

  - Property based testing (for large inputs), e.g. test calling reverse() twice gives same as original

Dealing with unknowns:
  - developing: small iterative functional changes; understand requirements to deliver actionable
  - existing: can incur technical debt that must be paid later using a slower language etc.
