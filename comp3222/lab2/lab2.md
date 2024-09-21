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
