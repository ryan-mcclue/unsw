<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Synthesiser should optimise via Karnaugh maps anyway

TODO: 2-5 variable karnaugh maps to get minimum cost realisation
number of karnaugh maps related to number of outputs
2-inputs 2x2
3-inputs 4x2
4-inputs 4x4
indices are graycoded (i.e. can only change 1 bit at a time)
implicant is anything that is 1
find prime implicants are largest power of 2 groupings (toroidal)
mark regions where variable asserted true
then, for each prime implicant, see if variable appears in it to include it  

TODO: when drawing circuit diagrams, any fan-in allowed?
IMPORTANT: when drawing circuit diagrams, start vertical with negated counterpart 
find minimal form

TODO: FPGA internal LUT structure
FPGA composed of logic blocks (whose configuration are written in SRAM)
  - LUT functionality based on configured truth-table.
    so n-input LUT as 2^n entries in truth-table
  - flip-flop memory/state 
  - multiplexor routing

Factoring expression reduces circuit cost (e.g. FO3 to FO2 gates), 
increases propagation delay
i.e. a FO3 or gate quicker than FO2 but more expensive

3-LUT implement by chaining 2-LUTs

NAND and NOR implementation preferred as less transistors
demorgan allows this transformation
to NAND:
  - bubble at AND output 
  - bubble at OR input 
  - balance
  - single inversion becomes 2-input NAND
TODO: convert back to AND-OR to get function

