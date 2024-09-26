<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Synthesiser should optimise via Karnaugh maps anyway

IMPORTANT: don't count cost of input inverter gate

number of karnaugh maps related to number of outputs
2-inputs 2x2
3-inputs 4x2
4-inputs 4x4
indices are graycoded (i.e. can only change 1 bit at a time)
implicant is anything that is 1
find prime implicants are largest power of 2 groupings (toroidal)
IMPORTANT: must all be largest size
mark regions where variable asserted true (for POS, take same region just invert and OR)
then, for each prime implicant, see if variable appears in it to include it  

IMPORTANT: if truth table not completely specified, can put either 0 or 1 as convenient 

IMPORTANT: when drawing circuit diagrams, start vertical with negated counterpart 
find minimal form

FPGA composed of logic blocks (whose configuration are written in SRAM)
  - LUT functionality based on configured truth-table.
    so n-input LUT as 2^n entries in truth-table
  - flip-flop memory/state 
  - multiplexor routing
  (sythesis schematic is what types of LUT used)
  (implementation schematic is what actual LUTs were used; cell-properties truth table)

Factor expression to reduce fan-in and reducing literal circuit build cost
However, larger fan-in quicker as less propagation delay

3-LUT implement by chaining 2-LUTs
Factoring, e.g. x1(x2 + x3) + x4(x2 + x3)

NAND and NOR implementation preferred as less transistors
demorgan allows this transformation
to NAND:
  - bubble at AND output 
  - bubble at OR input 
  - IMPORTANT: balance bubbles even on input and output
  - single inversion becomes 2-input NAND

