<!-- SPDX-License-Identifier: zlib-acknowledgement -->
IMPORTANT: Q <= Q + 1; (BUFFER type)
```
GENERIC ( modulus : INTEGER := 8 ) ;

TODO: active low clears
TODO: explain registers through d-flip-flop
TODO: always have enable! 
      active low distinction!

1.
```
enables(0) <= E;
tgen: FOR i IN 0 TO 7 GENERATE
  tothers: T_ff PORT MAP (enables(i), Clk, nClear, Q(i));
  enables(i + 1) <= enables(i) AND Q(i);
END GENERATE;
```
The T Flip-Flop is implemented using a general purpose register.
The nClear, Clk and Enable signals pass to matching pins on register.
The Q output of the register is then fed back to D input of register with an inverter.
This inversion results in the next Clk/Enable pair latching a toggled D value to Q.

Implementation -> Edit Timing Constraints -> Create Clock
Implementation -> Report Timing Summary
Implementation -> Report Utilization

headroom/WNS is how much time available on critical path delay.
```
WNS = 8.429
uncertainty = 0.035ns
period = 10ns
critical_path_length = (period - WNS - uncertainty)
                     = (10 - 8.429 - 0.035)
                     = 1.536
fmax = 1 / (critical_path_length + uncertainty)
     = 1 / (1.536 + 0.035)
     = 0.637GHz
     = 637MHz
```
8 LUTs
8 FFs
11 IOs

2.
```
WNS = 7.754ns 
uncertainty = 0.035ns
period = 10ns
critical_path_length = (period - WNS - uncertainty)
                     = (10 - 7.754 - 0.035)
                     = 2.211
fmax = 1 / (critical_path_length + uncertainty)
     = 1 / (2.211 + 0.035)
     = 0.445GHz
     = 445MHz
```

2 LUT
16 FFs
19 IOs

Part 1 RTL shows registers chained together to form a counter via T-flip-flop toggling.
Part 2 RTL shows that specific addition hardware is present as well as registers.
Specifically, Carry4 hardware is present. 
In Part 1, the compiler had to insert connections between LUTs.
In Part 2, the Carry4 hardware has this connection hard-wired, so less LUTs required.

The Fmax of Part1 is higher than that of Part 2.
The critical path of Part 1 is through a single T flip-flop and enable propagation.
The critical path of Part 2 is the propagation of the carries through the Carry4 hardware.
So, it resembles a ripple structure as oppose to the parallel nature of Part1.
Therefore, Part 1 has shorter critical path and is faster than Part 2.
