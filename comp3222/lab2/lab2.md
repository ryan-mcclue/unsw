<!-- SPDX-License-Identifier: zlib-acknowledgement -->
1.
H(0) <= (B(2) AND NOT B(1) AND NOT B(0)) OR (NOT B(3) AND NOT B(2) AND NOT B(1) AND B(0));
H(1) <= (NOT B(3) AND NOT B(1) AND B(0)) OR (B(2) AND B(1) AND NOT B(0));
H(2) <= (NOT B(2) AND B(1) AND NOT B(0)) OR (NOT B(3) AND NOT B(2) AND NOT B(1) AND B(0));
H(3) <= (NOT B(2) AND NOT B(1) AND B(0)) OR (B(2) AND NOT B(1) AND NOT B(0)) OR (B(2) AND B(1) AND B(0));
H(4) <= (B(1) AND B(0)) OR (B(2) AND NOT B(1)) OR (B(3) AND B(0));
H(5) <= (NOT B(2) AND B(1)) OR (B(1) AND B(0));
H(6) <= (NOT B(3) AND NOT B(2) AND NOT B(1)) OR (B(2) AND B(1) AND B(0));

2.
circuit A is taking tens digit in case of greater than 0

a(0) <= (v(1) AND v(0)) OR (v(2) AND v(0));
a(1) <= v(2) AND NOT v(1);
a(2) <= v(2) AND v(1);

s <= v(3) AND (v(2) OR v(1));

TODO: b0: bcd_to_hex PORT MAP (v(3 DOWNTO 0), d0);
works when don't pass d0?
