<!-- SPDX-License-Identifier: zlib-acknowledgement -->

- Behavioural Template Pattern:
Same function skeleton (template method), interchangeable 'inner' part (primitive operations) 
So, a 'framework' as oppose to 'library' in that it calls us.
```
abstract class Template {
  void final templateMethod() {
    defaultHook();
    primitive1();
  }

  void defaultHook() {}

  abstract void primitive1();
}

class Concrete extends Template {
  @Override
  void primitive1() {}
}
```

- Structural Decorator Pattern
Attach functionality to object rather than class at runtime
Dynamically attach pre and post calls
```
abstract class Component {
  public abstract void operation();
}

class ComponentObject extends Component {
  void operation() {}
}

// Forwards component calls
class Decorator extends Component {
  Component c;
  void operation() { 
    prework(); 
    c.operation(); 
    postwork(); 
  } 
}

main() {
  Component c = new ComponentObject();
  c = new Decorator(c);
}
```

Generic Programming:
Type is parameter
```
interface Pair<K super Integer, V> {}

// operators like '>' only work on primitive types; so use compareTo()
class OrderedPair<K, V> implements Pair<K, V> {
  static <T extends Comparable<T>> boolean compare() 
}
```

- Structural Adapter Pattern
Interface conversion
```
class Object1ToObject2Adapter implements Object2 {
  Object1 o;
}
```

```
class Singleton {
  Singleton instance;
  Singleton getInstance() {
    if (instance == null) return new Singleton();
    else return instance;
  }
  private Singleton() {}
}
```

```
// acquires an implicit lock for scope of function
public synchronized void f() {}
```
