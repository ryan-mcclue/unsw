<!-- SPDX-License-Identifier: zlib-acknowledgement -->
https://www.coursehero.com/textbook-solutions/Fundamentals-of-Digital-Logic-with-VHDL-Design-3rd-Edition-9780077221430-2740/

http://www.32x8.com/index.html
https://www.dcode.fr/boolean-expressions-calculator


- logic simplification
  1 + x = 1
  zz' = 0
  z + z' = 1
  IMPORTANT: x + x'yz = x + yz
  xy + xy' = x
  (x + y)' = x'y'
  gain term: xz = x(y + y')z

- canonical POS, SOP
  x = 0, y = 1, z = 0
  SOP: (x'yz')
  POS: (x + y' + z)

- karnaugh map
  prime implicants can be of different sizes (group where inputs asserted)
  f(x, y, z) = m(1, 2, 3)
               001,010,011
- circuit cost
  num_inputs + num_gates

- nand/nor circuit conversions
  single bubble for matching output component, or 2 input bubbles for opposite component
  balance bubbles even on input and output
  single inversion becomes 2-input component

- twos complement 
  (5 + (-2)) ignore carry outs

- adder
  overflow bit ignored for end calculation
  however, detect if: carry in to msb != carry out
                      carry int to msb XOR carry out

  carry = x XOR y XOR sum
  sum = x XOR y XOR carry

- shannon's expansion theorem
  `a'b'(0, 0, c + a'b(0, 1, c) + ab'(1, 0, c) + ab(1, 1, c)`

- boolean functions with decoders
  the output pins are minterm numbers, so OR relevent outputs as SOP
  Add x(y + y')z to get into minterms

- combinational logic
  A LUT is a series of multiplexors.
  A 2 input LUT has 2^2=4 memory cells.
  So, a 2LUT is a 4-1 mux.
  Each cell is a 0 or 1, and goes to input of multiplexors.
  So, the contents of each cell is determined by truth table of implemting expression.
  The inputs of LUT are selectors to these multiplexors.
  multiplexor formula is: (select)'(input0) + (select)(input1)

  selected assignment (single signal): WITH state SELECT
  conditional assignment (multiple signals): 

  invertor period is 2 * delay as have to go through circuit twice to get back to start.

- flip-flops
  if 4bit counter, 4 d-flip-flops etc.
  if contain conditional logic, would have a mux.

  IMPORTANT: the variables have values given at the instant of sensitivity list

  clock skew: t = d / s; (sqrt(4 + 4)) / (0.3c) 

  due to setup/hold times, don't want enable to be pressed near clock rise 