<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Microservices focus on decoupling as oppose to monolithic code bases.
Have to consider idempotency (same thing multiple times), latency, error propagation

Adapter/facade patterns to allow multiple interfaces to same service?

Behavioural Command Pattern
- batch and queue requests?
```
interface Command {
  void execute();
}

class LightOnCommand implements Command {
  Light l;
  execute() {
    l.on();
  }
}
class Invoker {
  List<Commands> commands;
  addCommand();
  runCommands();
}
```

Facade Pattern
- Simplify, doesn't encapsulate like adapter
```
class HomeTheatreFacade {
  Object1 o1;
  Object2 o2;
  Object3 o3;
  Object4 o4;

  void someComplexOperation() {
    o1.operate();
    o2.setOp(1, 2);
  }
}
```
