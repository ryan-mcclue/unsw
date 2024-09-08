<!-- SPDX-License-Identifier: zlib-acknowledgement -->

- Behavioural Observer Pattern:
Callbacks. 
Observable/subject object maintains list of observers/subscribers and notifies them.
Observable will call observers interface function

```
interface Subject {
  attach(Observer o);
  detach(Observer o);
  notify();
}

class Sensor implements Subject {
  ArrayList<Observers> o;
}

interface Observer {
  update(Subject s);
}

class Monitor implements Observer {
  update(Subject s) {
    if (s instanceof Sensor) {

    }
  }
}

```

- Structural Composite Pattern 
Tree structures
```
// uniformity; (type-safety option removes child() from interface and requires typecasting)
interface Component {
  calculateCost();
  addChild(Componet c);
  removeChild(Componet c);
  getChild(int i);
}
class Leaf implements Component {

}
class Composite implements Component {
  ArrayList<Component> c;
}
```

```
interface Expression {
  double evaluate()
}

(leaf)
class Number implements Expression {
  double value;
}
(components)
class Add/Sub/Div/Mul implements Expression {
  Expression e1; 
  Expression e2;
}
```

- Creational Factory Method Pattern
(Abstract Factory has many factories)
Create object without specifying exact class
```
// what all creations must have
interface Button {

}
class WebButton implements Button {

}

(useful for objects with lots of composition contructors)
abstract class DialogFactory {
  factoryCreateButton();
  factoryCreateScrollbar();
}
(one for each object creation extracting over)
class WebDialogFactory extends DialogFactory {
  @Override
  factoryCreateButton();
}

class Client {
  DialogFactory f;
}

```
