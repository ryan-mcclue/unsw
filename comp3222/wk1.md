<!-- SPDX-License-Identifier: zlib-acknowledgement -->
FPGA has logic and programmable on chip
ASIC only logic 

digital logic has inherent parallelism; higher throughput than CPU

2nd hour of 2nd lecture worked problems

Fundamentals of Digital Logic with
VHDL Design 3ed. (exercises derived)

VHDL is a description, not a program.
It will be synthesised into logic gates and interconnections and mapped to a specific FPGA architecture

Use boolean algebra as oppose to formal logic symbols
in-series: AND ·
in-parallel: OR +

commutivity, distributive, uniting (remove complement), de-morgan (complement all inverse)

provable for dual of boolean expression also

precedence: NOT, AND, OR

circuit cost is `num_inputs + num_gates`

AND all truth table terms that yield 1 to form minterm
OR minterms to form sum-of-products
minterms number is binary count of uncomplemented terms, e.g. x1!x2x3 = m5 
can also OR truth table terms that yield 0 to form maxterm, e.g. x1!x2x3 = M2
