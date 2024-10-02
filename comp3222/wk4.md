<!-- SPDX-License-Identifier: zlib-acknowledgement -->
RTL schematic looks at vhdl code (logic gates)
Synthesis schematic will look at netlist (LUTs)

Testbench is file that encodes a simulation.
Behavioural simulation for testing inputs.
Timing simulation to see gate delays. 
IMPORTANT: to maintain internal signal presence in simulation:
```
SIGNAL R_g, S_g, Qa, Qb : STD_LOGIC;
ATTRIBUTE DONT_TOUCH : STRING;
ATTRIBUTE DONT_TOUCH OF R_g, S_g, Qa, Qb : SIGNAL IS "true";
```

# Behavioural Process
PROCESS (clk)

# Combinatorial Process
PROCESS (t0)
  IMPORTANT: multiline ifs have to be in sequential
  i.e. if not mutually exclusive
  IF a = 10 THEN 
  IMPORTANT: if don't exhaust all possiblities,
  will have 'implied memory' logic error, i.e
  the circuit will retain previous value when not desired
  CASE WHEN 
END PROCESS;

## Multiplexor
IMPORTANT: prefer WITHs and WHENs for performance
WITH s SELECT
  f <= w0 WHEN "00",
       w1 WHEN "01",
       w2 WHEN "10",
       w3 WHEN OTHERS;

AeqB <= '1' WHEN A = B ELSE '0' ;
f <= w0 WHEN s="00" ELSE w1;

PROCESS ( w0, w1, s )
BEGIN
  IF s = '0' THEN
    f <= w0 ;
  ELSE
    f <= w1 ;
  END IF ;
END PROCESS ;


## Cascading
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
  IMPORTANT: gated variants mean takes clk as enable, but level detection
  i.e. the inputs are gated by the clock
  TODO: is the glitching from level detection really an issue?

Flip flops respond to clock pulses.
  - D (store data input on rising or falling)
  TODO: most common?
  use rising edge of clock as enable pin to D latch (so EN replaced with CLK)
  so, only changing value at specified moments in time
  will have an edge detector circuit
    - 1 input and inversion to AND gate (the delay for invertor gives pulse)
    - simpler capacitor and resistor
  - SR
   has CLK, S and R
  - JK 
   Like SR, except has additional feedback, so 3 fanin AND gates at start.
   Fixes 'invalid' state of S=R=1, whereby it toggles in this state.
   This toggling can be used to create a counters:
     - Ripple
       Chaining output of 1 flip-flop to clk of other.
       Prone to glitching due to time for signal to propagate.
     - Synchronous 
       All flip-flops use same clk, so all output bits change at once.
       The interconnections involve AND gates to toggle.
      TODO: use cases, e.g. clock division?
   IMPORTANT: racing occurs on toggling where clock pulse is too short and continually toggles back and forth during pulse time
   TODO: is racing just an artefact of RC edge detection circuit?

   Can overcome racing with master-slave JK flip-flop.
   In effect, connecting two SR latches; 1 master, 1 slave (only active when clock low). 
   So both will never be active.
   Therefore, master active on clock high, then slave active on low.
   No need for a RC circuit, as will only change on one complete clock cycle.
  - T (merges JK lines to single T)

Registers
  - General Purpose
    Series of D flip-flops
    So, for 8bit would have QA, QB, QC, etc.

  - Shift (shift data sequentially on each clock cycle)
    Series of flip-flops with interconnections
    TODO: for 8bit, has 1 data in and 8 data outs?
    TODO: data out for 1 can be wired to data in for other, so 2-8bit shifts to control 16

    clock line as normal
    'latch' line takes data from storage registers to outputs?
    so, always shifting into QA storage register.

    TODO: Can control in effective unlimited of outputs?
  - Parallel-Access (shift and parallel load capabilities?)
