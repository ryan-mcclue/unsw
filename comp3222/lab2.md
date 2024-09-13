<!-- SPDX-License-Identifier: zlib-acknowledgement -->
TODO: When adding a design source file, why specify no input/outputs for module?

TODO: how come board seems to forget previous program on reboot?

TODO: ex3. not sure if correct.
      tips on reading simulation output

cascade 2-1 multiplexor to get multi-bit multiplexor.
`(NOT sw(0) AND X(0)) OR (sw(0) AND Y(0));` (0 maps to X)
chain 2-1 multiplexor to get 3-1 multiplexor.




```
-- iii
N(0) <= (NOT s(0) AND U(0)) OR (s(0) AND V(0));
N(1) <= (NOT s(0) AND U(1)) OR (s(0) AND V(1));
M(0) <= (NOT s(1) AND N(0)) OR (s(1) AND W(0));
M(1) <= (NOT s(1) AND N(1)) OR (s(1) AND W(1));

-- iv (TODO: regenerate expressions with 0 being on)
seg(0) <= NOT (c(1) AND NOT c(0)); -- add logic expressions in terms of c(1) and c(0) to describe the output signals
seg(1) <= c(0);
seg(2) <= NOT ((NOT c(1)) OR (c(1) AND (NOT c(0))));
seg(3) <= NOT ((NOT c(1)) OR (c(1) AND (NOT c(0))));
seg(4) <= c(1);
seg(5) <= NOT ((NOT c(1)) AND c(0));
seg(6) <= NOT ((NOT c(1)) OR (c(1) AND (NOT c(0))));

-- v (anode specific to display, cathode per segment)
```
