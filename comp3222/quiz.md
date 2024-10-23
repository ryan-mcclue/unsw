<!-- SPDX-License-Identifier: zlib-acknowledgement -->
https://www.coursehero.com/textbook-solutions/Fundamentals-of-Digital-Logic-with-VHDL-Design-3rd-Edition-9780077221430-2740/


- logic simplification
  1 + x = 1
  zz' = 0
  z + z' = 1
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
  Add x(y + y')z to get into minterms



