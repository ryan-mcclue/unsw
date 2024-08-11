<!-- SPDX-License-Identifier: zlib-acknowledgement -->

delegation forwards an operation to another object on behalf of first object

essentially make methods on containing objects

tight coupling (law of demeter/least knowledge):
where rely a lot on containing class internals, 
e.g. calling a lot of contained class methods
grouping them together can help, i.e. encapsulate

low cohesion:
methods aren't relatable,
e.g. methods to operate on contained classes 

Functional Programming: (chaining methods)
lambda can treat code as data and implement a single method interface

an existing method is an instance of a functional interface
Predicate<String> p = String::isEmpty 
(get reference to isEmpty function, whose type will be a functional interface)
Function<String, Integer> p = String::length
Consumer<String> p = (s) -> { System.out.println(s); }

Comparator<Object> 

ArrayList<E> a = new ArrayList<>(this.elements);
Collections.reverse(a);

Pipelines:
stream() creates from collection
`roster.stream().filter(p -> p.getHeight() > 190).forEach(p -> p.printName());`
filter() is intermediate, i.e. returns new stream
forEach() is terminal, i.e does not return new stream
`l.stream().filter(e -> e.length() > 10).mapToInt(e::getAge).average()`
`List<Integer> l = strings.stream().map(Integer::parseInt).collect(Collectors.toList())`

type-switch replacement with polymorphism.

IMPORTANT: if dynamic, have composition

1. common to all: inheritance
2. common to some: composition (can just override if only a small number of classes)
  - Behavioural Strategy Pattern:
  (IMPORTANT: also common for removing switch(type) statements)
  * delegation allows dynamic/change at runtime behaviour
  * can group together functions for code-reuse
  take variable operations and turn into 'behaviour'/'strategy' interfaces, e.g:
  ```
  class Satellite:
    LightDisplayInterface light_display_behaviour;
    SoundDisplayInterface sound_display_behaviour;
    
    CubeSatellite extends Satellite() {
      light_display_behaviour = new StrobeLights(); 
      sound_display_behaviour = new AcousticSounds(); 
    }

    void performLightDisplay() {
      light_display_behaviour.light_up();
    }
  ```

- Behavioural State Machine Pattern:
Helps maintain open/closed principle (class should be open for extension/closed for modification)
e.g. have to modify containing class switch statement to extend
  ```
  abstract class MachineState {
    Machine m;

    void change();
  }

  class waitingState extends MachineState {
    void change() {
      this.m.setState(new runningState(this.m));
    }
  }

  class Machine:
    MachineState curState;

    void change() {
      state.change(this);
    }
  ```
