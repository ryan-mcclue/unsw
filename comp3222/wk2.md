<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Synthesiser should optimise via Karnaugh maps anyway

TODO: 2-5 variable karnaugh maps to get minimum cost realisation
TODO: FPGA internal LUT structure

FPGA composed of logic blocks (whose configuration are written in SRAM)
  - LUT functionality based on configured truth-table.
    so n-input LUT as 2^n entries in truth-table
  - flip-flop memory/state 
  - multiplexor routing

Factoring expression reduces circuit cost (e.g. FO3 to FO2 gates), increases propagation delay
3-LUT implement by chaining 2-LUTs

NAND and NOR implementation preferred as less transistors
demorgan allows this transformation
to NAND:
  - bubble at AND output 
  - bubble at OR input 
  - balance
  - single inversion becomes 2-input NAND
TODO: convert back to AND-OR to get function

