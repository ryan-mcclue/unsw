<!-- SPDX-License-Identifier: zlib-acknowledgement -->

delegation forwards an operation to another object on behalf of first object

essentially make methods on containing objects

tight coupling:
where rely a lot on containing class internals, 
e.g. calling a lot of contained class methods
grouping them together can help

low cohesion:
methods aren't relatable,
e.g. methods to operate on contained classes 

type-switch replacement:
1. inheritance
2. if type can change during lifetime use composition?
favor composition over inheritance?

Functional Programming: (chaining methods)
lambda can treat code as data and implement a single method interface

an existing method is an instance of a functional interface
Predicate<String> p = String::isEmpty (get reference to isEmpty function, whose type will be a functional interface)
Function<String, Integer> p = String::length
Consumer<String> p = (s) -> { System.out.println(s); }
Comparator<Object> 

Pipelines:
stream() creates from collection
`roster.stream().filter(p -> p.getHeight() > 190).forEach(p -> p.printName());`
filter() is intermediate, i.e. returns new stream
forEach() is terminal, i.e does not return new stream
`l.stream().filter(e -> e.length() > 10).mapToInt(e::getAge).average()`



