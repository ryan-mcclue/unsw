<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Use feedback to 'trap' a value

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
