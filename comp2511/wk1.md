<!-- SPDX-License-Identifier: zlib-acknowledgement -->
java SE -> open/oracleJDK (javac) -> JRE (vm; runs .class bytecode)

OO:
data hiding (private, getters/setters), init/deinit
class,package,global visibility

has-a is a composition, i.e. contains another class (method forwarding would call methods of this class)

start out with all in one class (treating like C global scope), then refactor with extending class or interface

Object superclass
abstract must override to instantiate (can also override superclass functions)
interface has all implicitly abstract
- Behavioural (callbacks)
- Structural (generics)
- Creational (singleton)
- Exceptions, generics
- Testing
Functional 
Concurrent
