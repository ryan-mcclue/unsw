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
Dynamically attach pre and post calls, i.e. extend functionality, e.g. reduce/increase exisiting amount etc.
```
abstract class Base {
  public abstract void operation();
}

class BaseObject extends Base {
  void operation() {}
}

// Forwards component calls
class Decorator extends Base {
  Base b;
  void operation() { 
    prework(); 
    b.operation(); 
    postwork(); 
  } 
}

// IMPORTANT: an undecorate function would just return the previous contained object
main() {
  Base b = new BaseObject();
  b = new Decorator(b);
}
```

Generic Programming:
Type is parameter. Does type checks at compile time
```
interface Pair<K super Integer, V> {} 
IMPORTANT: so, base types are Object and Integer.
now, anything that could be cast to these can be passed in, i.e. subclasses of them

// operators like '>' only work on primitive types; so use compareTo()
class OrderedPair<K, V> implements Pair<K, V> {
  static <T extends Comparable<T>> boolean compare() 
}

IMPORTANT: <T> adds a type scope. So, <T>'s are different here
class Name<T> {

  public void <T> func(T t) {

  }
}

IMPORTANT: with <? extends Integer> cannot add or remove anything to it
Only use is as a function parameter

IMPORTANT: with <? super Integer> all types are Object and Integer.
so, any passed in value must castable to both Object and Integer

void func(ArrayList<? extends Integer> a) {
  Iterator<? extends Integer> it = a.iterator(); 
  (? saves having to paramaterise many possible type argument types)
  (Also, ? over just Integer, means specific type, rather than any subclass of Integer)
  while (!iterator.hasNext()) {
    sum += iterator.next();
  }
}
```

- Structural Adapter Pattern
When have two fixed incompatible endpoints and insert intermediary conversion class
```
class JSONToXMLAdapter implements Output {
  JSONOutput o;
  JSONToXMLAdapter(JSONOutput o);
}
```

```
class Singleton {
  static Singleton instance;
  Singleton synchronized getInstance() {
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
