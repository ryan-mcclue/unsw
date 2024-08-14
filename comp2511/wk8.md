<!-- SPDX-License-Identifier: zlib-acknowledgement -->
- Visitor Behavioural Pattern
External class helper functions (need to iterate through different classes)
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

Builder Pattern:
- Breaking long parameter list, e.g. `Car c = new Car(a, b, c, d, ...)`
  Create functions that create object in stages
```
interface CarBuilder {
  reset();
  setSeats();
  setEngine();
  setGPS();
  getResult();
}
class SportsCarBuilder implements CarBuilder {
  SportsCar c;
  reset() { c = new SportsCar(); }
  getResult() { return c; }
}

CarBuilder cb = new SportsCarBuilder();
cb.setSeats(2);
cb.setGPS(new FancyGPS());
SportsCar = cb.getResult();

// A director may then collate these recipes
class CarDirector {
  Builder b;
  makeSportsCar(builder) {
    builder.reset();
    builder.setEngine();
  }
}
CarDirector d = new CarDirector();
d.makeSportsCar(builder);
SportsCar = builder.getResult();
```

Testing:
  - Input space
    * Input groups, e.g. all same, decreasing etc.
    * Boundary testing
    * Randomness (testing randomness with known seed; compare outputs of two objects to see same)
  (a parameterised test runs same test with different input)

  - Property based testing (for large inputs), e.g. test calling reverse() twice gives same as original

Dealing with unknowns:
  - developing: small iterative functional changes; understand requirements to deliver actionable
  - existing: can incur technical debt that must be paid later using a slower language etc.
