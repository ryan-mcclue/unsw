<!-- SPDX-License-Identifier: zlib-acknowledgement -->
java SE -> open/oracleJDK (javac) -> JRE (vm; runs .class bytecode)

OO:
data hiding (private, getters/setters), init/deinit
same-class,same-package-and-subclasses,all

has-a is a composition, i.e. contains another class 
(method forwarding would call methods of this class)

is-a inherits

start out with all in one class (treating like C global scope), 
then refactor with extending class or interface

same name, different types overloads (override is all same)

Object superclass
abstract must override to instantiate (override for polymorphism)
interface has all implicitly abstract (allows for diamond-inheritance)
- Behavioural (callbacks)
- Structural (generics)
- Creational (singleton)
- Exceptions, generics
- Testing
Functional 
Concurrent
