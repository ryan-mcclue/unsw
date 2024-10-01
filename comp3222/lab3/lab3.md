<!-- SPDX-License-Identifier: zlib-acknowledgement -->
TODO: glitching in ripple adder as carries propagate
clock solves this; however what order of time is the glitch?
i.e. what is fastest concievable clock speed?
   (would look at period on oscillscope channel)

TODO: the difference between the two RTLs from lab2 is that using '+' FPGA uses built in hardware?
i.e. bypasses a LUT?

TODO: are Q' outputs often ignored?

TODO: when would level-edge be preferred if inherent glitching?

TODO: why is converting a truth table to a mux really that useful? 
      just as a human understanding, not circuit efficiency?
      For example, does synthesis do Karnaugh map or Shannon's?

TODO: would all encoders be priority encoders as more efficient to just look at one 1 bit

TODO: synthesis schematic has input and output buffers?
      what are the circuits?
      if for handling noise, what might they be?
      buffer just electrical term for input cleaning, i.e. noise handling, amplifying etc?

TODO: comparing gate delays for post-synthesis and post-implementation timing simulations seemed the same
(critical path gate delays impose max. frequency of clock)

TODO: asynchronous reset not gated
isn't synchronous more common?

2.
```
R <= NOT D;
S_g <= NOT (D AND Clk);
R_g <= NOT (R AND Clk);
Qa <= NOT (S_g AND Qb);
Qb <= NOT (R_g AND Qa);
Q <= Qa;

wait for 100 ns;    -- wait for global reset after device powers up
  D_in <= '0';  -- clk high from 105, 115, etc.
wait for 17.5 ns; -- (high, 0): 1 -> 1
  D_in <= '1'; 
wait for 5 ns; -- (low, 1): 0 -> 1
  D_in <= '0';
wait for 5 ns; -- (high, 1): 0 -> 0
  D_in <= '0';
wait for 5 ns; -- (low, 0): 1 -> 1
  D_in <= '1';
wait;
```
