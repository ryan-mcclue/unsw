<!-- SPDX-License-Identifier: zlib-acknowledgement -->
PROCESS (t0)
  IMPORTANT: multiline ifs have to be in sequential
  i.e. if not mutually exclusive
  IF a = 10 THEN 
  IMPORTANT: if don't exhaust all possiblities,
  will have 'implied memory' logic error, i.e
  the circuit will retain previous value when not desired

  CASE WHEN 
END PROCESS;

f <= w0 WHEN s="00" ELSE w1;

f <= w0 WHEN s="00" ELSE 
     w1 WHEN x="00";

WITH s SELECT
  f <= w0 WHEN "00",
       w1 WHEN OTHERS;

G1: FOR i IN 0 TO 3 GENERATE
  muxes: mux2to1 PORT MAP (sw(4*i to i), m(0));
  G2: IF i=2 GENERATE
    muxother: mux3to1 PORT MAP (sw(4*i to i), m(0));
  END GENERATE;
END GENERATE;


Latches (simplest form of memory) are built using cross-coupled NOR/NAND gates
Use feedback to 'trap' value.
Latch types:
  - SR (set, reset)
  - Gated SR (clock)
  - Gated D (data input)

Flip flops respond to edges rather than level
  - D (store data input on rising or falling)
  - T (toggles output on each clock)
  - JK (combine SR and T flip flop?)

Registers
  - Shift (shift data sequentially on each clock cycle)
  - Parallel-Access (shift and parallel load capabilities?)

Counters
  - Ripple (simple; prone to glitching)
  - Synchronous (all output bits change at once)


