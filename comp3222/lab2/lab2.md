<!-- SPDX-License-Identifier: zlib-acknowledgement -->
The distinction between 1 TO 3 and 3 DOWNTO 1 is where want MSB

1.
TODO: submit Karnaugh maps

    H(0) <= (B(2) AND NOT B(1) AND NOT B(0)) OR (NOT B(3) AND NOT B(2) AND NOT B(1) AND B(0));
    H(1) <= (NOT B(3) AND NOT B(1) AND B(0)) OR (B(2) AND B(1) AND NOT B(0));
    H(2) <= (NOT B(2) AND B(1) AND NOT B(0)) OR (NOT B(3) AND NOT B(2) AND NOT B(1) AND B(0));
    H(3) <= (NOT B(2) AND NOT B(1) AND B(0)) OR (B(2) AND NOT B(1) AND NOT B(0)) OR (B(2) AND B(1) AND B(0));
    H(4) <= (B(1) AND B(0)) OR (B(2) AND NOT B(1)) OR (B(3) AND B(0));
    H(5) <= (NOT B(2) AND B(1)) OR (B(1) AND B(0));
    H(6) <= (NOT B(3) AND NOT B(2) AND NOT B(1)) OR (B(2) AND B(1) AND B(0));

2.
TODO: have don't care outputs

circuit A is taking tens digit in case of greater than 0

a(0) <= (v(1) AND v(0)) OR (v(2) AND v(0));
a(1) <= v(2) AND NOT v(1);
a(2) <= v(2) AND v(1);

s <= v(3) AND (v(2) OR v(1));

TODO: b0: bcd_to_hex PORT MAP (v(3 DOWNTO 0), d0);
works when don't pass d0?

3.
s = (NOT a AND NOT b AND c) OR (NOT a and b AND NOT c) OR (a AND NOT b AND NOT c) OR (a AND b AND c);
co <= (b AND ci) OR (a AND ci) OR (a AND b);
s <= (NOT a AND NOT b AND ci) OR (NOT a AND b AND NOT ci) OR (a AND NOT b AND NOT ci) OR (a AND b AND ci); 
TODO: full_add includes a multiplexor component but not used?

4. 

TODO: can have out-of-order assignments, e.g. assign led to signal set later

led(7) <= (a(3) AND (a(2) OR a(1))) OR (b(3) AND (b(2) OR b(1)));

CA(3) <= NOT s(3) AND s(1); B'D
CA(2) <= (NOT s(3) AND NOT s(1)) OR (s(2) AND s(1));   B'D' + CD
CA(1) <= (NOT s(3) AND NOT s(1)) OR (NOT s(1) AND NOT s(0)) OR (NOT cout AND NOT s(2) AND s(0)); B'D' + D'E' + A'C'E
CA(0) <= s(0); E 

    m0: mux_2to1 PORT MAP (s(0), CA(0), z, M(0)); -- your mux_2to1 instantiations
    m1: mux_2to1 PORT MAP (s(1), CA(1), z, M(1)); 
    m2: mux_2to1 PORT MAP (s(2), CA(2), z, M(2)); 
    m3: mux_2to1 PORT MAP (s(3), CA(3), z, M(3));

    ds3: bcd_to_hex PORT MAP (a(3 DOWNTO 0), d3); -- your bcd_to_hex instantiation
    ds2: bcd_to_hex PORT MAP (b(3 DOWNTO 0), d2); -- your bcd_to_hex instantiation
    ds1: bcd_to_hex PORT MAP (N, d1); -- your bcd_to_hex instantiation
    ds0: bcd_to_hex PORT MAP (M(3 DOWNTO 0), d0);-- your bcd_to_hex instantiation

5.
TODO: explore different combinatorial constructs
   PROCESS (T0)
   BEGIN
     IF (T0 > 9) THEN
       Z0 <= "01010";
       C1 <= "0001";
     ELSE
       Z0 <= "00000";
       C1 <= "0000";
     END IF;
   END PROCESS;
