<!-- SPDX-License-Identifier: zlib-acknowledgement -->
1.
```
enables(0) <= E;
tgen: FOR i IN 0 TO 7 GENERATE
  tothers: T_ff PORT MAP (enables(i), Clk, nClear, Q(i));
  enables(i + 1) <= enables(i) AND Q(i);
END GENERATE;
```
The T Flip-Flop is implemented using a general purpose register.
The nClear signal passes through a mux to achieve active-low logic which is then passed to register reset signal.
The Clk and Enable signals pass to same pins on register.
The Q output of the register is then fed back to D input of register with an inverter.
The result is that each Clk/Enable pair toggles the D and Q.

Implementation -> Edit Timing Constraints -> Create Clock
Implementation -> Report Timing Summary
Implementation -> Report Utilization

headroom/WNS is how much time available on critical path delay.

```
WNS = 8.429ns
uncertainty = 0.035ns
period = 10ns
critical_path_length = (period - WNS) + uncertainty
                     = (10 - 8.429) + 0.035
                     = 1.606ns
fmax = 1 / critical_path_length
     = 1 / 1.606
     = 0.623THz
     = 623GHz
```
8 LUTs
8 FFs
11 IOs

2.
