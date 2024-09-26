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

The output 'latches' on, i.e. feeds back in
Latch types:
  - SR
    Implemented by crossing NOR gates (NOR 00 is only 11)
    R -\- Q
    S -/- Q'
    Setting S high will set Q
    Setting R high will reset Q
    Having both R and S on at same time is invalid
    TODO: Which output high initially is random, so want to have an ability to set in known state
    TODO: Do you just ignore the Q' value?
  - D (data input)
    Similar structure to SR, except one D signal that is fed through invertor to top
    Also has an E enable signal that must be down for it to latch
    So, will hold E, D, release E, release D
    D -- Q
    E -- Q'

  TODO: clocked d latch
  https://www.youtube.com/watch?v=8bUKw2cGcGg

Flip flops respond to edges rather than level
  - D (store data input on rising or falling)
  use rising edge of clock as enable pin to D latch

  - T (toggles output on each clock)
  - JK (combine SR and T flip flop?)

Registers
  - Shift (shift data sequentially on each clock cycle)
  - Parallel-Access (shift and parallel load capabilities?)

Counters
  - Ripple (simple; prone to glitching)
  - Synchronous (all output bits change at once)


